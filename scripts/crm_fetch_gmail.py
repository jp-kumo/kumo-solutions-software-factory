#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from typing import Any, Dict, List

ACCOUNT = "jacquespayne.9914@gmail.com"


def listify(x: Any) -> List[Dict[str, Any]]:
    if isinstance(x, list):
        return x
    if isinstance(x, dict):
        for k in ("messages", "items", "data", "threads", "results"):
            v = x.get(k)
            if isinstance(v, list):
                return v
    return []


def header(msg: Dict[str, Any], name: str) -> str:
    # Handle common shapes
    for container in (msg.get("payload", {}), msg):
        headers = container.get("headers") if isinstance(container, dict) else None
        if isinstance(headers, list):
            for h in headers:
                if str(h.get("name", "")).lower() == name.lower():
                    return str(h.get("value", ""))
    return str(msg.get(name, ""))


def main() -> int:
    cmd = [
        "gog",
        "gmail",
        "messages",
        "search",
        "newer_than:60d",
        "--account",
        ACCOUNT,
        "--max",
        "500",
        "--all",
        "--include-body",
        "--json",
        "--no-input",
    ]
    raw = subprocess.check_output(cmd, text=True)
    data = json.loads(raw)
    rows = listify(data)

    out: List[Dict[str, Any]] = []
    for m in rows:
        out.append(
            {
                "threadId": m.get("threadId") or m.get("thread_id") or "",
                "subject": header(m, "Subject"),
                "snippet": m.get("snippet") or "",
                "date": header(m, "Date") or m.get("internalDate") or "",
                "from": header(m, "From") or m.get("from") or "",
                "to": header(m, "To") or m.get("to") or "",
                "cc": header(m, "Cc") or m.get("cc") or "",
                "bcc": header(m, "Bcc") or m.get("bcc") or "",
            }
        )

    print(json.dumps(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
