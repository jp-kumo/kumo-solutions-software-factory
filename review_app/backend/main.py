import os
import socket
import subprocess
import threading
from pathlib import Path

import uvicorn
import webview
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, HttpUrl

from backend.services import download_video, get_video_info, save_transcript

app = FastAPI(title="YT Downloader API", version="1.0.0")

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


class TranscriptRequest(BaseModel):
    url: HttpUrl
    video_id: str
    title: str
    fmt: str


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/info")
def info(url: str):
    # Backward-compatible GET endpoint
    return get_video_info(url)


@app.post("/api/info")
def info_post(payload: UrlRequest):
    return get_video_info(str(payload.url))


@app.get("/api/download")
def download(url: str):
    # Backward-compatible GET endpoint
    return download_video(url)


@app.post("/api/download")
def download_post(payload: UrlRequest):
    return download_video(str(payload.url))


@app.get("/api/transcript")
def transcript(url: str, video_id: str, title: str, fmt: str):
    # Backward-compatible GET endpoint
    return save_transcript(video_id, title, fmt, url)


@app.post("/api/transcript")
def transcript_post(payload: TranscriptRequest):
    return save_transcript(payload.video_id, payload.title, payload.fmt, str(payload.url))


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
