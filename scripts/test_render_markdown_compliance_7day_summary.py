#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import render_markdown_compliance_7day_summary as target


class RenderMarkdownCompliance7DaySummaryTests(unittest.TestCase):
    def test_load_history_rows_missing_file_returns_empty(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'missing.json'
            self.assertEqual(target.load_history_rows(path), [])

    def test_load_history_rows_invalid_json_returns_empty(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'bad.json'
            path.write_text('{invalid', encoding='utf-8')
            self.assertEqual(target.load_history_rows(path), [])

    def test_load_history_rows_dict_payload_uses_history_key(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'history.json'
            path.write_text(json.dumps({'history': [{'generated_at': '2026-03-14T00:00:00+00:00'}]}), encoding='utf-8')
            rows = target.load_history_rows(path)
            self.assertEqual(len(rows), 1)

    def test_render_summary_markdown_no_recent_runs(self) -> None:
        rows = [{'generated_at': '2020-01-01T00:00:00+00:00', 'non_compliant_count': 1}]
        out = target.render_summary_markdown(rows, now=datetime(2026, 3, 14, tzinfo=timezone.utc))
        self.assertIn('No runs in the last 7 days', out)

    def test_render_summary_markdown_computes_metrics(self) -> None:
        rows = [
            {'generated_at': '2026-03-10T00:00:00+00:00', 'non_compliant_count': 2, 'project_count': 10},
            {'generated_at': '2026-03-11T00:00:00+00:00', 'non_compliant_count': 0, 'project_count': 10},
            {'generated_at': '2026-03-12T00:00:00+00:00', 'non_compliant_count': 0, 'project_count': 10},
        ]
        out = target.render_summary_markdown(rows, now=datetime(2026, 3, 14, tzinfo=timezone.utc))
        self.assertIn('Runs analyzed: **3**', out)
        self.assertIn('Average non-compliant projects: **0.67**', out)
        self.assertIn('Best compliant streak (0 non-compliant): **2** runs', out)
        self.assertIn('Latest run: non-compliant=**0**, project_count=**10**', out)


if __name__ == '__main__':
    unittest.main()
