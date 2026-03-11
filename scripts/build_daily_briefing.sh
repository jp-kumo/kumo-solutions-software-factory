#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/jpadmin/.openclaw/workspace"
OUT="${ROOT}/data/daily_briefing.md"
TS="$(date -u +"%Y-%m-%d %H:%M UTC")"

MARKDOWN_SNIPPET="${ROOT}/data/project_markdown_compliance_morning_snippet.md"
REPORT_DIR="${ROOT}/data/reports"

mkdir -p "${ROOT}/data"

CRM_SNIPPET="$(python3 - <<'PY'
import json
from pathlib import Path

report_dir = Path('/home/jpadmin/.openclaw/workspace/data/reports')
paths = sorted(report_dir.glob('personal_crm_run_*.json'), key=lambda p: p.stat().st_mtime)
if not paths:
    print('### Personal CRM\n- no recent report found')
    raise SystemExit(0)

p = paths[-1]
try:
    data = json.loads(p.read_text())
except Exception:
    print(f'### Personal CRM\n- latest report unreadable: `{p.name}`')
    raise SystemExit(0)

summary = data.get('summary', data)
candidates = summary.get('candidates', 'n/a')
shadow_mode = summary.get('shadow_mode', 'n/a')
shadow_approved = summary.get('shadow_approved', 'n/a')
new = summary.get('new', summary.get('new_contacts', summary.get('new_records', 'n/a')))
merges = summary.get('merges', 'n/a')
rejected = summary.get('rejected', 'n/a')
anomaly = summary.get('anomaly', 'n/a')
issues = summary.get('issues', 'n/a')

print('\n'.join([
    '### Personal CRM',
    f'- latest report: `{p.name}`',
    f'- candidates: **{candidates}**',
    f'- shadow mode: **{shadow_mode}** (approved: **{shadow_approved}**)',
    f'- new: **{new}** • merges: **{merges}** • rejected: **{rejected}**',
    f'- anomaly: **{anomaly}** • issues: **{issues}**',
]))
PY
)"

{
  echo "# Daily Briefing"
  echo
  echo "Generated: ${TS}"
  echo

  if [[ -f "${MARKDOWN_SNIPPET}" ]]; then
    cat "${MARKDOWN_SNIPPET}"
    echo
  else
    echo "### Markdown compliance"
    echo "- snippet unavailable"
    echo
  fi

  echo "${CRM_SNIPPET}"
  echo
} > "${OUT}"

echo "Updated: ${OUT}"