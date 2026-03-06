#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 /path/to/backup.sql.gz" >&2
  exit 1
fi

backup_file="$1"

if [[ ! -f "${backup_file}" ]]; then
  echo "Backup file not found: ${backup_file}" >&2
  exit 1
fi

gunzip -c "${backup_file}" | docker compose exec -T postgres psql -U "${POSTGRES_USER:-mission_control_app}" "${POSTGRES_DB:-mission_control}"

echo "Restore complete from ${backup_file}"
