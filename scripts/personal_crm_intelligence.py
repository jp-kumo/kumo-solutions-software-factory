#!/usr/bin/env python3
"""
Personal CRM Intelligence (server source-of-truth)

Implements:
- 2-stage filtering (hard rules + AI/heuristic classifier)
- contact scoring
- dedupe/merge
- SQLite storage (WAL + FK)
- daily run summary

Input adapters:
- JSON exports for email/calendar (works now)
- optional custom CLI commands for live ingestion

Usage:
  python3 scripts/personal_crm_intelligence.py --run

Config:
  configs/personal_crm_learning.json
"""
from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import json
import os
import re
import sqlite3
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import requests
except Exception:  # optional
    requests = None

WORKSPACE = Path("/home/jpadmin/.openclaw/workspace")
CFG_PATH = WORKSPACE / "configs" / "personal_crm_learning.json"
DB_PATH = WORKSPACE / "data" / "personal_crm.sqlite"
RPT_DIR = WORKSPACE / "data" / "reports"


DEFAULT_CFG = {
    "my_emails": ["jacquespayne.9914@gmail.com"],
    "my_domains": ["gmail.com"],
    "excluded_contacts": [],
    "skip_domains": [],
    "allow_emails": [],
    "allow_domains": [],
    "skip_keywords": [
        "weekly roundup",
        "monthly update",
        "newsletter",
        "digest",
        "feature announcement",
        "product launch",
    ],
    "prefer_titles": [
        "ceo",
        "founder",
        "vp",
        "head of",
        "engineer",
        "partner",
        "director",
    ],
    "min_exchanges": 1,
    "max_days_between": 60,
    "max_attendees": 10,
    "min_duration_minutes": 15,
    "email_days": 60,
    "calendar_days": 60,
    "account": "jacquespayne.9914@gmail.com",
    "email_json_path": "",
    "calendar_json_path": "",
    "email_command": "",
    "calendar_command": "",
    "notify_command": "",
    "shadow_mode": True,
    "max_new_contacts_per_run": 50,
    "max_rejections_per_run": 250,
    "domain_rejection_threshold": 3,
}

ROLE_PREFIXES = ("info@", "team@", "partnerships@", "collabs@", "noreply@")
MARKETING_PREFIXES = ("noreply@", "tx.", "cx.", "mail.", "email.")


