#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/jpadmin/.openclaw/workspace"
HISTORY_JSON="$ROOT/data/project_markdown_compliance_history.json"
HISTORY_MD="$ROOT/data/project_markdown_compliance_history.md"
HISTORY_SUMMARY_MD="$ROOT/data/project_markdown_compliance_history_7day.md"
MORNING_SNIPPET="$ROOT/data/project_markdown_compliance_morning_snippet.md"
SUMMARY_START="<!-- AUTO-7DAY-SUMMARY:START -->"
SUMMARY_END="<!-- AUTO-7DAY-SUMMARY:END -->"

cd "$ROOT"
python3 scripts/check_project_markdown_compliance.py \
  --history-json "$HISTORY_JSON" \
  --history-md-report "$HISTORY_MD" \
  --history-md-max-rows 30

python3 scripts/render_markdown_compliance_7day_summary.py \
  --history-json "$HISTORY_JSON" \
  --out-md "$HISTORY_SUMMARY_MD"

# Keep history dashboard idempotent by replacing (not appending) the auto summary block.
if [[ -f "$HISTORY_MD" && -f "$HISTORY_SUMMARY_MD" ]]; then
  TMP_FILE="$(mktemp)"

  awk -v start="$SUMMARY_START" -v end="$SUMMARY_END" '
    $0 == start { skip=1; next }
    $0 == end { skip=0; next }
    skip != 1 { print }
  ' "$HISTORY_MD" > "$TMP_FILE"

  {
    cat "$TMP_FILE"
    echo
    echo "$SUMMARY_START"
    cat "$HISTORY_SUMMARY_MD"
    echo "$SUMMARY_END"
  } > "$HISTORY_MD"

  rm -f "$TMP_FILE"
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

# Refresh consolidated daily briefing output.
if [[ -x "$ROOT/scripts/build_daily_briefing.sh" ]]; then
  "$ROOT/scripts/build_daily_briefing.sh"
fi

echo "Updated: $HISTORY_JSON"
echo "Updated: $HISTORY_MD"
echo "Updated: $HISTORY_SUMMARY_MD"
echo "Updated: $MORNING_SNIPPET"
