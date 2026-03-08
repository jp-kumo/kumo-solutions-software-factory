#!/usr/bin/env bash
set -euo pipefail

cd /home/jpadmin/.openclaw/workspace

# Pin auth/runtime paths for non-interactive cron consistency
export HOME="/home/jpadmin"
export XDG_CONFIG_HOME="/home/jpadmin/.config"
export XDG_DATA_HOME="/home/jpadmin/.local/share"

export GOG_ACCOUNT="jacquespayne.9914@gmail.com"
export GOG_CLIENT="default"

# Optional non-interactive keyring password source
if [[ -z "${GOG_KEYRING_PASSWORD:-}" && -f "/home/jpadmin/.openclaw/.secrets/gog_keyring_password" ]]; then
  export GOG_KEYRING_PASSWORD
  GOG_KEYRING_PASSWORD="$(tr -d '\r\n' < /home/jpadmin/.openclaw/.secrets/gog_keyring_password)"
fi

/usr/bin/python3 /home/jpadmin/.openclaw/workspace/scripts/personal_crm_intelligence.py --run
