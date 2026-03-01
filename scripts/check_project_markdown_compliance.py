#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

WORKSPACE = Path('/home/jpadmin/.openclaw/workspace')
PROJECTS_DIR = WORKSPACE / 'projects'
REPORT_PATH = WORKSPACE / 'data' / 'project_markdown_compliance.json'

REQUIRED_FILES = [
    'README.md',
    'docs/decisions.md',
    'docs/roadmap.md',
    'docs/security-notes.md',
    'docs/changelog.md',
]


def check_project(project_dir: Path) -> dict:
    missing = []
    for rel in REQUIRED_FILES:
        if not (project_dir / rel).exists():
            missing.append(rel)
    md_count = len(list(project_dir.rglob('*.md')))
    return {
        'project': project_dir.name,
        'md_count': md_count,
        'missing_required': missing,
        'ok': len(missing) == 0,
    }


def main() -> int:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    if not PROJECTS_DIR.exists():
        report = {
            'ok': True,
            'projects': [],
            'message': 'No projects directory found.',
        }
        REPORT_PATH.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
        print(json.dumps(report, indent=2))
        return 0

    results = []
    for p in sorted([x for x in PROJECTS_DIR.iterdir() if x.is_dir()]):
        results.append(check_project(p))

    non_compliant = [r for r in results if not r['ok']]
    report = {
        'ok': len(non_compliant) == 0,
        'required_files': REQUIRED_FILES,
        'project_count': len(results),
        'non_compliant_count': len(non_compliant),
        'projects': results,
    }

    REPORT_PATH.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({
        'ok': report['ok'],
        'project_count': report['project_count'],
        'non_compliant_count': report['non_compliant_count'],
        'report_path': str(REPORT_PATH),
    }, indent=2))

    return 0 if report['ok'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
