#!/usr/bin/env python3

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sync_taste_power_tracker import discover_latest_runs, normalize_title, sync_rows


class SyncTastePowerTrackerTests(unittest.TestCase):
    def test_normalize_title(self):
        self.assertEqual(normalize_title("The War for Pepper"), "the_war_for_pepper")
        self.assertEqual(normalize_title("  The   History of Tea!"), "the_history_of_tea")

    def test_discover_latest_runs_picks_newest(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            older = base / "20260206_111111_the_war_for_pepper"
            newer = base / "20260206_222222_the_war_for_pepper"
            older.mkdir()
            newer.mkdir()
            (older / "4_script_draft.md").write_text("draft", encoding="utf-8")
            (newer / "5_final_script.md").write_text("final", encoding="utf-8")
            (newer / "6_visual_prompts.json").write_text("{}", encoding="utf-8")

            runs = discover_latest_runs(base)
            self.assertIn("the_war_for_pepper", runs)
            run = runs["the_war_for_pepper"]
            self.assertEqual(run.run_dir.name, newer.name)
            self.assertTrue(run.final_script)
            self.assertFalse(run.draft_script)
            self.assertTrue(run.visual_prompts)

    def test_sync_rows_updates_matching_title(self):
        rows = [
            {
                "episode_id": "EP01",
                "title": "The War for Pepper",
                "status": "Planned",
                "script_status": "Not Started",
                "edit_status": "Not Started",
                "thumb_status": "Not Started",
                "published_url": "",
                "notes": "",
            }
        ]

        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "20260206_171554_the_war_for_pepper"
            run_dir.mkdir()
            (run_dir / "5_final_script.md").write_text("final", encoding="utf-8")
            (run_dir / "6_visual_prompts.json").write_text("{}", encoding="utf-8")
            discovered = discover_latest_runs(Path(tmp))

        changed = sync_rows(rows, discovered)

        self.assertEqual(changed, 1)
        self.assertEqual(rows[0]["status"], "Needs QA")
        self.assertEqual(rows[0]["script_status"], "Ready")
        self.assertEqual(rows[0]["edit_status"], "Ready")
        self.assertEqual(rows[0]["thumb_status"], "Needs Pass")
        self.assertIn("Auto-synced", rows[0]["notes"])


if __name__ == "__main__":
    unittest.main()
