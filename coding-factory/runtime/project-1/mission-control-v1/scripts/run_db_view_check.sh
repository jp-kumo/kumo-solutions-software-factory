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
set +e
python3 scripts/verify_reporting_views.py --dsn "${DSN}" --out-json "${OUT_JSON}"
RC=$?
set -e

cp "${OUT_JSON}" "${OUT_LATEST}"

echo "Wrote: ${OUT_JSON}"
echo "Updated: ${OUT_LATEST}"

ALERT_FILE="${REPORT_DIR}/mission-control-db-view-alert-${TS}.txt"
python3 - <<PY > "${ALERT_FILE}"
import json
from pathlib import Path
p = Path("${OUT_JSON}")
r = json.loads(p.read_text())
failed = [c for c in r.get("checks", []) if not (c.get("exists") and c.get("queryable"))]
if not failed:
    print("DB View Check OK: all required reporting views are present and queryable.")
else:
    lines = ["⚠️ Mission Control DB View Gate FAILED", ""]
    for f in failed:
        lines.append(f"- {f.get('name')}: exists={f.get('exists')} queryable={f.get('queryable')} error={f.get('error')}")
    lines.append("")
    lines.append(f"Report: {p}")
    print("\n".join(lines))
PY

# Optional Telegram alert (telegram-ready): set TELEGRAM_BOT_TOKEN + TELEGRAM_CHAT_ID
if [[ "${RC}" -ne 0 && -n "${TELEGRAM_BOT_TOKEN:-}" && -n "${TELEGRAM_CHAT_ID:-}" ]]; then
  MSG="$(cat "${ALERT_FILE}")"
  curl -sS -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
    -d "chat_id=${TELEGRAM_CHAT_ID}" \
    --data-urlencode "text=${MSG}" >/dev/null || true
fi

echo "Alert text: ${ALERT_FILE}"
exit "${RC}"
