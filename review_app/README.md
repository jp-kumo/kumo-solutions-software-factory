# YT Downloader Pro (stabilized v1)

A desktop/web hybrid app to fetch YouTube metadata, download MP4 files, and export transcripts (`txt`, `md`, `pdf`).

## What was stabilized

- Added safer backend handling for local ffmpeg permissions (no raw shell command strings).
- Added request models + `POST` endpoints (`/api/info`, `/api/download`, `/api/transcript`) while keeping old `GET` routes for compatibility.
- Added backend health endpoint: `GET /api/health`.
- Improved transcript format validation and filename sanitization.
- Added persisted user preferences (`quality_profile`, `transcript_format`) with new API endpoints.
- Updated frontend to call `POST` APIs, load backend settings dynamically, support quality-profile selection, and one-click download using default transcript format.
- Added `.gitignore` to avoid committing heavy/local artifacts (`venv`, zips, build outputs).

## Project structure

- `backend/` FastAPI service + download/transcript logic
- `frontend/` React + Vite UI
- `Dockerfile` multi-stage build (frontend + backend)
- `docker-compose.yml` containerized run

## Local run (dev)

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

By default, Vite dev server should proxy to backend (configure in `vite.config.js` if needed).

## Docker run

```bash
docker compose up --build
```

Then open: `http://localhost:8000`

## API summary

- `GET /api/health`
- `GET /api/settings` (supported transcript formats + download quality profiles + defaults)
- `GET /api/preferences`
- `POST /api/preferences` with body `{ "quality_profile": "balanced", "transcript_format": "txt" }`
- `POST /api/info` with body `{ "url": "https://..." }`
- `POST /api/download` with body `{ "url": "https://...", "quality_profile": "balanced" }`
  - quality profiles: `best`, `balanced`, `small`
- `POST /api/transcript` with body:
  ```json
  {
    "url": "https://...",
    "video_id": "abc123", // optional if URL includes YouTube ID
    "title": "Video title",
    "fmt": "txt"
  }
  ```

Supported transcript formats: `txt`, `md`, `pdf`.

## Test the API (offline-friendly)

A lightweight offline test file is included so basic API behavior can be validated without calling YouTube:

```bash
cd review_app
python3 test_api_offline.py
```

The tests mock service calls and verify:
- success behavior for `/api/info`
- download quality profile passthrough + invalid profile handling
- `400` mapping for invalid transcript format
- `502` mapping for upstream transcript/provider failures

Nightly/local check helper (from workspace root):
```bash
./scripts/review_app_nightly_check.sh
```
This runs Python syntax checks, backend offline tests in an isolated venv, and a frontend production build smoke test (`npm ci && npm run build`).

## Next recommended improvements

1. Add end-to-end integration tests behind an optional network flag.
2. Add background job/progress reporting for long downloads.
3. Add persistent app settings (download path, preferred transcript format + quality profile).
4. Add frontend controls for selecting quality profile before download.
