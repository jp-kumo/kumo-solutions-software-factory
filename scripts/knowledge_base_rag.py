#!/usr/bin/env python3
from __future__ import annotations

import argparse
import contextlib
import dataclasses
import datetime as dt
import functools
import hashlib
import json
import math
import os
import re
import signal
import sqlite3
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

try:
    import requests
except Exception:
    requests = None

WORKSPACE = Path("/home/jpadmin/.openclaw/workspace")
DATA_DIR = WORKSPACE / "data"
DB_PATH = DATA_DIR / "knowledge_base.sqlite"
LOCK_PATH = DATA_DIR / "knowledge_base.lock"
CFG_PATH = WORKSPACE / "configs" / "knowledge_base.json"

TRACKING_PARAMS = {"utm_source", "utm_medium", "utm_campaign", "fbclid", "igshid", "ref", "s", "t"}
ERROR_SIGNALS = ["access denied", "captcha", "please enable javascript", "cloudflare", "404", "sign in", "blocked", "rate limit"]


DEFAULT_CFG = {
    "embedding_provider": "gemini",  # gemini|openai
    "embedding_model_gemini": "models/gemini-embedding-001",
    "embedding_model_openai": "text-embedding-3-small",
    "synthesis_provider": "auto",  # auto|gemini|openai|none
    "synthesis_model_gemini": "models/gemini-flash-latest",
    "synthesis_model_openai": "gpt-4o-mini",
    "max_content_chars": 200000,
    "min_chars": 20,
    "min_non_tweet_chars": 500,
    "chunk_size": 800,
    "chunk_overlap": 200,
    "min_chunk_size": 100,
    "batch_size": 10,
    "batch_delay_ms": 200,
    "retrieval_top_k": 10,
}


@dataclasses.dataclass
class Extracted:
    title: str
    content: str
    source_type: str
    canonical_url: str


def ensure_paths() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    CFG_PATH.parent.mkdir(parents=True, exist_ok=True)


def load_cfg() -> Dict[str, Any]:
    ensure_paths()
    if not CFG_PATH.exists():
        CFG_PATH.write_text(json.dumps(DEFAULT_CFG, indent=2) + "\n", encoding="utf-8")
        return dict(DEFAULT_CFG)
    cfg = json.loads(CFG_PATH.read_text(encoding="utf-8"))
    out = dict(DEFAULT_CFG)
    out.update(cfg)
    return out


def db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys=ON;")
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    return conn


