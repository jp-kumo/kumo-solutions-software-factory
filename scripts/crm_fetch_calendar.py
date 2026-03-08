#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import json
import subprocess
from typing import Any, Dict, List

ACCOUNT = "jacquespayne.9914@gmail.com"
CLIENT = "default"


def listify(x: Any) -> List[Dict[str, Any]]:
    if isinstance(x, list):
        return x
    if isinstance(x, dict):
        for k in ("events", "items", "data", "results"):
            v = x.get(k)
            if isinstance(v, list):
                return v
    return []


def iso(v: Any) -> str:
    if isinstance(v, dict):
        return str(v.get("dateTime") or v.get("date") or "")
    return str(v or "")


def main() -> int:
    now = dt.datetime.now(dt.timezone.utc)
    start = (now - dt.timedelta(days=60)).isoformat().replace("+00:00", "Z")
    end = now.isoformat().replace("+00:00", "Z")

    cmd = [
        "gog",
        "calendar",
        "events",
        "primary",
        "--account",
        ACCOUNT,
        "--client",
        CLIENT,
        "--from",
        start,
        "--to",
        end,
        "--all-pages",
        "--max",
        "500",
        "--json",
        "--no-input",
    ]
    raw = subprocess.check_output(cmd, text=True)
    data = json.loads(raw)
    rows = listify(data)

    out: List[Dict[str, Any]] = []
    for e in rows:
        attendees = []
        for a in e.get("attendees", []) or []:
            if isinstance(a, dict):
                attendees.append({"name": a.get("displayName", ""), "email": a.get("email", "")})
            else:
                attendees.append({"name": "", "email": str(a)})

        s = iso(e.get("start"))
        t = iso(e.get("end"))
        duration_minutes = 0
        try:
            sd = dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
            ed = dt.datetime.fromisoformat(t.replace("Z", "+00:00"))
            duration_minutes = int((ed - sd).total_seconds() // 60)
        except Exception:
            duration_minutes = int(e.get("duration_minutes") or 0)

        out.append(
            {
                "title": e.get("summary") or e.get("title") or "",
                "start": s,
                "end": t,
                "duration_minutes": duration_minutes,
                "attendees": attendees,
            }
        )

    print(json.dumps(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
