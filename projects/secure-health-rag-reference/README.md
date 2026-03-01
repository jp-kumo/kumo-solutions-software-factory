# Secure Health RAG Reference

A hiring-focused reference project demonstrating secure-by-design GenAI patterns for healthcare-style data handling.

## Why this project exists
Most GenAI demos ignore production controls. This project shows practical controls for:
- sanitize-before-embed
- tenant/patient-scoped retrieval
- guardrailed generation + structured outputs
- PHI-safe audit logging

## Quickstart (uv)
```bash
uv venv
source .venv/bin/activate
uv sync --extra dev
cp .env.example .env
uv run uvicorn app.main:app --reload --port 8000
```

## Run tests
```bash
uv run pytest
```

## Demo endpoint
- `GET /health`
- `GET /patients/{patient_id}/report`

Use headers for context simulation:
- `x-role: clinician`
- `x-tenant: tenant-demo`
- `x-patient: patient-demo`
- `x-scope: reports:read`
- `x-request-id: req-123`

## Limitations
- Mock data only; not for clinical use.
- No real Bedrock call yet (deterministic generator for MVP).
