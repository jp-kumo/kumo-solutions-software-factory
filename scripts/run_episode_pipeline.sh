#!/usr/bin/env bash
set -euo pipefail

# One-command wrapper for Taste & Power episode generation
# Usage:
#   ./scripts/run_episode_pipeline.sh --topic "The Salt Tax" [--marketing] [--sync-tracker] [--status-report]

WORKDIR="/home/jpadmin/.openclaw/workspace"
SYSTEM_DIR="$WORKDIR/taste_and_power_system"
SYNC_TRACKER=0
STATUS_REPORT=0
ARGS=()

while (($#)); do
  case "$1" in
    --sync-tracker)
      SYNC_TRACKER=1
      shift
      ;;
    --status-report)
      STATUS_REPORT=1
      shift
      ;;
    *)
      ARGS+=("$1")
      shift
      ;;
  esac
done

if [[ ! -d "$SYSTEM_DIR" ]]; then
  echo "ERROR: taste_and_power_system not found at $SYSTEM_DIR" >&2
  exit 2
fi

cd "$WORKDIR"
python3 "$WORKDIR/scripts/run_taste_power_episode.py" --system-dir "$SYSTEM_DIR" "${ARGS[@]}"

if [[ "$SYNC_TRACKER" -eq 1 ]]; then
  python3 "$WORKDIR/scripts/sync_taste_power_tracker.py"
fi

if [[ "$STATUS_REPORT" -eq 1 ]]; then
  python3 "$WORKDIR/scripts/generate_taste_power_status_report.py"
fi
