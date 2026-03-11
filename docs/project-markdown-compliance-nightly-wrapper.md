# Project Markdown Compliance Nightly Wrapper

## Purpose
Implements three operational improvements:
1. Nightly wrapper that always runs compliance with `--history-json`.
2. 7-day trend summary generation (streaks + average non-compliance).
3. Morning-digest-ready snippet output.

## Script
`scripts/run_project_markdown_compliance_nightly.sh`

## Generated artifacts
- `data/project_markdown_compliance_history.json`
- `data/project_markdown_compliance_history.md`
- `data/project_markdown_compliance_history_7day.md`
- `data/project_markdown_compliance_morning_snippet.md`
- `data/daily_briefing.md` (consolidated briefing output)

## Recommended cron command
```bash
bash /home/jpadmin/.openclaw/workspace/scripts/run_project_markdown_compliance_nightly.sh
```

## Morning digest integration
Nightly wrapper now refreshes a consolidated briefing file via:
- `scripts/build_daily_briefing.sh`

Outputs:
- `data/project_markdown_compliance_morning_snippet.md` (section snippet)
- `data/daily_briefing.md` (ready-to-consume briefing document)

This keeps markdown compliance signal wired into the daily briefing pipeline automatically.
