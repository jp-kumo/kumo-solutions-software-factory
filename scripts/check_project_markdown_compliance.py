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

DEFAULT_MD_EXCLUDE_DIRS = {
    '.git',
    '.venv',
    'venv',
    'node_modules',
    '__pycache__',
    '.pytest_cache',
    '.mypy_cache',
    'dist',
    'build',
}


@dataclass
class ProjectCompliance:
    project: str
    md_count: int
    missing_required: list[str]
    present_required_count: int
    required_total: int
    required_coverage_pct: float
    ok: bool


def parse_required_files(raw: str | None) -> list[str]:
    if not raw:
        return DEFAULT_REQUIRED_FILES.copy()
    files = [x.strip() for x in raw.split(',') if x.strip()]
    return files or DEFAULT_REQUIRED_FILES.copy()


def parse_exclude_dirs(raw: str | None) -> set[str]:
    if not raw:
        return set(DEFAULT_MD_EXCLUDE_DIRS)
    parsed = {x.strip() for x in raw.split(',') if x.strip()}
    return parsed or set(DEFAULT_MD_EXCLUDE_DIRS)


def list_projects(projects_dir: Path, project_glob: str = '*') -> Iterable[Path]:
    return sorted(x for x in projects_dir.glob(project_glob) if x.is_dir())


def count_markdown_files(project_dir: Path, exclude_dirs: set[str]) -> int:
    count = 0
    for path in project_dir.rglob('*.md'):
        if any(part in exclude_dirs for part in path.relative_to(project_dir).parts):
            continue
        count += 1
    return count


def check_project(
    project_dir: Path,
    required_files: list[str],
    exclude_dirs: set[str],
    min_md_files: int,
) -> ProjectCompliance:
    missing = [rel for rel in required_files if not (project_dir / rel).exists()]
    md_count = count_markdown_files(project_dir, exclude_dirs)

    if md_count < min_md_files:
        missing.append(f'__min_markdown_files__ ({md_count} < {min_md_files})')

    required_total = len(required_files)
    present_required_count = required_total - len([m for m in missing if not m.startswith('__min_markdown_files__')])
    required_coverage_pct = (present_required_count / required_total * 100.0) if required_total else 100.0

    return ProjectCompliance(
        project=project_dir.name,
        md_count=md_count,
        missing_required=missing,
        present_required_count=present_required_count,
        required_total=required_total,
        required_coverage_pct=round(required_coverage_pct, 1),
        ok=len(missing) == 0,
    )


def build_markdown_report(
    generated_at: str,
    projects_dir: Path,
    required_files: list[str],
    results: list[ProjectCompliance],
    min_md_files: int,
    exclude_dirs: set[str],
) -> str:
    non_compliant = [r for r in results if not r.ok]
    lines = [
        '# Project Markdown Compliance Report',
        '',
        f'- Generated: {generated_at}',
        f'- Projects directory: `{projects_dir}`',
        f'- Project count: **{len(results)}**',
        f'- Non-compliant projects: **{len(non_compliant)}**',
        f'- Minimum markdown files per project: **{min_md_files}**',
        '',
        '## Required files',
        '',
    ]
    lines.extend(f'- `{f}`' for f in required_files)

    lines.extend(['', '## Markdown count exclusions', ''])
    for directory in sorted(exclude_dirs):
        lines.append(f'- `{directory}`')

    lines.extend(['', '## Project status', ''])

    if not results:
        lines.append('_No projects found._')
        lines.append('')
        return '\n'.join(lines)

    lines.append('| Project | Markdown Files | Required Coverage | Status | Missing |')
    lines.append('|---|---:|---:|---|---|')
    for r in results:
        status = '✅ OK' if r.ok else '❌ Missing files'
        missing = ', '.join(f'`{m}`' for m in r.missing_required) if r.missing_required else '—'
        coverage = f"{r.present_required_count}/{r.required_total} ({r.required_coverage_pct:.1f}%)"
        lines.append(f'| {r.project} | {r.md_count} | {coverage} | {status} | {missing} |')

    lines.append('')
    return '\n'.join(lines)


def run_check(
    projects_dir: Path,
    json_report: Path,
    md_report: Path,
    required_files: list[str],
    min_md_files: int = 1,
    exclude_dirs: set[str] | None = None,
    project_glob: str = '*',
    emit_summary: bool = True,
) -> int:
    generated_at = datetime.now(timezone.utc).isoformat()
    json_report.parent.mkdir(parents=True, exist_ok=True)
    exclude_dirs = exclude_dirs or set(DEFAULT_MD_EXCLUDE_DIRS)

    if not projects_dir.exists():
        report = {
            'ok': True,
            'generated_at': generated_at,
            'projects_dir': str(projects_dir),
            'project_glob': project_glob,
            'required_files': required_files,
            'min_md_files': min_md_files,
            'exclude_dirs': sorted(exclude_dirs),
            'projects': [],
            'message': 'No projects directory found.',
        }
        json_report.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
        md_report.write_text(
            build_markdown_report(
                generated_at,
                projects_dir,
                required_files,
                [],
                min_md_files=min_md_files,
                exclude_dirs=exclude_dirs,
            ),
            encoding='utf-8',
        )
        if emit_summary:
            print(json.dumps({'ok': True, 'project_count': 0, 'non_compliant_count': 0}, indent=2))
        return 0

    results = [
        check_project(
            p,
            required_files=required_files,
            exclude_dirs=exclude_dirs,
            min_md_files=min_md_files,
        )
        for p in list_projects(projects_dir, project_glob=project_glob)
    ]
    non_compliant = [r for r in results if not r.ok]

    report = {
        'ok': len(non_compliant) == 0,
        'generated_at': generated_at,
        'projects_dir': str(projects_dir),
        'project_glob': project_glob,
        'required_files': required_files,
        'min_md_files': min_md_files,
        'exclude_dirs': sorted(exclude_dirs),
        'project_count': len(results),
        'non_compliant_count': len(non_compliant),
        'projects': [asdict(r) for r in results],
    }

    json_report.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    md_report.write_text(
        build_markdown_report(
            generated_at,
            projects_dir,
            required_files,
            results,
            min_md_files=min_md_files,
            exclude_dirs=exclude_dirs,
        ),
        encoding='utf-8',
    )

    if emit_summary:
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
    parser.add_argument(
        '--min-md-files',
        type=int,
        default=1,
        help='Minimum markdown file count per project for compliance (default: 1).',
    )
    parser.add_argument(
        '--exclude-dirs',
        type=str,
        default=None,
        help='Comma-separated directory names to exclude from markdown counting.',
    )
    parser.add_argument(
        '--project-glob',
        type=str,
        default='*',
        help='Glob pattern to select project directories (default: *).',
    )
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress JSON summary output to stdout (files are still written).',
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    required_files = parse_required_files(args.required_files)
    exclude_dirs = parse_exclude_dirs(args.exclude_dirs)

    if args.min_md_files < 0:
        parser.error('--min-md-files must be >= 0')

    return run_check(
        projects_dir=args.projects_dir,
        json_report=args.json_report,
        md_report=args.md_report,
        required_files=required_files,
        min_md_files=args.min_md_files,
        exclude_dirs=exclude_dirs,
        project_glob=args.project_glob,
        emit_summary=not args.quiet,
    )


if __name__ == '__main__':
    raise SystemExit(main())
