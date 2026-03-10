#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/jpadmin/.openclaw/workspace"
HISTORY_JSON="$ROOT/data/project_markdown_compliance_history.json"
HISTORY_MD="$ROOT/data/project_markdown_compliance_history.md"
HISTORY_SUMMARY_MD="$ROOT/data/project_markdown_compliance_history_7day.md"
MORNING_SNIPPET="$ROOT/data/project_markdown_compliance_morning_snippet.md"

cd "$ROOT"
python3 scripts/check_project_markdown_compliance.py \
  --history-json "$HISTORY_JSON" \
  --history-md-report "$HISTORY_MD" \
  --history-md-max-rows 30

python3 scripts/render_markdown_compliance_7day_summary.py \
  --history-json "$HISTORY_JSON" \
  --out-md "$HISTORY_SUMMARY_MD"

# Append 7-day summary into history markdown report.
if [[ -f "$HISTORY_MD" && -f "$HISTORY_SUMMARY_MD" ]]; then
  {
    echo
    echo "---"
    echo
    cat "$HISTORY_SUMMARY_MD"
  } >> "$HISTORY_MD"
fi

# Generate morning digest snippet consumed by summary jobs or manual updates.
{
  echo "### Markdown compliance"
  if [[ -f "$HISTORY_SUMMARY_MD" ]]; then
    cat "$HISTORY_SUMMARY_MD"
  else
    echo "- 7-day summary unavailable"
  fi
} > "$MORNING_SNIPPET"

echo "Updated: $HISTORY_JSON"
echo "Updated: $HISTORY_MD"
echo "Updated: $HISTORY_SUMMARY_MD"
echo "Updated: $MORNING_SNIPPET"
