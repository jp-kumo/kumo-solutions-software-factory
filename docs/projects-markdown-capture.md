# Projects Markdown Capture

This file tracks project documentation artifacts in Markdown for continuity and restore.

Total projects: **2**

## cobol-modernization-bridge
- Markdown files: **4**
  - `projects/cobol-modernization-bridge/README.md`
  - `projects/cobol-modernization-bridge/data/raw/record_layout.md`
  - `projects/cobol-modernization-bridge/docs/architecture.md`
  - `projects/cobol-modernization-bridge/docs/interview-story-pack.md`

## secure-health-rag-reference
- Markdown files: **1**
  - `projects/secure-health-rag-reference/README.md`

## Minimum Markdown Standard (apply to each project)
- `README.md` — purpose, architecture, setup, run, test, demo.
- `docs/decisions.md` — key technical decisions + rationale.
- `docs/roadmap.md` — next milestones and acceptance criteria.
- `docs/security-notes.md` — threat assumptions, controls, known risks.
- `docs/changelog.md` — project-level human-readable changes.

## Compliance checker
- Script: `scripts/check_project_markdown_compliance.py`
- Run manually:
  - `python3 scripts/check_project_markdown_compliance.py`
- JSON report output:
  - `data/project_markdown_compliance.json`
- Exit code:
  - `0` when all projects compliant
  - `2` when one or more projects are missing required Markdown files

## Current Focus Project
- `projects/secure-health-rag-reference` already contains `README.md` and test scaffolding.
- Next doc additions recommended:
  - `projects/secure-health-rag-reference/docs/decisions.md`
  - `projects/secure-health-rag-reference/docs/roadmap.md`
  - `projects/secure-health-rag-reference/docs/security-notes.md`
  - `projects/secure-health-rag-reference/docs/changelog.md`
