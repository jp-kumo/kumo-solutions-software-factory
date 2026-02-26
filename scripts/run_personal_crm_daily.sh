#!/usr/bin/env bash
set -euo pipefail

cd /home/jpadmin/.openclaw/workspace

export GOG_ACCOUNT="jacquespayne.9914@gmail.com"

# Optional non-interactive keyring password source
if [[ -z "${GOG_KEYRING_PASSWORD:-}" && -f "/home/jpadmin/.openclaw/.secrets/gog_keyring_password" ]]; then
  export GOG_KEYRING_PASSWORD
  GOG_KEYRING_PASSWORD="$(cat /home/jpadmin/.openclaw/.secrets/gog_keyring_password)"
fi

/usr/bin/python3 /home/jpadmin/.openclaw/workspace/scripts/personal_crm_intelligence.py --run
