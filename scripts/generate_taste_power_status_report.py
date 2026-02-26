#!/usr/bin/env python3
"""Generate a concise markdown status report from the Taste & Power tracker CSV."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


def load_rows(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def build_report(rows: list[dict]) -> str:
    status_counts = Counter((r.get("status") or "Unknown").strip() for r in rows)
    script_counts = Counter((r.get("script_status") or "Unknown").strip() for r in rows)

    lines = []
    lines.append("# Taste & Power Status Report")
    lines.append("")
    lines.append(f"Generated (UTC): {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')} UTC")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("- Episodes tracked: {}".format(len(rows)))
    lines.append("- Pipeline status: " + ", ".join(f"{k}: {v}" for k, v in sorted(status_counts.items())))
    lines.append("- Script status: " + ", ".join(f"{k}: {v}" for k, v in sorted(script_counts.items())))
    lines.append("")

    ready_for_qa = [r for r in rows if (r.get("status") or "").strip() == "Needs QA"]
    lines.append("## Ready for QA")
    lines.append("")
    if ready_for_qa:
        for row in ready_for_qa:
            lines.append(f"- {row.get('episode_id','')} — {row.get('title','')} ({row.get('notes','').strip()})")
    else:
        lines.append("- None")
    lines.append("")

    planned = [r for r in rows if (r.get("status") or "").strip() == "Planned"]
    lines.append("## Planned Backlog")
    lines.append("")
    if planned:
        for row in planned:
            lines.append(f"- {row.get('episode_id','')} — {row.get('title','')} ({row.get('script_status','')})")
    else:
        lines.append("- None")
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tracker", default="docs/taste-power-episodes-tracker.csv")
    parser.add_argument("--out", default="docs/taste-power-status-report.md")
    args = parser.parse_args()

    rows = load_rows(Path(args.tracker))
    report = build_report(rows)

    out_path = Path(args.out)
    out_path.write_text(report + "\n", encoding="utf-8")
    print(f"Wrote: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
