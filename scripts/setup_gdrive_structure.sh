#!/usr/bin/env bash
set -euo pipefail

GOG_BIN="/home/jpadmin/.local/bin/gog"
ACCOUNT="jacquespayne.9914@gmail.com"

mk() {
  local name="$1"
  local parent="${2:-}"
  if [[ -n "$parent" ]]; then
    "$GOG_BIN" drive mkdir "$name" --account "$ACCOUNT" --parent "$parent" --json \
      | python3 -c 'import sys, json; d=json.load(sys.stdin); print(d.get("id",""))'
  else
    "$GOG_BIN" drive mkdir "$name" --account "$ACCOUNT" --json \
      | python3 -c 'import sys, json; d=json.load(sys.stdin); print(d.get("id",""))'
  fi
}

echo "Creating Google Drive structure for ${ACCOUNT}..."
ROOT_ID=$(mk "Jacques-Agent-Ops")
echo "ROOT_ID=$ROOT_ID"

INBOX_ID=$(mk "00-Inbox" "$ROOT_ID")
KNOW_ID=$(mk "01-Knowledge-Hub" "$ROOT_ID")
EXEC_ID=$(mk "02-Execution" "$ROOT_ID")
DELIV_ID=$(mk "03-Deliverables" "$ROOT_ID")
CLIENT_ID=$(mk "04-Client Work" "$ROOT_ID")
ARCHIVE_ID=$(mk "99-Archive" "$ROOT_ID")

mk "New Resources" "$INBOX_ID" >/dev/null
mk "To Process" "$INBOX_ID" >/dev/null

KC_ID=$(mk "Knowledge Cards" "$KNOW_ID")
mk "Playbooks" "$KNOW_ID" >/dev/null
mk "Prompt Templates" "$KNOW_ID" >/dev/null

mk "Portfolio Build" "$EXEC_ID" >/dev/null
mk "Fiverr Offers" "$EXEC_ID" >/dev/null
mk "Lead Pipeline" "$EXEC_ID" >/dev/null
mk "Market Signals" "$EXEC_ID" >/dev/null

mk "Slide Decks" "$DELIV_ID" >/dev/null
mk "Reports" "$DELIV_ID" >/dev/null
mk "Video Overviews" "$DELIV_ID" >/dev/null
mk "Data Tables" "$DELIV_ID" >/dev/null

mk "Prospects" "$CLIENT_ID" >/dev/null
mk "Active Engagements" "$CLIENT_ID" >/dev/null

# Upload starter knowledge docs
"$GOG_BIN" drive upload "/home/jpadmin/.openclaw/workspace/docs/google-drive-knowledge-structure.md" --account "$ACCOUNT" --parent "$KC_ID" >/dev/null
"$GOG_BIN" drive upload "/home/jpadmin/.openclaw/workspace/docs/knowledge/notebooklm-gemini-consulting-playbook.md" --account "$ACCOUNT" --parent "$KC_ID" >/dev/null

# Optional: upload the source PDF from this session if present
PDF_SRC="/home/jpadmin/.openclaw/media/inbound/file_45---cd240d4a-6614-48db-8d52-5249f750993f.pdf"
if [[ -f "$PDF_SRC" ]]; then
  "$GOG_BIN" drive upload "$PDF_SRC" --account "$ACCOUNT" --parent "$INBOX_ID" --name "resource-notebooklm-gemini-consulting.pdf" >/dev/null
fi

echo "Done."
echo "Created root folder ID: $ROOT_ID"
