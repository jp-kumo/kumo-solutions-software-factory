#!/usr/bin/env bash
set -euo pipefail

# One-command wrapper for Taste & Power episode generation
# Usage:
#   ./scripts/run_episode_pipeline.sh --topic "The Salt Tax" [--marketing]

WORKDIR="/home/jpadmin/.openclaw/workspace"
SYSTEM_DIR="$WORKDIR/taste_and_power_system"

if [[ ! -d "$SYSTEM_DIR" ]]; then
  echo "ERROR: taste_and_power_system not found at $SYSTEM_DIR" >&2
  exit 2
fi

cd "$WORKDIR"
python3 "$WORKDIR/scripts/run_taste_power_episode.py" --system-dir "$SYSTEM_DIR" "$@"
