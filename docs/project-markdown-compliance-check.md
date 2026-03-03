# Project Markdown Compliance Check

This workspace includes a documentation compliance checker at:

- `scripts/check_project_markdown_compliance.py`

## What it does

- Scans each project under `projects/`
- Verifies required docs exist (README + key docs under `docs/`)
- Generates:
  - machine-readable JSON report
  - human-readable markdown report

Default outputs:

- `data/project_markdown_compliance.json`
- `data/project_markdown_compliance.md`

## Default required files

- `README.md`
- `docs/decisions.md`
- `docs/roadmap.md`
- `docs/security-notes.md`
- `docs/changelog.md`

## Usage

```bash
python3 scripts/check_project_markdown_compliance.py
```

Custom paths/files:

```bash
python3 scripts/check_project_markdown_compliance.py \
  --projects-dir /path/to/projects \
  --json-report /tmp/compliance.json \
  --md-report /tmp/compliance.md \
  --required-files "README.md,docs/roadmap.md,docs/changelog.md"
```

Exit code:

- `0` when all projects are compliant (or no projects directory exists)
- `2` when one or more projects are missing required files
