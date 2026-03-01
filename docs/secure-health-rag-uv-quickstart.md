# Secure Health RAG — uv Quickstart

## 1) Initialize project
```bash
mkdir -p secure-health-rag-reference && cd secure-health-rag-reference
uv init --python 3.12
```

## 2) Replace generated pyproject
Copy `docs/secure-health-rag-pyproject.toml` into your project root as `pyproject.toml`.

## 3) Create virtual env + install deps
```bash
uv venv
source .venv/bin/activate
uv sync --extra dev
```

## 4) Create env file
```bash
cp /home/jpadmin/.openclaw/workspace/docs/secure-health-rag-.env.example .env
```
Fill placeholders (do not commit secrets).

## 5) Run app
```bash
uv run uvicorn app.main:app --reload --port 8000
```

## 6) Run tests/lint
```bash
uv run pytest
uv run ruff check .
```

## Notes
- Prefer `uv run <command>` to guarantee environment consistency.
- Commit `.env.example` only; never commit `.env`.
- Keep credentials in a secrets manager for non-local environments.
