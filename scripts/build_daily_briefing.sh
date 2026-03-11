#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/jpadmin/.openclaw/workspace"
OUT="${ROOT}/data/daily_briefing.md"
TS="$(date -u +"%Y-%m-%d %H:%M UTC")"

MARKDOWN_SNIPPET="${ROOT}/data/project_markdown_compliance_morning_snippet.md"

mkdir -p "${ROOT}/data"

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
} > "${OUT}"

echo "Updated: ${OUT}"