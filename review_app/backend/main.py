import os
import socket
import subprocess
import threading
from pathlib import Path

import uvicorn
import webview
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, HttpUrl

from backend.services import (
    ALLOWED_TRANSCRIPT_FORMATS,
    QUALITY_PROFILES,
    download_video,
    get_video_info,
    load_preferences,
    save_preferences,
    save_transcript,
)

app = FastAPI(title="YT Downloader API", version="1.2.0")

# Development-friendly CORS. Tighten in production if exposed remotely.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UrlRequest(BaseModel):
    url: HttpUrl


class DownloadRequest(BaseModel):
    url: HttpUrl
    quality_profile: str = "balanced"


class TranscriptRequest(BaseModel):
    url: HttpUrl
    video_id: str
    title: str
    fmt: str


class PreferencesRequest(BaseModel):
    quality_profile: str
    transcript_format: str


def _handle_service_error(exc: Exception) -> None:
    """Convert service-layer exceptions into API-friendly HTTP errors."""
    if isinstance(exc, ValueError):
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    # Network/provider failures from transcript/video fetches
    if isinstance(exc, RuntimeError):
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    raise HTTPException(status_code=500, detail="Internal server error") from exc


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/settings")
def settings():
    prefs = load_preferences()
    return {
        "quality_profiles": sorted(QUALITY_PROFILES.keys()),
        "transcript_formats": sorted(ALLOWED_TRANSCRIPT_FORMATS),
        "default_quality_profile": prefs["quality_profile"],
        "default_transcript_format": prefs["transcript_format"],
    }


@app.get("/api/preferences")
def preferences_get():
    return load_preferences()


@app.post("/api/preferences")
def preferences_post(payload: PreferencesRequest):
    try:
        return save_preferences(payload.model_dump())
    except Exception as exc:
        _handle_service_error(exc)


@app.get("/api/info")
def info(url: str):
    # Backward-compatible GET endpoint
    try:
        return get_video_info(url)
    except Exception as exc:
        _handle_service_error(exc)


@app.post("/api/info")
def info_post(payload: UrlRequest):
    try:
        return get_video_info(str(payload.url))
    except Exception as exc:
        _handle_service_error(exc)


@app.get("/api/download")
def download(url: str, quality_profile: str = "balanced"):
    # Backward-compatible GET endpoint
    try:
        return download_video(url, quality_profile)
    except Exception as exc:
        _handle_service_error(exc)


@app.post("/api/download")
def download_post(payload: DownloadRequest):
    try:
        return download_video(str(payload.url), payload.quality_profile)
    except Exception as exc:
        _handle_service_error(exc)


@app.get("/api/transcript")
def transcript(url: str, video_id: str, title: str, fmt: str):
    # Backward-compatible GET endpoint
    try:
        return save_transcript(video_id, title, fmt, url)
    except Exception as exc:
        _handle_service_error(exc)


@app.post("/api/transcript")
def transcript_post(payload: TranscriptRequest):
    try:
        return save_transcript(payload.video_id, payload.title, payload.fmt, str(payload.url))
    except Exception as exc:
        _handle_service_error(exc)


frontend_dist = Path(__file__).resolve().parent.parent / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dist), html=True), name="static")


def find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


def start_server(port: int):
    config = uvicorn.Config(app, host="127.0.0.1", port=port, log_level="info")
    server = uvicorn.Server(config)
    server.install_signal_handlers = lambda: None
    server.run()


def ensure_local_ffmpeg_permissions() -> None:
    """
    Optional helper for desktop mode.
    If a bundled ffmpeg binary exists, mark executable on macOS/Linux.
    """
    ffmpeg_path = Path(__file__).resolve().parent / "ffmpeg"
    if not ffmpeg_path.exists():
        return

    try:
        ffmpeg_path.chmod(0o755)
    except Exception as exc:
        print(f"Warning: could not chmod ffmpeg: {exc}")

    # macOS-only quarantine cleanup
    if os.uname().sysname == "Darwin":
        try:
            subprocess.run(
                ["xattr", "-d", "com.apple.quarantine", str(ffmpeg_path)],
                check=False,
                capture_output=True,
                text=True,
            )
        except Exception as exc:
            print(f"Warning: could not clear quarantine attribute: {exc}")


if __name__ == "__main__":
    ensure_local_ffmpeg_permissions()

    port = 8000
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("127.0.0.1", port))
    except OSError:
        print(f"⚠️ Port {port} is busy. Finding a free port...")
        port = find_free_port()

    t = threading.Thread(target=start_server, args=(port,), daemon=True)
    t.start()

    print(f"🚀 Server starting on http://127.0.0.1:{port}")
    print("🖥️  Launching native window...")

    try:
        webview.create_window("YT Downloader", f"http://127.0.0.1:{port}", width=1200, height=800)
        webview.start()
    except Exception as exc:
        print(f"❌ Failed to start window: {exc}")
