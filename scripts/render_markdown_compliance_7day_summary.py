#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path


def parse_ts(s: str) -> datetime | None:
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except Exception:
        return None


def main() -> int:
    ap = argparse.ArgumentParser(description="Render 7-day trend summary for markdown compliance history")
    ap.add_argument("--history-json", required=True)
    ap.add_argument("--out-md", required=True)
    args = ap.parse_args()

    p = Path(args.history_json)
    if not p.exists():
        Path(args.out_md).write_text("## 7-day trend summary\n\nNo history data available yet.\n", encoding="utf-8")
        return 0

    data = json.loads(p.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        rows = data.get("history", [])
    else:
        rows = data

    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=7)

    selected = []
    for r in rows:
        ts = parse_ts(str(r.get("generated_at") or r.get("run_at") or ""))
        if ts and ts >= cutoff:
            selected.append(r)

    selected.sort(key=lambda r: str(r.get("generated_at") or r.get("run_at") or ""))

    if not selected:
        Path(args.out_md).write_text("## 7-day trend summary\n\nNo runs in the last 7 days.\n", encoding="utf-8")
        return 0

    non = [int(r.get("non_compliant_count", 0)) for r in selected]
    avg_non = sum(non) / len(non)

    # streaks
    best = worst = cur_ok = cur_bad = 0
    for n in non:
        if n == 0:
            cur_ok += 1
            cur_bad = 0
        else:
            cur_bad += 1
            cur_ok = 0
        best = max(best, cur_ok)
        worst = max(worst, cur_bad)

    latest = selected[-1]
    lines = [
        "## 7-day trend summary",
        "",
        f"- Runs analyzed: **{len(selected)}**",
        f"- Average non-compliant projects: **{avg_non:.2f}**",
        f"- Best compliant streak (0 non-compliant): **{best}** runs",
        f"- Worst non-compliant streak (>0 non-compliant): **{worst}** runs",
        f"- Latest run: non-compliant=**{int(latest.get('non_compliant_count', 0))}**, project_count=**{int(latest.get('project_count', 0))}**",
        "",
    ]
    Path(args.out_md).write_text("\n".join(lines), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
