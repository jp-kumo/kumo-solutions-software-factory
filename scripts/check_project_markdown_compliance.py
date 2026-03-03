#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

DEFAULT_WORKSPACE = Path('/home/jpadmin/.openclaw/workspace')
DEFAULT_PROJECTS_DIR = DEFAULT_WORKSPACE / 'projects'
DEFAULT_DATA_DIR = DEFAULT_WORKSPACE / 'data'
DEFAULT_JSON_REPORT = DEFAULT_DATA_DIR / 'project_markdown_compliance.json'
DEFAULT_MD_REPORT = DEFAULT_DATA_DIR / 'project_markdown_compliance.md'

DEFAULT_REQUIRED_FILES = [
    'README.md',
    'docs/decisions.md',
    'docs/roadmap.md',
    'docs/security-notes.md',
    'docs/changelog.md',
]


@dataclass
class ProjectCompliance:
    project: str
    md_count: int
    missing_required: list[str]
    ok: bool


def parse_required_files(raw: str | None) -> list[str]:
    if not raw:
        return DEFAULT_REQUIRED_FILES.copy()
    files = [x.strip() for x in raw.split(',') if x.strip()]
    return files or DEFAULT_REQUIRED_FILES.copy()


def list_projects(projects_dir: Path) -> Iterable[Path]:
    return sorted(x for x in projects_dir.iterdir() if x.is_dir())


def check_project(project_dir: Path, required_files: list[str]) -> ProjectCompliance:
    missing = [rel for rel in required_files if not (project_dir / rel).exists()]
    md_count = len(list(project_dir.rglob('*.md')))
    return ProjectCompliance(
        project=project_dir.name,
        md_count=md_count,
        missing_required=missing,
        ok=len(missing) == 0,
    )


def build_markdown_report(
    generated_at: str,
    projects_dir: Path,
    required_files: list[str],
    results: list[ProjectCompliance],
) -> str:
    non_compliant = [r for r in results if not r.ok]
    lines = [
        '# Project Markdown Compliance Report',
        '',
        f'- Generated: {generated_at}',
        f'- Projects directory: `{projects_dir}`',
        f'- Project count: **{len(results)}**',
        f'- Non-compliant projects: **{len(non_compliant)}**',
        '',
        '## Required files',
        '',
    ]
    lines.extend(f'- `{f}`' for f in required_files)
    lines.extend(['', '## Project status', ''])

    if not results:
        lines.append('_No projects found._')
        lines.append('')
        return '\n'.join(lines)

    lines.append('| Project | Markdown Files | Status | Missing |')
    lines.append('|---|---:|---|---|')
    for r in results:
        status = '✅ OK' if r.ok else '❌ Missing files'
        missing = ', '.join(f'`{m}`' for m in r.missing_required) if r.missing_required else '—'
        lines.append(f'| {r.project} | {r.md_count} | {status} | {missing} |')

    lines.append('')
    return '\n'.join(lines)


def run_check(
    projects_dir: Path,
    json_report: Path,
    md_report: Path,
    required_files: list[str],
) -> int:
    generated_at = datetime.now(timezone.utc).isoformat()
    json_report.parent.mkdir(parents=True, exist_ok=True)

    if not projects_dir.exists():
        report = {
            'ok': True,
            'generated_at': generated_at,
            'projects_dir': str(projects_dir),
            'required_files': required_files,
            'projects': [],
            'message': 'No projects directory found.',
        }
        json_report.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
        md_report.write_text(
            build_markdown_report(generated_at, projects_dir, required_files, []),
            encoding='utf-8',
        )
        print(json.dumps({'ok': True, 'project_count': 0, 'non_compliant_count': 0}, indent=2))
        return 0

    results = [check_project(p, required_files) for p in list_projects(projects_dir)]
    non_compliant = [r for r in results if not r.ok]

    report = {
        'ok': len(non_compliant) == 0,
        'generated_at': generated_at,
        'projects_dir': str(projects_dir),
        'required_files': required_files,
        'project_count': len(results),
        'non_compliant_count': len(non_compliant),
        'projects': [asdict(r) for r in results],
    }

    json_report.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    md_report.write_text(
        build_markdown_report(generated_at, projects_dir, required_files, results),
        encoding='utf-8',
    )

    print(
        json.dumps(
            {
                'ok': report['ok'],
                'project_count': report['project_count'],
                'non_compliant_count': report['non_compliant_count'],
                'json_report_path': str(json_report),
                'markdown_report_path': str(md_report),
            },
            indent=2,
        )
    )

    return 0 if report['ok'] else 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Check projects for required markdown documentation and emit JSON + markdown reports.'
    )
    parser.add_argument(
        '--projects-dir',
        type=Path,
        default=DEFAULT_PROJECTS_DIR,
        help='Directory containing project folders (default: workspace/projects).',
    )
    parser.add_argument(
        '--json-report',
        type=Path,
        default=DEFAULT_JSON_REPORT,
        help='Path to write machine-readable JSON report.',
    )
    parser.add_argument(
        '--md-report',
        type=Path,
        default=DEFAULT_MD_REPORT,
        help='Path to write human-readable markdown report.',
    )
    parser.add_argument(
        '--required-files',
        type=str,
        default=None,
        help='Comma-separated list of required relative file paths. Uses defaults when omitted.',
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    required_files = parse_required_files(args.required_files)
    return run_check(
        projects_dir=args.projects_dir,
        json_report=args.json_report,
        md_report=args.md_report,
        required_files=required_files,
    )


if __name__ == '__main__':
    raise SystemExit(main())
