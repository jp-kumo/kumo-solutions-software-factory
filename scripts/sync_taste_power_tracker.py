#!/usr/bin/env python3
"""Sync docs/taste-power-episodes-tracker.csv from taste_and_power_system/output runs."""

from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional


RUN_DIR_PATTERN = re.compile(r"^(?P<ts>\d{8}_\d{6})_(?P<slug>[a-z0-9_]+)$")


@dataclass
class RunArtifacts:
    run_dir: Path
    final_script: bool
    draft_script: bool
    visual_prompts: bool



def normalize_title(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    return value



def discover_latest_runs(output_dir: Path) -> Dict[str, RunArtifacts]:
    runs: Dict[str, RunArtifacts] = {}

    if not output_dir.exists():
        return runs

    for child in output_dir.iterdir():
        if not child.is_dir():
            continue

        match = RUN_DIR_PATTERN.match(child.name)
        if not match:
            continue

        slug = match.group("slug")
        existing = runs.get(slug)
        if existing and existing.run_dir.name > child.name:
            # Existing is newer because timestamp prefix sorts lexicographically.
            continue

        runs[slug] = RunArtifacts(
            run_dir=child,
            final_script=(child / "5_final_script.md").exists(),
            draft_script=(child / "4_script_draft.md").exists(),
            visual_prompts=(child / "6_visual_prompts.json").exists(),
        )

    return runs



def sync_rows(rows: List[dict], discovered: Dict[str, RunArtifacts]) -> int:
    changed = 0

    for row in rows:
        slug = normalize_title(row.get("title", ""))
        run = discovered.get(slug)
        if not run:
            continue

        updates = {
            "status": "Needs QA" if run.final_script else "Planned",
            "script_status": (
                "Ready"
                if run.final_script
                else ("Draft" if run.draft_script else "Not Started")
            ),
            "edit_status": "Ready" if run.final_script else row.get("edit_status", "Not Started"),
            "thumb_status": "Needs Pass" if run.visual_prompts else "Not Started",
            "notes": f"Auto-synced from {run.run_dir.name}",
        }

        row_changed = False
        for key, value in updates.items():
            if row.get(key, "") != value:
                row[key] = value
                row_changed = True

        if row_changed:
            changed += 1

    return changed



def load_csv(path: Path) -> tuple[list[dict], list[str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        if not reader.fieldnames:
            raise ValueError(f"CSV has no header: {path}")
        return rows, reader.fieldnames



def write_csv(path: Path, rows: List[dict], fieldnames: List[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)



def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--tracker",
        default="docs/taste-power-episodes-tracker.csv",
        help="Path to tracker CSV",
    )
    parser.add_argument(
        "--output-dir",
        default="taste_and_power_system/output",
        help="Path to Taste & Power output directory",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print changes without writing")
    args = parser.parse_args()

    tracker_path = Path(args.tracker)
    output_dir = Path(args.output_dir)

    rows, fieldnames = load_csv(tracker_path)
    discovered = discover_latest_runs(output_dir)
    changed = sync_rows(rows, discovered)

    print(f"Discovered runs: {len(discovered)}")
    print(f"Tracker rows updated: {changed}")

    if args.dry_run:
        print("Dry run: no file written.")
        return 0

    if changed > 0:
        write_csv(tracker_path, rows, fieldnames)
        print(f"Updated: {tracker_path}")
    else:
        print("No changes needed.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
