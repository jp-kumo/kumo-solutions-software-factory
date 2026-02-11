# YT Downloader Pro (stabilized v1)

A desktop/web hybrid app to fetch YouTube metadata, download MP4 files, and export transcripts (`txt`, `md`, `pdf`).

## What was stabilized

- Added safer backend handling for local ffmpeg permissions (no raw shell command strings).
- Added request models + `POST` endpoints (`/api/info`, `/api/download`, `/api/transcript`) while keeping old `GET` routes for compatibility.
- Added backend health endpoint: `GET /api/health`.
- Improved transcript format validation and filename sanitization.
- Updated frontend to call `POST` APIs and display backend error details when available.
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
- `POST /api/info` with body `{ "url": "https://..." }`
- `POST /api/download` with body `{ "url": "https://..." }`
- `POST /api/transcript` with body:
  ```json
  {
    "url": "https://...",
    "video_id": "abc123",
    "title": "Video title",
    "fmt": "txt"
  }
  ```

Supported transcript formats: `txt`, `md`, `pdf`.

## Next recommended improvements

1. Add API tests (success + failure paths).
2. Add explicit input validation and friendlier error codes for transcript-not-available cases.
3. Add configurable download quality profiles.
4. Add background job/progress reporting for long downloads.
5. Add persistent app settings (download path, preferred transcript format).
