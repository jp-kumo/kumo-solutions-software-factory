#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APP_DIR="$ROOT_DIR/review_app"
VENV_DIR="$APP_DIR/.venv-nightly"

cd "$APP_DIR"

echo "[1/4] Running Python syntax checks..."
python3 -m py_compile backend/main.py backend/services.py test_api_offline.py

echo "[2/4] Running backend offline unit tests..."
if python3 -m venv "$VENV_DIR" >/dev/null 2>&1; then
  source "$VENV_DIR/bin/activate"
  pip install --upgrade pip >/dev/null
  pip install -r backend/requirements.txt >/dev/null
  python -m unittest -q test_api_offline.py
  deactivate
else
  echo "python3-venv unavailable; using existing local virtualenv if present..."
  if [[ -f "$APP_DIR/.venv/bin/python" ]]; then
    if "$APP_DIR/.venv/bin/python" -c "import fastapi" >/dev/null 2>&1; then
      "$APP_DIR/.venv/bin/python" -m unittest -q test_api_offline.py
    else
      echo "Local .venv missing backend deps; skipping backend unit tests."
    fi
  elif [[ -f "$APP_DIR/venv/bin/python" ]]; then
    if "$APP_DIR/venv/bin/python" -c "import fastapi" >/dev/null 2>&1; then
      "$APP_DIR/venv/bin/python" -m unittest -q test_api_offline.py
    else
      echo "Local venv missing backend deps; skipping backend unit tests."
    fi
  else
    echo "No usable virtualenv found; skipping backend unit tests."
  fi
fi

echo "[3/4] Running frontend build validation..."
cd "$APP_DIR/frontend"
npm ci --silent
npm run build --silent

echo "[4/4] Nightly check complete: validations finished."
