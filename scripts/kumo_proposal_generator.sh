#!/usr/bin/env bash
# scripts/kumo_proposal_generator.sh
# Generate a Kumo Solutions proposal draft from template.
#
# Usage:
#   ./scripts/kumo_proposal_generator.sh "Client Name" [YYYY-MM-DD] [output_filename.md]
#
# Examples:
#   ./scripts/kumo_proposal_generator.sh "Acme Biotech"
#   ./scripts/kumo_proposal_generator.sh "Acme Biotech" "2026-03-01"
#   ./scripts/kumo_proposal_generator.sh "Acme Biotech" "2026-03-01" "proposals/acme-proposal.md"

set -euo pipefail

show_help() {
  cat <<'EOF'
Generate a Kumo Solutions proposal draft from template.

Usage:
  kumo_proposal_generator.sh "Client Name" [YYYY-MM-DD] [output_filename.md]

Arguments:
  Client Name        Required. Used to replace {{Client Name}} in template.
  YYYY-MM-DD         Optional. Defaults to current UTC date.
  output_filename    Optional. Defaults to proposals/<date>-<client-slug>-proposal.md

Notes:
  - Template path: docs/kumo-proposal-lead-response-accelerator-lr.md
  - Output directories are created automatically.
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  show_help
  exit 0
fi

CLIENT_NAME="${1:-}"
DATE="${2:-$(date -u +%F)}"
OUTPUT_FILE="${3:-}"
TEMPLATE="docs/kumo-proposal-lead-response-accelerator-lr.md"

if [[ -z "$CLIENT_NAME" ]]; then
  echo "Error: Client Name is required."
  echo
  show_help
  exit 1
fi

if [[ ! "$DATE" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
  echo "Error: Date must be in YYYY-MM-DD format. Got: $DATE"
  exit 1
fi

if [[ ! -f "$TEMPLATE" ]]; then
  echo "Error: Template not found at $TEMPLATE"
  exit 1
fi

slugify() {
  local input="$1"
  # Lowercase, replace non-alphanumeric sequences with '-', trim leading/trailing '-'
  echo "$input" \
    | tr '[:upper:]' '[:lower:]' \
    | sed -E 's/[^a-z0-9]+/-/g; s/^-+//; s/-+$//'
}

if [[ -z "$OUTPUT_FILE" ]]; then
  CLIENT_SLUG="$(slugify "$CLIENT_NAME")"
  OUTPUT_FILE="proposals/${DATE}-${CLIENT_SLUG}-proposal.md"
fi

mkdir -p "$(dirname "$OUTPUT_FILE")"

export CLIENT_NAME DATE
perl -pe 's/\{\{Client Name\}\}/$ENV{CLIENT_NAME}/g; s/\{\{Date\}\}/$ENV{DATE}/g' \
  "$TEMPLATE" > "$OUTPUT_FILE"

echo "Proposal generated: $OUTPUT_FILE"
