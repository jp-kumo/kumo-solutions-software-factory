#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="/home/jpadmin/.openclaw/workspace/coding-factory/runtime/project-1/mission-control-v1"
REPORT_DIR="/home/jpadmin/.openclaw/workspace/data/reports"
TS="$(date -u +%Y-%m-%dT%H-%M-%SZ)"
OUT_JSON="${REPORT_DIR}/mission-control-db-view-check-${TS}.json"
OUT_LATEST="${REPORT_DIR}/mission-control-db-view-check-latest.json"

# Allow override from environment/CI
DSN="${DB_VIEW_CHECK_DSN:-${DATABASE_URL:-postgresql://postgres:postgres@localhost:15432/mission_control}}"

mkdir -p "${REPORT_DIR}"

cd "${ROOT_DIR}"
python3 scripts/verify_reporting_views.py --dsn "${DSN}" --out-json "${OUT_JSON}"
cp "${OUT_JSON}" "${OUT_LATEST}"

echo "Wrote: ${OUT_JSON}"
echo "Updated: ${OUT_LATEST}"
