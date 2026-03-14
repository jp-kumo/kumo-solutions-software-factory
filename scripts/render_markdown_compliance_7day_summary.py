#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

NO_HISTORY_TEXT = "## 7-day trend summary\n\nNo history data available yet.\n"
NO_RECENT_RUNS_TEXT = "## 7-day trend summary\n\nNo runs in the last 7 days.\n"


def parse_ts(s: str) -> datetime | None:
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except Exception:
        return None


def load_history_rows(path: Path) -> list[dict[str, Any]]:
    if not path.exists() or not path.is_file():
        return []

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []

    if isinstance(data, dict):
        rows = data.get("history", [])
    else:
        rows = data

    if not isinstance(rows, list):
        return []
    return [row for row in rows if isinstance(row, dict)]


def render_summary_markdown(rows: list[dict[str, Any]], now: datetime | None = None) -> str:
    if not rows:
        return NO_HISTORY_TEXT

    now_utc = now or datetime.now(timezone.utc)
    cutoff = now_utc - timedelta(days=7)

    selected: list[dict[str, Any]] = []
    for r in rows:
        ts = parse_ts(str(r.get("generated_at") or r.get("run_at") or ""))
        if ts and ts >= cutoff:
            selected.append(r)

    selected.sort(key=lambda r: str(r.get("generated_at") or r.get("run_at") or ""))

    if not selected:
        return NO_RECENT_RUNS_TEXT

    non = [int(r.get("non_compliant_count", 0)) for r in selected]
    avg_non = sum(non) / len(non)

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
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Render 7-day trend summary for markdown compliance history")
    ap.add_argument("--history-json", required=True)
    ap.add_argument("--out-md", required=True)
    args = ap.parse_args()

    rows = load_history_rows(Path(args.history_json))
    output = render_summary_markdown(rows)
    Path(args.out_md).write_text(output, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
