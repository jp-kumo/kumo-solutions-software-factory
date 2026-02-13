#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APP_DIR="$ROOT_DIR/review_app"

cd "$APP_DIR"

echo "Running syntax checks..."
python3 -m py_compile backend/main.py backend/services.py test_api_offline.py

echo "Syntax checks passed."

if python3 -m venv .venv >/dev/null 2>&1; then
  source .venv/bin/activate
  pip install --upgrade pip >/dev/null
  pip install -r backend/requirements.txt >/dev/null
  python -m unittest -q test_api_offline.py
  echo "Nightly check complete: offline API tests passed."
else
  echo "Nightly check partial: python3-venv unavailable on host, skipped unit tests."
fi
