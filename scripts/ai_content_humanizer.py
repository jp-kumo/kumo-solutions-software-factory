#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

AI_TELLS = [
    "delve",
    "landscape",
    "leverage",
    "it's important to note",
    "in conclusion",
    "game-changing",
    "revolutionary",
    "transformative",
]

REPLACEMENTS = {
    r"\bdelve\b": "dig into",
    r"\blandscape\b": "space",
    r"\bleverage\b": "use",
    r"\bit'?s important to note\b": "",
    r"\bin conclusion\b": "",
    r"\bgame-?changing\b": "useful",
    r"\brevolutionary\b": "new",
    r"\btransformative\b": "practical",
    r"\bit'?s worth noting that perhaps\b": "",
    r"\bperhaps\b": "",
    r"\bvery\b": "",
    r"\breally\b": "",
}


@dataclass
class HumanizeResult:
    revised: str
    changes: List[str]
    detected: List[str]


def split_sentences(text: str) -> List[str]:
    s = re.split(r"(?<=[.!?])\s+", text.strip())
    return [x.strip() for x in s if x.strip()]


def detect(text: str) -> List[str]:
    found: List[str] = []
    low = text.lower()

    for phrase in AI_TELLS:
        if phrase in low:
            found.append(f"AI tell phrase: '{phrase}'")

    starters = []
    for s in split_sentences(text):
        starters.append((s.split()[:2] or [""])[0].lower())
    if starters:
        same_start_ratio = max(starters.count(x) for x in set(starters)) / len(starters)
        if same_start_ratio > 0.4:
            found.append("Repetitive sentence starts")

    if re.search(r"\b(it might|perhaps|it seems|could potentially)\b", low):
        found.append("Excessive hedging")

    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    if len(paragraphs) >= 3:
        lens = [len(p) for p in paragraphs]
        if max(lens) - min(lens) < 40:
            found.append("Uniform paragraph rhythm")

    if re.search(r"\n\s*[-*]\s+[^\n]+\n\s*[-*]\s+[^\n]+\n\s*[-*]\s+[^\n]+", text):
        found.append("Generated-feeling parallel list structure")

    return found


def rewrite_base(text: str) -> Tuple[str, List[str]]:
    changes: List[str] = []
    out = text

    for pat, repl in REPLACEMENTS.items():
        new = re.sub(pat, repl, out, flags=re.I)
        if new != out:
            changes.append(f"Replaced pattern: {pat} -> '{repl}'")
            out = new

    # Remove filler lead-ins
    out2 = re.sub(r"\b(Additionally|Moreover|Furthermore),\s*", "", out, flags=re.I)
    if out2 != out:
        changes.append("Removed formal filler transitions")
        out = out2

    # tighten spaces/punctuation
    out = re.sub(r"\s{2,}", " ", out)
    out = re.sub(r"\s+([,.;!?])", r"\1", out)

    # vary cadence: make every third sentence shorter if long
    sents = split_sentences(out)
    for i, s in enumerate(sents):
        if i % 3 == 2 and len(s.split()) > 16:
            chunk = re.split(r",|;", s)
            if chunk and len(chunk[0].split()) >= 4:
                sents[i] = chunk[0].strip() + "."
                changes.append("Varied cadence by shortening one long sentence")

    out = " ".join(sents)

    # contractions and informal natural phrasing
    contractions = {
        r"\bdo not\b": "don't",
        r"\bcan not\b": "can't",
        r"\bit is\b": "it's",
        r"\bwe are\b": "we're",
        r"\byou are\b": "you're",
    }
    for pat, repl in contractions.items():
        new = re.sub(pat, repl, out, flags=re.I)
        if new != out:
            changes.append(f"Applied contraction: {pat} -> {repl}")
            out = new

    # clean awkward leftovers after removals
    out = re.sub(r"(^|[.!?]\s+)that\s+", r"\1", out, flags=re.I)
    out = re.sub(r",\s*,", ",", out)
    out = re.sub(r",\s*\.", ".", out)
    out = re.sub(r"\.\s*,", ". ", out)
    out = re.sub(r"\.\s*\.", ".", out)
    out = re.sub(r"\s{2,}", " ", out).strip(" ,")

    parts = re.split(r"([.!?]\s+)", out)
    rebuilt = []
    for i, p in enumerate(parts):
        if i % 2 == 0 and p:
            rebuilt.append(p[:1].upper() + p[1:])
        else:
            rebuilt.append(p)
    out = "".join(rebuilt)
    return out, changes


def tune_channel(text: str, channel: str) -> Tuple[str, List[str]]:
    changes: List[str] = []
    out = text

    if channel == "twitter":
        out = re.sub(r"\s+", " ", out).strip()
        if len(out) > 280:
            out = out[:277].rstrip() + "..."
            changes.append("Trimmed to <=280 chars for X/Twitter")
        changes.append("Tuned to punchy, direct style")

    elif channel == "linkedin":
        out = re.sub(r"\bguys\b", "folks", out, flags=re.I)
        out = re.sub(r"\s+", " ", out).strip()
        changes.append("Tuned to professional-conversational LinkedIn style")

    elif channel == "blog":
        if "I " not in out and "my " not in out.lower():
            out += "\n\nQuick take: this works better when you keep the language concrete and specific."
            changes.append("Added light opinionated voice for blog style")

    elif channel == "email":
        # make first sentence action-oriented if possible
        sents = split_sentences(out)
        if sents:
            sents[0] = "Quick update: " + sents[0][0].lower() + sents[0][1:] if len(sents[0]) > 1 else sents[0]
            out = " ".join(sents)
            changes.append("Made opening brief and action-oriented for email")

    return out, changes


def humanize(text: str, channel: str | None = None) -> HumanizeResult:
    detected = detect(text)
    revised, changes = rewrite_base(text)
    if channel:
        revised, c2 = tune_channel(revised, channel)
        changes.extend(c2)
    return HumanizeResult(revised=revised, changes=changes, detected=detected)


def main() -> int:
    ap = argparse.ArgumentParser(description="AI Content Humanization Tool")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--text", help="Input text")
    src.add_argument("--file", help="Path to input text file")
    ap.add_argument("--channel", choices=["twitter", "linkedin", "blog", "email"], help="Optional destination tuning")
    ap.add_argument("--show-changes", action="store_true", help="Show what changed and why")
    args = ap.parse_args()

    text = args.text or Path(args.file).read_text(encoding="utf-8", errors="ignore")
    result = humanize(text, args.channel)

    print(result.revised)
    if args.show_changes:
        print("\n--- DETECTED ---")
        for d in result.detected:
            print(f"- {d}")
        print("\n--- CHANGES ---")
        for c in result.changes:
            print(f"- {c}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
