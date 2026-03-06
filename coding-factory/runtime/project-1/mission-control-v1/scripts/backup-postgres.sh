#!/usr/bin/env bash
set -euo pipefail

mkdir -p backups
ts="$(date +%Y%m%d-%H%M%S)"
outfile="backups/mission-control-${ts}.sql.gz"

docker compose exec -T postgres pg_dump -U "${POSTGRES_USER:-mission_control_app}" "${POSTGRES_DB:-mission_control}" | gzip > "${outfile}"

echo "Wrote ${outfile}"
