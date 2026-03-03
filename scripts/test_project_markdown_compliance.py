#!/usr/bin/env python3
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_project_markdown_compliance import run_check


class ProjectMarkdownComplianceTests(unittest.TestCase):
    def test_run_check_generates_reports_and_nonzero_on_missing_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            projects_dir = root / 'projects'
            projects_dir.mkdir(parents=True)

            complete = projects_dir / 'complete-project'
            complete.mkdir()
            (complete / 'README.md').write_text('# ok\n', encoding='utf-8')
            docs = complete / 'docs'
            docs.mkdir()
            for name in ['decisions.md', 'roadmap.md', 'security-notes.md', 'changelog.md']:
                (docs / name).write_text('ok\n', encoding='utf-8')

            incomplete = projects_dir / 'incomplete-project'
            incomplete.mkdir()
            (incomplete / 'README.md').write_text('# missing docs\n', encoding='utf-8')

            json_report = root / 'report.json'
            md_report = root / 'report.md'
            code = run_check(
                projects_dir=projects_dir,
                json_report=json_report,
                md_report=md_report,
                required_files=[
                    'README.md',
                    'docs/decisions.md',
                    'docs/roadmap.md',
                    'docs/security-notes.md',
                    'docs/changelog.md',
                ],
            )

            self.assertEqual(code, 2)
            self.assertTrue(json_report.exists())
            self.assertTrue(md_report.exists())
            md_text = md_report.read_text(encoding='utf-8')
            self.assertIn('incomplete-project', md_text)
            self.assertIn('❌ Missing files', md_text)

    def test_run_check_no_projects_dir_returns_success(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            json_report = root / 'report.json'
            md_report = root / 'report.md'
            code = run_check(
                projects_dir=root / 'does-not-exist',
                json_report=json_report,
                md_report=md_report,
                required_files=['README.md'],
            )
            self.assertEqual(code, 0)
            self.assertTrue(json_report.exists())
            self.assertTrue(md_report.exists())


if __name__ == '__main__':
    unittest.main()
