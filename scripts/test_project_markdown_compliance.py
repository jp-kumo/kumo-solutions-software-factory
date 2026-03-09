#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import io
import json
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
                emit_summary=False,
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
                emit_summary=False,
            )
            self.assertEqual(code, 0)
            self.assertTrue(json_report.exists())
            self.assertTrue(md_report.exists())

    def test_run_check_min_md_files_threshold_enforced(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            projects_dir = root / 'projects'
            project = projects_dir / 'p1'
            project.mkdir(parents=True)
            (project / 'README.md').write_text('# readme\n', encoding='utf-8')
            docs = project / 'docs'
            docs.mkdir()
            (docs / 'decisions.md').write_text('ok\n', encoding='utf-8')

            code = run_check(
                projects_dir=projects_dir,
                json_report=root / 'report.json',
                md_report=root / 'report.md',
                required_files=['README.md', 'docs/decisions.md'],
                min_md_files=3,
                emit_summary=False,
            )

            self.assertEqual(code, 2)
            text = (root / 'report.md').read_text(encoding='utf-8')
            self.assertIn('__min_markdown_files__ (2 < 3)', text)

    def test_run_check_excludes_configured_dirs_from_md_count(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            projects_dir = root / 'projects'
            project = projects_dir / 'p1'
            project.mkdir(parents=True)
            (project / 'README.md').write_text('# readme\n', encoding='utf-8')

            (project / 'node_modules').mkdir()
            (project / 'node_modules' / 'vendor.md').write_text('noise\n', encoding='utf-8')

            code = run_check(
                projects_dir=projects_dir,
                json_report=root / 'report.json',
                md_report=root / 'report.md',
                required_files=['README.md'],
                min_md_files=2,
                exclude_dirs={'node_modules'},
                emit_summary=False,
            )

            self.assertEqual(code, 2)
            text = (root / 'report.md').read_text(encoding='utf-8')
            self.assertIn('| p1 | 1 | 1/1 (100.0%) | ❌ Missing files |', text)

    def test_run_check_project_glob_filters_projects(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            projects_dir = root / 'projects'
            projects_dir.mkdir(parents=True)

            selected = projects_dir / 'ai-selected'
            selected.mkdir()
            (selected / 'README.md').write_text('# ok\n', encoding='utf-8')

            ignored = projects_dir / 'web-ignored'
            ignored.mkdir()

            code = run_check(
                projects_dir=projects_dir,
                json_report=root / 'report.json',
                md_report=root / 'report.md',
                required_files=['README.md'],
                project_glob='ai-*',
                emit_summary=False,
            )

            self.assertEqual(code, 0)
            text = (root / 'report.md').read_text(encoding='utf-8')
            self.assertIn('ai-selected', text)
            self.assertNotIn('web-ignored', text)

    def test_run_check_trend_detects_improvement_against_baseline(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            projects_dir = root / 'projects'
            project = projects_dir / 'p1'
            project.mkdir(parents=True)
            (project / 'README.md').write_text('# ok\n', encoding='utf-8')

            baseline_path = root / 'baseline.json'
            baseline_path.write_text(
                json.dumps(
                    {
                        'generated_at': '2026-03-01T00:00:00+00:00',
                        'project_count': 1,
                        'non_compliant_count': 1,
                        'projects': [
                            {
                                'project': 'p1',
                                'ok': False,
                            }
                        ],
                    }
                ),
                encoding='utf-8',
            )

            code = run_check(
                projects_dir=projects_dir,
                json_report=root / 'report.json',
                md_report=root / 'report.md',
                required_files=['README.md'],
                baseline_json=baseline_path,
                emit_summary=False,
            )

            self.assertEqual(code, 0)
            report = json.loads((root / 'report.json').read_text(encoding='utf-8'))
            trend = report['trend']
            self.assertEqual(trend['delta_non_compliant'], -1)
            self.assertEqual(trend['improved_projects'], ['p1'])
            self.assertEqual(trend['regressed_projects'], [])

    def test_run_check_invalid_baseline_is_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            projects_dir = root / 'projects'
            project = projects_dir / 'p1'
            project.mkdir(parents=True)
            (project / 'README.md').write_text('# ok\n', encoding='utf-8')

            baseline_path = root / 'bad-baseline.json'
            baseline_path.write_text('{not valid json', encoding='utf-8')

            code = run_check(
                projects_dir=projects_dir,
                json_report=root / 'report.json',
                md_report=root / 'report.md',
                required_files=['README.md'],
                baseline_json=baseline_path,
                emit_summary=False,
            )

            self.assertEqual(code, 0)
            report = json.loads((root / 'report.json').read_text(encoding='utf-8'))
            trend = report['trend']
            self.assertFalse(trend['has_baseline'])
            self.assertIsNone(trend['delta_non_compliant'])

    def test_run_check_can_suppress_stdout_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            projects_dir = root / 'projects'
            project = projects_dir / 'p1'
            project.mkdir(parents=True)
            (project / 'README.md').write_text('# ok\n', encoding='utf-8')

            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = run_check(
                    projects_dir=projects_dir,
                    json_report=root / 'report.json',
                    md_report=root / 'report.md',
                    required_files=['README.md'],
                    emit_summary=False,
                )

            self.assertEqual(code, 0)
            self.assertEqual(buf.getvalue(), '')

    def test_run_check_emits_missing_requirement_frequency_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            projects_dir = root / 'projects'
            projects_dir.mkdir(parents=True)

            p1 = projects_dir / 'p1'
            p1.mkdir()
            (p1 / 'README.md').write_text('# ok\n', encoding='utf-8')

            p2 = projects_dir / 'p2'
            p2.mkdir()

            run_check(
                projects_dir=projects_dir,
                json_report=root / 'report.json',
                md_report=root / 'report.md',
                required_files=['README.md', 'docs/roadmap.md'],
                emit_summary=False,
            )

            report = json.loads((root / 'report.json').read_text(encoding='utf-8'))
            self.assertIn('missing_required_frequency', report)
            self.assertEqual(
                report['missing_required_frequency'][0],
                {'requirement': 'docs/roadmap.md', 'missing_in_projects': 2},
            )

            md_text = (root / 'report.md').read_text(encoding='utf-8')
            self.assertIn('## Most commonly missing requirements', md_text)
            self.assertIn('`docs/roadmap.md` missing in **2** project(s)', md_text)

    def test_run_check_fail_on_regression_returns_3(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            projects_dir = root / 'projects'
            project = projects_dir / 'p1'
            project.mkdir(parents=True)

            baseline_path = root / 'baseline.json'
            baseline_path.write_text(
                json.dumps(
                    {
                        'generated_at': '2026-03-01T00:00:00+00:00',
                        'project_count': 1,
                        'non_compliant_count': 0,
                        'projects': [{'project': 'p1', 'ok': True}],
                    }
                ),
                encoding='utf-8',
            )

            code = run_check(
                projects_dir=projects_dir,
                json_report=root / 'report.json',
                md_report=root / 'report.md',
                required_files=['README.md'],
                baseline_json=baseline_path,
                fail_on_regression=True,
                emit_summary=False,
            )

            self.assertEqual(code, 3)
            report = json.loads((root / 'report.json').read_text(encoding='utf-8'))
            self.assertTrue(report['regression_detected'])

    def test_run_check_appends_history_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            projects_dir = root / 'projects'
            project = projects_dir / 'p1'
            project.mkdir(parents=True)
            (project / 'README.md').write_text('# ok\n', encoding='utf-8')

            history_path = root / 'history.json'

            run_check(
                projects_dir=projects_dir,
                json_report=root / 'r1.json',
                md_report=root / 'r1.md',
                required_files=['README.md'],
                history_json=history_path,
                max_history=1,
                emit_summary=False,
            )
            run_check(
                projects_dir=projects_dir,
                json_report=root / 'r2.json',
                md_report=root / 'r2.md',
                required_files=['README.md'],
                history_json=history_path,
                max_history=1,
                emit_summary=False,
            )

            history = json.loads(history_path.read_text(encoding='utf-8'))
            self.assertEqual(len(history), 1)
            self.assertEqual(history[0]['project_count'], 1)
            self.assertTrue(history[0]['ok'])


if __name__ == '__main__':
    unittest.main()