@dataclasses.dataclass
class Candidate:
    name: str
    email: str
    subjects: List[str]
    snippets: List[str]
    total_messages: int
    thread_count: int
    meetings: int = 0
    last_touch: Optional[str] = None
    title: str = ""
    company: str = ""
    source_email: bool = False
    source_calendar: bool = False
    inbound_messages: int = 0
    outbound_messages: int = 0

    @property
    def exchanges(self) -> int:
        return min(self.total_messages // 2, self.thread_count)


def ensure_dirs() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    RPT_DIR.mkdir(parents=True, exist_ok=True)
    CFG_PATH.parent.mkdir(parents=True, exist_ok=True)


def load_cfg() -> Dict[str, Any]:
    ensure_dirs()
    if not CFG_PATH.exists():
        CFG_PATH.write_text(json.dumps(DEFAULT_CFG, indent=2) + "\n", encoding="utf-8")
        return dict(DEFAULT_CFG)
    cfg = json.loads(CFG_PATH.read_text(encoding="utf-8"))
    merged = dict(DEFAULT_CFG)
    merged.update(cfg)
    return merged


def save_cfg(cfg: Dict[str, Any]) -> None:
    CFG_PATH.write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")


def db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys=ON;")
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    return conn


def init_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS contacts (
          id INTEGER PRIMARY KEY,
          name TEXT,
          email TEXT UNIQUE,
          company TEXT,
          title TEXT,
          score INTEGER,
          source_email INTEGER DEFAULT 0,
          source_calendar INTEGER DEFAULT 0,
          exchanges INTEGER DEFAULT 0,
          meetings INTEGER DEFAULT 0,
          last_touch TEXT,
          tags TEXT DEFAULT '',
          created_at TEXT DEFAULT CURRENT_TIMESTAMP,
          updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS interactions (
          id INTEGER PRIMARY KEY,
          contact_id INTEGER NOT NULL,
          source TEXT NOT NULL,
          event_date TEXT,
          subject TEXT,
          snippet TEXT,
          metadata_json TEXT,
          created_at TEXT DEFAULT CURRENT_TIMESTAMP,
          FOREIGN KEY(contact_id) REFERENCES contacts(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS rejections (
          id INTEGER PRIMARY KEY,
          name TEXT,
          email TEXT,
          reason TEXT,
          stage TEXT,
          created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS contact_embeddings (
          contact_id INTEGER PRIMARY KEY,
          text_blob TEXT,
          vector_json TEXT,
          updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
          FOREIGN KEY(contact_id) REFERENCES contacts(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS runs (
          id INTEGER PRIMARY KEY,
          run_at TEXT,
          new_contacts INTEGER,
          merges INTEGER,
          rejected INTEGER,
          issues INTEGER,
          summary_json TEXT
        );

        CREATE VIEW IF NOT EXISTS v_stale_contacts_30d AS
        SELECT * FROM contacts
        WHERE last_touch IS NOT NULL
          AND julianday('now') - julianday(last_touch) >= 30;

        CREATE VIEW IF NOT EXISTS v_cross_signal_contacts AS
        SELECT * FROM contacts
        WHERE source_email = 1 AND source_calendar = 1;

        CREATE VIEW IF NOT EXISTS v_recent_high_score AS
        SELECT * FROM contacts
        WHERE score >= 80
          AND last_touch IS NOT NULL
          AND julianday('now') - julianday(last_touch) <= 30
        ORDER BY score DESC, last_touch DESC;
        """
    )
    conn.commit()


def norm_email(email: str) -> str:
    return (email or "").strip().lower()


def parse_email_addr(raw: str) -> Tuple[str, str]:
    raw = raw or ""
    m = re.search(r"<([^>]+)>", raw)
    if m:
        email = norm_email(m.group(1))
        name = raw.replace(m.group(0), "").strip().strip('"')
    else:
        email = norm_email(raw)
        name = ""
    if "@" in email and not name:
        name = email.split("@")[0].replace(".", " ").title()
    return name.strip(), email


def maybe_learn_skip_domain(cfg: Dict[str, Any], conn: sqlite3.Connection, email: str) -> None:
    e = norm_email(email)
    if "@" not in e:
        return
    dom = e.split("@", 1)[1]
    threshold = int(cfg.get("domain_rejection_threshold", 3))
    if threshold <= 1:
        if dom not in cfg.get("skip_domains", []):
            cfg.setdefault("skip_domains", []).append(dom)
        return
    row = conn.execute(
        "SELECT COUNT(DISTINCT email) FROM rejections WHERE email LIKE ?",
        (f"%@{dom}",),
    ).fetchone()
    n = int(row[0]) if row and row[0] is not None else 0
    if n >= threshold and dom not in cfg.get("skip_domains", []):
        cfg.setdefault("skip_domains", []).append(dom)


def hard_filter(c: Candidate, cfg: Dict[str, Any], conn: sqlite3.Connection) -> Optional[str]:
    e = norm_email(c.email)
    if not e or "@" not in e:
        return "invalid_email"
    domain = e.split("@", 1)[1]

    allow_emails = [norm_email(x) for x in cfg.get("allow_emails", [])]
    allow_domains = [d.lower() for d in cfg.get("allow_domains", [])]
    if e in allow_emails or domain in allow_domains:
        return None

    if e in [norm_email(x) for x in cfg.get("my_emails", [])]:
        return "own_email"
    if domain in [d.lower() for d in cfg.get("my_domains", [])]:
        # allow external gmail users; only block exact own_email by address
        pass
    if e in [norm_email(x) for x in cfg.get("excluded_contacts", [])]:
        return "excluded_contact"
    if domain in [d.lower() for d in cfg.get("skip_domains", [])]:
        return "skip_domain"

    cur = conn.execute("SELECT 1 FROM contacts WHERE email=?", (e,)).fetchone()
    if cur:
        return "already_contact"
    cur = conn.execute("SELECT 1 FROM rejections WHERE email=?", (e,)).fetchone()
    if cur:
        return "previously_rejected"

    if any(e.startswith(p) for p in ROLE_PREFIXES):
        return "role_inbox"
    if any(e.startswith(p) for p in MARKETING_PREFIXES):
        return "marketing_prefix"

    return None


def ai_classify(c: Candidate, cfg: Dict[str, Any]) -> Tuple[bool, str, float]:
    # Fast heuristic fallback (always available)
    subj = " | ".join([s.lower() for s in c.subjects[:8]])
    snip = " | ".join([s.lower() for s in c.snippets[:8]])
    text = f"{subj} {snip}".strip()

    if any(k in text for k in [x.lower() for x in cfg.get("skip_keywords", [])]):
        return False, "newsletter_or_digest_pattern", 0.95

    if c.exchanges < int(cfg.get("min_exchanges", 1)):
        return False, "low_exchange_count", 0.85

    total_dir = c.inbound_messages + c.outbound_messages
    if total_dir > 0:
        reply_ratio = min(c.inbound_messages, c.outbound_messages) / max(total_dir, 1)
        # Very one-way + low exchanges is usually cold outreach/automation
        if c.exchanges <= 1 and reply_ratio < 0.2:
            return False, "one_way_low_engagement", 0.9

    # Optional Gemini Flash call
    gemini = os.getenv("GEMINI_API_KEY", "").strip()
    if gemini and requests is not None:
        try:
            prompt = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": (
                                    "Classify contact as APPROVE or REJECT for personal CRM. "
                                    "Return strict JSON with keys: decision, reason, confidence. "
                                    "Rules: reject automation/newsletters/cold one-way outreach; "
                                    "approve real person with meaningful two-way interaction.\n\n"
                                    f"name={c.name}\nemail={c.email}\nexchanges={c.exchanges}\n"
                                    f"total_messages={c.total_messages}\nthread_count={c.thread_count}\n"
                                    f"inbound_messages={c.inbound_messages}\noutbound_messages={c.outbound_messages}\n"
                                    f"subjects={c.subjects[:8]}\nsnippets={c.snippets[:8]}"
                                )
                            }
                        ]
                    }
                ]
            }
            url = (
                "https://generativelanguage.googleapis.com/v1beta/models/"
                "gemini-1.5-flash:generateContent?key="
                + gemini
            )
            r = requests.post(url, json=prompt, timeout=20)
            r.raise_for_status()
            data = r.json()
            txt = (
                data.get("candidates", [{}])[0]
                .get("content", {})
                .get("parts", [{}])[0]
                .get("text", "")
            )
            j = json.loads(re.search(r"\{[\s\S]*\}", txt).group(0))
            decision = str(j.get("decision", "REJECT")).upper().strip()
            reason = str(j.get("reason", "llm_reject"))
            confidence = float(j.get("confidence", 0.5))
            return decision == "APPROVE", reason, confidence
        except Exception:
            pass

    return True, "heuristic_approve", 0.7


def contact_score(c: Candidate, cfg: Dict[str, Any]) -> int:
    score = 50
    score += min(c.exchanges * 5, 20)
    score += min(c.meetings * 3, 15)

    t = (c.title or "").lower()
    if any(x in t for x in [p.lower() for p in cfg.get("prefer_titles", [])]):
        score += 15

    if c.meetings > 0:
        score += 10

    if c.last_touch:
        try:
            d = dt.datetime.fromisoformat(c.last_touch.replace("Z", "+00:00"))
            age = (dt.datetime.now(dt.timezone.utc) - d).days
            if age <= 7:
                score += 10
            elif age <= 30:
                score += 5
        except Exception:
            pass

    if c.source_email and c.source_calendar:
        score += 25
    if c.title:
        score += 10
    if c.company:
        score += 5

    return score


def dedupe_lookup(conn: sqlite3.Connection, c: Candidate) -> Optional[int]:
    row = conn.execute("SELECT id FROM contacts WHERE email=?", (norm_email(c.email),)).fetchone()
    if row:
        return int(row[0])
    if c.name and c.company:
        row = conn.execute(
            "SELECT id FROM contacts WHERE lower(name)=lower(?) AND lower(company)=lower(?)",
            (c.name, c.company),
        ).fetchone()
        if row:
            return int(row[0])
    return None


def upsert_contact(conn: sqlite3.Connection, c: Candidate, score: int) -> Tuple[int, bool]:
    contact_id = dedupe_lookup(conn, c)
    if contact_id is None:
        cur = conn.execute(
            """
            INSERT INTO contacts(name,email,company,title,score,source_email,source_calendar,exchanges,meetings,last_touch,updated_at)
            VALUES(?,?,?,?,?,?,?,?,?,?,CURRENT_TIMESTAMP)
            """,
            (
                c.name,
                norm_email(c.email),
                c.company,
                c.title,
                score,
                1 if c.source_email else 0,
                1 if c.source_calendar else 0,
                c.exchanges,
                c.meetings,
                c.last_touch,
            ),
        )
        conn.commit()
        return int(cur.lastrowid), True

    conn.execute(
        """
        UPDATE contacts
        SET name=COALESCE(NULLIF(?,''),name),
            company=COALESCE(NULLIF(?,''),company),
            title=COALESCE(NULLIF(?,''),title),
            score=?,
            source_email=MAX(source_email,?),
            source_calendar=MAX(source_calendar,?),
            exchanges=MAX(exchanges,?),
            meetings=MAX(meetings,?),
            last_touch=CASE WHEN last_touch IS NULL THEN ? WHEN ? > last_touch THEN ? ELSE last_touch END,
            updated_at=CURRENT_TIMESTAMP
        WHERE id=?
        """,
        (
            c.name,
            c.company,
            c.title,
            score,
            1 if c.source_email else 0,
            1 if c.source_calendar else 0,
            c.exchanges,
            c.meetings,
            c.last_touch,
            c.last_touch,
            c.last_touch,
            contact_id,
        ),
    )
    conn.commit()
    return contact_id, False


def insert_interaction(conn: sqlite3.Connection, contact_id: int, source: str, date: str, subject: str, snippet: str, meta: Dict[str, Any]) -> None:
    conn.execute(
        """
        INSERT INTO interactions(contact_id,source,event_date,subject,snippet,metadata_json)
        VALUES(?,?,?,?,?,?)
        """,
        (contact_id, source, date, subject, snippet, json.dumps(meta)),
    )


def insert_embedding_stub(conn: sqlite3.Connection, contact_id: int, c: Candidate) -> None:
    blob = (
        f"name: {c.name}\nemail: {c.email}\ncompany: {c.company}\ntitle: {c.title}\n"
        f"exchanges: {c.exchanges}\nmeetings: {c.meetings}\nlast_touch: {c.last_touch}\n"
    )
    conn.execute(
        """
        INSERT INTO contact_embeddings(contact_id,text_blob,vector_json,updated_at)
        VALUES(?,?,?,CURRENT_TIMESTAMP)
        ON CONFLICT(contact_id) DO UPDATE SET text_blob=excluded.text_blob, updated_at=CURRENT_TIMESTAMP
        """,
        (contact_id, blob, ""),
    )


def load_json_records(path: str) -> List[Dict[str, Any]]:
    if not path:
        return []
    p = Path(path)
    if not p.exists():
        return []
    data = json.loads(p.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        for k in ("messages", "emails", "events", "items", "data"):
            if k in data and isinstance(data[k], list):
                return data[k]
    return data if isinstance(data, list) else []


def load_command_records(cmd: str) -> List[Dict[str, Any]]:
    if not cmd.strip():
        return []
    p = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    if p.returncode != 0:
        err = (p.stderr or p.stdout or "command failed").strip()
        raise RuntimeError(err)
    out = p.stdout
    data = json.loads(out)
    if isinstance(data, dict):
        for k in ("messages", "emails", "events", "items", "data"):
            if k in data and isinstance(data[k], list):
                return data[k]
    return data if isinstance(data, list) else []


def build_email_candidates(records: List[Dict[str, Any]], cfg: Dict[str, Any]) -> Dict[str, Candidate]:
    by_email: Dict[str, Candidate] = {}
    thread_sets: Dict[str, set] = defaultdict(set)
    my_emails = {norm_email(x) for x in cfg.get("my_emails", [])}

    for r in records:
        subject = str(r.get("subject", ""))
        snippet = str(r.get("snippet", ""))
        date = str(r.get("date", r.get("internalDate", "")))
        thread = str(r.get("thread_id", r.get("threadId", "")))

        participants = []
        for f in ("from", "to", "cc", "bcc", "sender", "recipient"):
            v = r.get(f)
            if isinstance(v, str):
                participants.extend([x.strip() for x in v.split(",") if x.strip()])
            elif isinstance(v, list):
                participants.extend([str(x).strip() for x in v if str(x).strip()])

        from_name, from_email = parse_email_addr(str(r.get("from", r.get("sender", ""))))
        from_is_me = from_email in my_emails

        for raw in participants:
            name, email = parse_email_addr(raw)
            if not email or email in my_emails:
                continue
            c = by_email.get(email)
            if not c:
                c = Candidate(
                    name=name,
                    email=email,
                    subjects=[],
                    snippets=[],
                    total_messages=0,
                    thread_count=0,
                    source_email=True,
                    last_touch=date,
                )
                by_email[email] = c
            c.total_messages += 1
            c.subjects.append(subject)
            c.snippets.append(snippet)
            if from_is_me:
                c.outbound_messages += 1
            else:
                c.inbound_messages += 1
            if thread:
                thread_sets[email].add(thread)
                c.thread_count = len(thread_sets[email])
            if date and (not c.last_touch or date > c.last_touch):
                c.last_touch = date

    return by_email


def build_calendar_candidates(records: List[Dict[str, Any]], cfg: Dict[str, Any]) -> Dict[str, Candidate]:
    by_email: Dict[str, Candidate] = {}
    max_attendees = int(cfg.get("max_attendees", 10))
    min_duration = int(cfg.get("min_duration_minutes", 15))
    my_emails = {norm_email(x) for x in cfg.get("my_emails", [])}

    for r in records:
        attendees = r.get("attendees", [])
        if not isinstance(attendees, list):
            attendees = []
        if not (1 <= len(attendees) <= max_attendees):
            continue

        start = r.get("start") or r.get("start_time")
        end = r.get("end") or r.get("end_time")
        duration = r.get("duration_minutes")
        if duration is None:
            try:
                s = dt.datetime.fromisoformat(str(start).replace("Z", "+00:00"))
                e = dt.datetime.fromisoformat(str(end).replace("Z", "+00:00"))
                duration = int((e - s).total_seconds() // 60)
            except Exception:
                duration = 0
        if int(duration or 0) < min_duration:
            continue

        title = str(r.get("title", r.get("summary", "")))
        for a in attendees:
            if isinstance(a, dict):
                email = norm_email(a.get("email", ""))
                name = str(a.get("name", "")).strip()
            else:
                name, email = parse_email_addr(str(a))
            if not email or email in my_emails:
                continue
            c = by_email.get(email)
            if not c:
                c = Candidate(
                    name=name,
                    email=email,
                    subjects=[],
                    snippets=[],
                    total_messages=0,
                    thread_count=0,
                    source_calendar=True,
                    last_touch=str(start or ""),
                )
                by_email[email] = c
            c.meetings += 1
            c.subjects.append(title)
            c.snippets.append(f"Meeting: {title}")
            c.source_calendar = True
            if start and (not c.last_touch or str(start) > str(c.last_touch)):
                c.last_touch = str(start)

    return by_email


def merge_candidates(a: Dict[str, Candidate], b: Dict[str, Candidate]) -> Dict[str, Candidate]:
    out = dict(a)
    for e, c in b.items():
        if e not in out:
            out[e] = c
            continue
        x = out[e]
        x.subjects.extend(c.subjects)
        x.snippets.extend(c.snippets)
        x.total_messages += c.total_messages
        x.thread_count += c.thread_count
        x.meetings += c.meetings
        x.source_email = x.source_email or c.source_email
        x.source_calendar = x.source_calendar or c.source_calendar
        x.inbound_messages += c.inbound_messages
        x.outbound_messages += c.outbound_messages
        if c.last_touch and (not x.last_touch or c.last_touch > x.last_touch):
            x.last_touch = c.last_touch
        if not x.name and c.name:
            x.name = c.name
    return out


def maybe_notify(cfg: Dict[str, Any], msg: str) -> None:
    cmd = (cfg.get("notify_command") or "").strip()
    if not cmd:
        return
    try:
        subprocess.run(cmd.format(summary=msg.replace("\n", " ")), shell=True, check=False)
    except Exception:
        pass


def preflight_auth_checks(cfg: Dict[str, Any]) -> List[str]:
    account = str(cfg.get("account") or "jacquespayne.9914@gmail.com")
    client = os.getenv("GOG_CLIENT", "default")
    checks = [
        [
            "gog",
            "gmail",
            "search",
            "newer_than:1d",
            "--account",
            account,
            "--client",
            client,
            "--max",
            "1",
            "--json",
            "--no-input",
        ],
        [
            "gog",
            "calendar",
            "events",
            "primary",
            "--account",
            account,
            "--client",
            client,
            "--from",
            dt.datetime.now(dt.timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0).isoformat().replace("+00:00", "Z"),
            "--to",
            (dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0).isoformat().replace("+00:00", "Z"),
            "--max",
            "1",
            "--json",
            "--no-input",
        ],
    ]

    problems: List[str] = []
    for cmd in checks:
        p = subprocess.run(cmd, text=True, capture_output=True)
        if p.returncode != 0:
            err = (p.stderr or p.stdout or "auth check failed").strip().splitlines()[-1]
            if "aes.KeyUnwrap" in (p.stderr or "") + (p.stdout or ""):
                problems.append(
                    "google_token_decrypt_failed: keyring mismatch/corrupt token; run gog auth remove+add with --client default in pinned HOME/XDG context"
                )
            else:
                problems.append(f"auth_preflight_failed: {' '.join(cmd[:4])} :: {err}")
    return problems


def run_ingest() -> int:
    cfg = load_cfg()
    conn = db()
    init_schema(conn)

    issues = 0
    issue_notes: List[str] = []

    # Preflight auth checks to fail fast with actionable errors.
    preflight_problems = preflight_auth_checks(cfg)
    if preflight_problems:
        issues += len(preflight_problems)
        issue_notes.extend(preflight_problems)

    # Data ingestion source order: command first (live), then json fallback
    emails = []
    cals = []

    try:
        emails = load_command_records(cfg.get("email_command", ""))
    except Exception as e:
        issues += 1
        issue_notes.append(f"email_fetch_failed: {str(e)[:220]}")
    if not emails:
        emails = load_json_records(cfg.get("email_json_path", ""))

    try:
        cals = load_command_records(cfg.get("calendar_command", ""))
    except Exception as e:
        issues += 1
        issue_notes.append(f"calendar_fetch_failed: {str(e)[:220]}")
    if not cals:
        cals = load_json_records(cfg.get("calendar_json_path", ""))

    em = build_email_candidates(emails, cfg)
    ca = build_calendar_candidates(cals, cfg)
    candidates = merge_candidates(em, ca)

    new_contacts = 0
    merges = 0
    rejected = 0
    shadow_approved = 0
    shadow_mode = bool(cfg.get("shadow_mode", True))

    for c in candidates.values():
        reason = hard_filter(c, cfg, conn)
        if reason:
            conn.execute(
                "INSERT INTO rejections(name,email,reason,stage) VALUES(?,?,?,?)",
                (c.name, norm_email(c.email), reason, "hard"),
            )
            rejected += 1
            maybe_learn_skip_domain(cfg, conn, c.email)
            continue

        ok, ai_reason, _conf = ai_classify(c, cfg)
        if not ok:
            conn.execute(
                "INSERT INTO rejections(name,email,reason,stage) VALUES(?,?,?,?)",
                (c.name, norm_email(c.email), ai_reason, "ai"),
            )
            rejected += 1
            maybe_learn_skip_domain(cfg, conn, c.email)
            continue

        score = contact_score(c, cfg)
        if shadow_mode:
            shadow_approved += 1
            continue

        contact_id, created = upsert_contact(conn, c, score)
        if created:
            new_contacts += 1
        else:
            merges += 1

        # Minimal interaction log rows
        insert_interaction(
            conn,
            contact_id,
            "email_calendar",
            c.last_touch or "",
            c.subjects[0] if c.subjects else "",
            c.snippets[0] if c.snippets else "",
            {"exchanges": c.exchanges, "meetings": c.meetings, "inbound": c.inbound_messages, "outbound": c.outbound_messages},
        )
        insert_embedding_stub(conn, contact_id, c)

    anomaly = False
    if not shadow_mode:
        if new_contacts > int(cfg.get("max_new_contacts_per_run", 50)):
            issues += 1
            anomaly = True
        if rejected > int(cfg.get("max_rejections_per_run", 250)):
            issues += 1
            anomaly = True

    summary = {
        "run_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "candidates": len(candidates),
        "new_contacts": new_contacts,
        "merges": merges,
        "rejected": rejected,
        "issues": issues,
        "issue_notes": issue_notes[:10],
        "shadow_mode": shadow_mode,
        "shadow_approved": shadow_approved,
        "anomaly": anomaly,
    }

    conn.execute(
        "INSERT INTO runs(run_at,new_contacts,merges,rejected,issues,summary_json) VALUES(?,?,?,?,?,?)",
        (
            summary["run_at"],
            new_contacts,
            merges,
            rejected,
            issues,
            json.dumps(summary),
        ),
    )
    conn.commit()
    if not anomaly:
        save_cfg(cfg)

    rpt = RPT_DIR / f"personal_crm_run_{dt.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    rpt.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    msg = (
        "Personal CRM ingestion complete\n"
        f"- candidates: {summary['candidates']}\n"
        f"- shadow_mode: {shadow_mode}\n"
        f"- shadow_approved: {shadow_approved}\n"
        f"- new: {new_contacts}\n"
        f"- merges: {merges}\n"
        f"- rejected: {rejected}\n"
        f"- anomaly: {anomaly}\n"
        f"- issues: {issues}\n"
        f"- report: {rpt}"
    )
    if issue_notes:
        msg += f"\n- issue_note: {issue_notes[0]}"
    print(msg)
    maybe_notify(cfg, msg)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true", help="execute ingestion run")
    ap.add_argument("--init", action="store_true", help="initialize config + schema")
    args = ap.parse_args()

    ensure_dirs()
    cfg = load_cfg()
    conn = db()
    init_schema(conn)

    if args.init:
        print(f"Initialized config: {CFG_PATH}")
        print(f"Initialized db: {DB_PATH}")
        return 0

    if args.run:
        return run_ingest()

    ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