def init_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS sources (
          id INTEGER PRIMARY KEY,
          url TEXT,
          normalized_url TEXT,
          title TEXT,
          source_type TEXT,
          summary TEXT,
          raw_content TEXT,
          content_hash TEXT UNIQUE,
          tags TEXT,
          created_at TEXT DEFAULT CURRENT_TIMESTAMP,
          updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS chunks (
          id INTEGER PRIMARY KEY,
          source_id INTEGER NOT NULL,
          chunk_index INTEGER NOT NULL,
          content TEXT,
          embedding BLOB,
          embedding_dim INTEGER,
          embedding_provider TEXT,
          embedding_model TEXT,
          created_at TEXT DEFAULT CURRENT_TIMESTAMP,
          FOREIGN KEY(source_id) REFERENCES sources(id) ON DELETE CASCADE
        );

        CREATE INDEX IF NOT EXISTS idx_chunks_source_id ON chunks(source_id);
        CREATE INDEX IF NOT EXISTS idx_sources_source_type ON sources(source_type);
        CREATE INDEX IF NOT EXISTS idx_sources_content_hash ON sources(content_hash);
        CREATE UNIQUE INDEX IF NOT EXISTS idx_sources_normalized_url ON sources(normalized_url);
        """
    )
    conn.commit()


def is_pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except Exception:
        return False


@contextlib.contextmanager
def ingestion_lock(max_age_sec: int = 900):
    ensure_paths()
    now = time.time()
    if LOCK_PATH.exists():
        try:
            meta = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
            pid = int(meta.get("pid", -1))
            ts = float(meta.get("ts", 0))
            stale = (now - ts) > max_age_sec or (pid > 0 and not is_pid_alive(pid))
            if not stale:
                raise RuntimeError("ingestion lock active")
        except Exception:
            pass
    LOCK_PATH.write_text(json.dumps({"pid": os.getpid(), "ts": now}), encoding="utf-8")
    try:
        yield
    finally:
        with contextlib.suppress(Exception):
            LOCK_PATH.unlink()


def detect_source_type(input_value: str) -> str:
    s = input_value.lower().strip()
    if s.startswith("http://") or s.startswith("https://"):
        if "x.com/" in s or "twitter.com/" in s:
            return "tweet"
        if "youtube.com/" in s or "youtu.be/" in s:
            return "video"
        if s.endswith(".pdf"):
            return "pdf"
        return "article"
    ext = Path(s).suffix.lower()
    if ext == ".pdf":
        return "pdf"
    if ext in {".txt", ".md", ".rtf"}:
        return "text"
    return "other"


def normalize_url(url: str) -> str:
    p = urlparse(url)
    scheme = p.scheme.lower() or "https"
    netloc = p.netloc.lower()
    if netloc.startswith("www."):
        netloc = netloc[4:]
    if netloc == "twitter.com":
        netloc = "x.com"
    qp = [(k, v) for k, v in parse_qsl(p.query, keep_blank_values=True) if k.lower() not in TRACKING_PARAMS]
    query = urlencode(qp)
    path = p.path.rstrip("/") or "/"
    return urlunparse((scheme, netloc, path, "", query, ""))


def retry_transient(fn, retries: int = 1, delay_sec: float = 2.0):
    transient = ("ECONNRESET", "ETIMEDOUT", "ENOTFOUND", "DNS", "timeout", "Connection aborted")
    for i in range(retries + 1):
        try:
            return fn()
        except Exception as e:
            msg = str(e)
            if i < retries and any(t.lower() in msg.lower() for t in transient):
                time.sleep(delay_sec)
                continue
            raise


def strip_html(html: str) -> str:
    text = re.sub(r"<script[\s\S]*?</script>", " ", html, flags=re.I)
    text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_tweet(url: str) -> Tuple[str, str]:
    if requests is None:
        raise RuntimeError("requests unavailable")

    def fx():
        api = "https://api.fxtwitter.com/status/"
        m = re.search(r"status/(\d+)", url)
        if not m:
            raise RuntimeError("missing tweet id")
        r = requests.get(api + m.group(1), timeout=20)
        r.raise_for_status()
        j = r.json()
        text = j.get("tweet", {}).get("text") or j.get("text") or ""
        title = j.get("tweet", {}).get("author", {}).get("name") or "Tweet"
        return title, text

    def x_oembed():
        r = requests.get("https://publish.twitter.com/oembed", params={"url": url}, timeout=20)
        r.raise_for_status()
        j = r.json()
        return "Tweet", strip_html(j.get("html", ""))

    def scrape():
        r = requests.get(url, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
        return "Tweet", strip_html(r.text)

    for fn in (fx, x_oembed, scrape):
        with contextlib.suppress(Exception):
            return retry_transient(fn)
    raise RuntimeError("tweet extraction failed")


def extract_youtube(url: str) -> Tuple[str, str]:
    # chain: youtube transcript api -> yt-dlp
    with contextlib.suppress(Exception):
        from youtube_transcript_api import YouTubeTranscriptApi  # type: ignore

        vid = None
        m = re.search(r"v=([A-Za-z0-9_-]{11})", url)
        if m:
            vid = m.group(1)
        m2 = re.search(r"youtu\.be/([A-Za-z0-9_-]{11})", url)
        if not vid and m2:
            vid = m2.group(1)
        if vid:
            items = YouTubeTranscriptApi.get_transcript(vid)
            text = "\n".join(x.get("text", "") for x in items)
            return "YouTube Video", text

    # yt-dlp fallback
    cmd = ["yt-dlp", "--skip-download", "--write-auto-sub", "--write-sub", "--sub-langs", "en.*", "--convert-subs", "srt", "--print", "title", "--print", "description", url]
    out = subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL)
    parts = out.splitlines()
    title = parts[0] if parts else "YouTube Video"
    desc = "\n".join(parts[1:])
    return title, desc


def extract_pdf(path_or_url: str) -> Tuple[str, str]:
    path = Path(path_or_url)
    tmp_path: Optional[Path] = None
    if path_or_url.startswith("http"):
        if requests is None:
            raise RuntimeError("requests unavailable")
        r = requests.get(path_or_url, timeout=30)
        r.raise_for_status()
        tmp_path = DATA_DIR / f"tmp_{int(time.time())}.pdf"
        tmp_path.write_bytes(r.content)
        path = tmp_path

    try:
        text = subprocess.check_output(["pdftotext", str(path), "-"], text=True)
    finally:
        if tmp_path and tmp_path.exists():
            tmp_path.unlink(missing_ok=True)
    return path.name, text


def extract_article(url: str) -> Tuple[str, str]:
    # a) readability/trafilatura, b) firecrawl/apify, c) headless, d) raw
    if requests is None:
        raise RuntimeError("requests unavailable")

    # a) trafilatura
    with contextlib.suppress(Exception):
        import trafilatura  # type: ignore

        html = requests.get(url, timeout=25, headers={"User-Agent": "Mozilla/5.0"}).text
        txt = trafilatura.extract(html, include_comments=False, include_tables=False) or ""
        if txt.strip():
            title = trafilatura.extract_metadata(html).title if trafilatura.extract_metadata(html) else "Article"
            return title or "Article", txt

    # b) firecrawl
    firecrawl_key = os.getenv("FIRECRAWL_API_KEY", "").strip()
    if firecrawl_key and requests is not None:
        with contextlib.suppress(Exception):
            r = requests.post(
                "https://api.firecrawl.dev/v1/scrape",
                headers={"Authorization": f"Bearer {firecrawl_key}", "Content-Type": "application/json"},
                json={"url": url, "formats": ["markdown"]},
                timeout=30,
            )
            r.raise_for_status()
            j = r.json()
            md = j.get("data", {}).get("markdown", "")
            if md.strip():
                return j.get("data", {}).get("title", "Article"), md

    # c) headless browser fallback via playwright if available
    with contextlib.suppress(Exception):
        js = (
            "const { chromium } = require('playwright');"
            "(async()=>{const b=await chromium.launch({headless:true});"
            "const p=await b.newPage();await p.goto(process.argv[1],{waitUntil:'networkidle'});"
            "const t=await p.title();const c=await p.content();console.log(JSON.stringify({t,c}));await b.close();})();"
        )
        out = subprocess.check_output(["node", "-e", js, url], text=True, timeout=60)
        j = json.loads(out)
        return j.get("t", "Article"), strip_html(j.get("c", ""))

    # d) raw fetch + stripping
    r = requests.get(url, timeout=25, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    html = r.text
    title_match = re.search(r"<title>(.*?)</title>", html, re.I | re.S)
    title = strip_html(title_match.group(1)) if title_match else "Article"
    return title, strip_html(html)


def extract_text(path: str) -> Tuple[str, str]:
    p = Path(path)
    return p.name, p.read_text(encoding="utf-8", errors="ignore")


def validate_content(source_type: str, content: str, cfg: Dict[str, Any], strict: bool = True) -> Tuple[bool, str, str]:
    content = (content or "").strip()
    if len(content) < int(cfg["min_chars"]):
        return False, "too_short", content

    content = content[: int(cfg["max_content_chars"])]

    if not strict:
        return True, "ok", content

    lower = content.lower()
    err_hits = sum(1 for s in ERROR_SIGNALS if s in lower)
    if err_hits >= 2:
        return False, "error_page_signals", content

    if source_type != "tweet":
        if len(content) < int(cfg["min_non_tweet_chars"]):
            return False, "non_tweet_too_short", content
        lines = [ln.strip() for ln in content.splitlines() if ln.strip()]
        if lines:
            long_lines = sum(1 for ln in lines if len(ln) > 80)
            ratio = long_lines / max(1, len(lines))
            if ratio < 0.15:
                return False, "low_prose_ratio", content

    return True, "ok", content


def sentence_chunks(text: str, size: int, overlap: int, min_size: int) -> List[str]:
    parts = re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", text.strip()))
    chunks: List[str] = []
    cur = ""
    for p in parts:
        if len(cur) + len(p) + 1 <= size:
            cur = (cur + " " + p).strip()
        else:
            if cur:
                chunks.append(cur)
            cur = p
    if cur:
        chunks.append(cur)

    # overlap stitching
    out: List[str] = []
    for i, ch in enumerate(chunks):
        if i == 0:
            out.append(ch)
            continue
        prev = out[-1]
        ov = prev[-overlap:] if overlap > 0 else ""
        merged = (ov + " " + ch).strip()
        out.append(merged[:size])

    # append tiny remainder to previous
    fixed: List[str] = []
    for ch in out:
        if fixed and len(ch) < min_size:
            fixed[-1] = (fixed[-1] + " " + ch).strip()
        else:
            fixed.append(ch)
    return fixed


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8", errors="ignore")).hexdigest()


@functools.lru_cache(maxsize=1000)
def _embed_cached(provider: str, model: str, text: str) -> Tuple[float, ...]:
    if len(text) > 8000:
        text = text[:8000]

    if requests is None:
        raise RuntimeError("requests unavailable")

    if provider == "gemini":
        key = os.getenv("GEMINI_API_KEY", "").strip()
        if not key:
            raise RuntimeError("GEMINI_API_KEY missing")
        url = f"https://generativelanguage.googleapis.com/v1beta/{model}:embedContent?key={key}"
        payload = {"model": model, "content": {"parts": [{"text": text}]}}
        r = requests.post(url, json=payload, timeout=30)
        r.raise_for_status()
        v = r.json().get("embedding", {}).get("values", [])
        return tuple(float(x) for x in v)

    if provider == "openai":
        key = os.getenv("OPENAI_API_KEY", "").strip()
        if not key:
            raise RuntimeError("OPENAI_API_KEY missing")
        r = requests.post(
            "https://api.openai.com/v1/embeddings",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={"model": model, "input": text},
            timeout=30,
        )
        r.raise_for_status()
        v = r.json().get("data", [{}])[0].get("embedding", [])
        return tuple(float(x) for x in v)

    raise RuntimeError(f"unknown embedding provider: {provider}")


def embed_with_retry(provider: str, model: str, text: str) -> List[float]:
    waits = [1, 2, 4]
    for i in range(4):
        try:
            return list(_embed_cached(provider, model, text))
        except Exception:
            if i >= 3:
                raise
            time.sleep(waits[i])
    raise RuntimeError("embed failed")


def cosine(a: List[float], b: List[float]) -> float:
    if not a or not b or len(a) != len(b):
        return -1.0
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0 or nb == 0:
        return -1.0
    return dot / (na * nb)


def blob_from_vector(v: List[float]) -> bytes:
    return json.dumps(v).encode("utf-8")


def vector_from_blob(b: bytes) -> List[float]:
    try:
        return [float(x) for x in json.loads((b or b"[]").decode("utf-8"))]
    except Exception:
        return []


def upsert_source(conn: sqlite3.Connection, src: Extracted, raw_url: str, tags: List[str]) -> Tuple[int, bool]:
    nurl = normalize_url(src.canonical_url)
    h = sha256_text(src.content)

    row = conn.execute("SELECT id FROM sources WHERE content_hash=?", (h,)).fetchone()
    if row:
        return int(row[0]), False

    row = conn.execute("SELECT id FROM sources WHERE normalized_url=?", (nurl,)).fetchone()
    if row:
        return int(row[0]), False

    cur = conn.execute(
        """
        INSERT INTO sources(url, normalized_url, title, source_type, summary, raw_content, content_hash, tags, updated_at)
        VALUES(?,?,?,?,?,?,?,?,CURRENT_TIMESTAMP)
        """,
        (
            raw_url,
            nurl,
            src.title[:400],
            src.source_type,
            src.content[:600],
            src.content,
            h,
            json.dumps(tags),
        ),
    )
    conn.commit()
    return int(cur.lastrowid), True


def ingest(input_value: str, tags: List[str], cfg: Dict[str, Any], force: bool = False) -> Dict[str, Any]:
    st = detect_source_type(input_value)
    raw_url = input_value

    if st == "tweet":
        title, content = extract_tweet(input_value)
        canonical = normalize_url(input_value)
    elif st == "video":
        title, content = extract_youtube(input_value)
        canonical = normalize_url(input_value)
    elif st == "pdf":
        title, content = extract_pdf(input_value)
        canonical = normalize_url(input_value) if input_value.startswith("http") else str(Path(input_value).resolve())
    elif st in {"article", "other"} and input_value.startswith("http"):
        title, content = extract_article(input_value)
        canonical = normalize_url(input_value)
        if st == "other":
            st = "article"
    else:
        title, content = extract_text(input_value)
        canonical = str(Path(input_value).resolve())
        st = "text"

    ok, reason, content = validate_content(st, content, cfg, strict=not force)
    if not ok:
        return {"ok": False, "reason": reason, "source_type": st}

    ex = Extracted(title=title, content=content, source_type=st, canonical_url=canonical)

    conn = db()
    init_schema(conn)
    source_id, created = upsert_source(conn, ex, raw_url, tags)
    if not created:
        return {"ok": True, "created": False, "source_id": source_id, "deduped": True}

    chunks = sentence_chunks(content, int(cfg["chunk_size"]), int(cfg["chunk_overlap"]), int(cfg["min_chunk_size"]))

    provider = cfg.get("embedding_provider", "gemini")
    model = cfg.get("embedding_model_gemini") if provider == "gemini" else cfg.get("embedding_model_openai")

    for i in range(0, len(chunks), int(cfg["batch_size"])):
        batch = chunks[i : i + int(cfg["batch_size"])]
        for j, ch in enumerate(batch):
            vec = embed_with_retry(provider, model, ch)
            conn.execute(
                """
                INSERT INTO chunks(source_id, chunk_index, content, embedding, embedding_dim, embedding_provider, embedding_model)
                VALUES(?,?,?,?,?,?,?)
                """,
                (source_id, i + j, ch, blob_from_vector(vec), len(vec), provider, model),
            )
        conn.commit()
        time.sleep(int(cfg["batch_delay_ms"]) / 1000.0)

    return {
        "ok": True,
        "created": True,
        "source_id": source_id,
        "source_type": st,
        "title": title,
        "chunks": len(chunks),
    }


def answer_with_context(question: str, contexts: List[Dict[str, Any]], cfg: Optional[Dict[str, Any]] = None) -> str:
    ctx_text = "\n\n".join(
        f"[Source {i+1}] title={c['title']} url={c['url']}\n{c['excerpt']}"
        for i, c in enumerate(contexts)
    )
    prompt = (
        "Answer using only the provided context. Cite which source numbers you used. "
        "If insufficient context, say so.\n\n"
        f"Question: {question}\n\nContext:\n{ctx_text}"
    )

    if requests is None:
        return "requests unavailable; cannot run LLM answer."

    cfg = cfg or {}
    synthesis_provider = str(cfg.get("synthesis_provider", "auto")).lower().strip()
    if synthesis_provider == "none":
        return "Synthesis disabled by config (synthesis_provider=none)."

    gemini_model = str(cfg.get("synthesis_model_gemini", "models/gemini-flash-latest")).strip()
    openai_model = str(cfg.get("synthesis_model_openai", "gpt-4o-mini")).strip()

    providers: List[str]
    if synthesis_provider in {"gemini", "openai"}:
        providers = [synthesis_provider]
    else:
        providers = ["gemini", "openai"]

    errors: List[str] = []

    for provider in providers:
        if provider == "gemini":
            gkey = os.getenv("GEMINI_API_KEY", "").strip()
            if not gkey:
                errors.append("gemini key missing")
                continue
            url = f"https://generativelanguage.googleapis.com/v1beta/{gemini_model}:generateContent?key={gkey}"
            r = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=40)
            if r.ok:
                return (
                    r.json()
                    .get("candidates", [{}])[0]
                    .get("content", {})
                    .get("parts", [{}])[0]
                    .get("text", "")
                    .strip()
                )
            errors.append(f"gemini http {r.status_code}: {r.text[:160]}")

        if provider == "openai":
            okey = os.getenv("OPENAI_API_KEY", "").strip()
            if not okey:
                errors.append("openai key missing")
                continue
            r = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {okey}", "Content-Type": "application/json"},
                json={
                    "model": openai_model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.1,
                },
                timeout=40,
            )
            if r.ok:
                return r.json().get("choices", [{}])[0].get("message", {}).get("content", "").strip()
            errors.append(f"openai http {r.status_code}: {r.text[:160]}")

    return "Synthesis unavailable. " + " | ".join(errors[:3])


def query(question: str, cfg: Dict[str, Any], top_k: Optional[int] = None) -> Dict[str, Any]:
    conn = db()
    init_schema(conn)
    k = int(top_k or cfg.get("retrieval_top_k", 10))

    provider = cfg.get("embedding_provider", "gemini")
    model = cfg.get("embedding_model_gemini") if provider == "gemini" else cfg.get("embedding_model_openai")
    qvec = embed_with_retry(provider, model, question)

    rows = conn.execute(
        """
        SELECT c.id, c.source_id, c.content, c.embedding, s.title, s.url
        FROM chunks c
        JOIN sources s ON s.id=c.source_id
        WHERE c.embedding IS NOT NULL
        """
    ).fetchall()

    scored: List[Tuple[float, Dict[str, Any]]] = []
    for _id, sid, content, emb, title, url in rows:
        vec = vector_from_blob(emb)
        sim = cosine(qvec, vec)
        scored.append(
            (
                sim,
                {
                    "chunk_id": _id,
                    "source_id": sid,
                    "title": title,
                    "url": url,
                    "excerpt": (content or "")[:2500],
                },
            )
        )

    scored.sort(key=lambda x: x[0], reverse=True)

    # top-k then dedupe best chunk per source
    best_by_source: Dict[int, Tuple[float, Dict[str, Any]]] = {}
    for sim, item in scored:
        sid = int(item["source_id"])
        if sid not in best_by_source:
            best_by_source[sid] = (sim, item)
        if len(best_by_source) >= k:
            break

    contexts = [v[1] for v in sorted(best_by_source.values(), key=lambda x: x[0], reverse=True)[:k]]
    answer = answer_with_context(question, contexts, cfg)
    return {"answer": answer, "contexts": contexts}


def main() -> int:
    ap = argparse.ArgumentParser(description="Personal Knowledge Base RAG")
    sub = ap.add_subparsers(dest="cmd")

    sub.add_parser("init")

    p_ing = sub.add_parser("ingest")
    p_ing.add_argument("input", help="URL or file path")
    p_ing.add_argument("--tags", default="", help="comma separated tags")
    p_ing.add_argument("--force", action="store_true", help="bypass strict quality/error-page validators for trusted inputs")

    p_q = sub.add_parser("query")
    p_q.add_argument("question")
    p_q.add_argument("--top-k", type=int, default=10)

    args = ap.parse_args()
    cfg = load_cfg()

    if args.cmd == "init":
        conn = db()
        init_schema(conn)
        print(json.dumps({"ok": True, "db": str(DB_PATH), "cfg": str(CFG_PATH)}))
        return 0

    if args.cmd == "ingest":
        tags = [t.strip() for t in str(args.tags).split(",") if t.strip()]
        with ingestion_lock():
            result = ingest(args.input, tags, cfg, force=bool(args.force))
        print(json.dumps(result, indent=2))
        return 0 if result.get("ok") else 1

    if args.cmd == "query":
        result = query(args.question, cfg, args.top_k)
        print(json.dumps(result, indent=2))
        return 0

    ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
