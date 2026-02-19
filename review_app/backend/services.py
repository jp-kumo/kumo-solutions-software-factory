import json
import os
import re
import textwrap
from pathlib import Path
from typing import Optional
from urllib.parse import parse_qs, urlparse


DOWNLOAD_DIR = os.environ.get(
    "DOWNLOAD_DIR", str(Path.home() / "Downloads" / "YT_Downloader")
)
Path(DOWNLOAD_DIR).mkdir(parents=True, exist_ok=True)

PREFERENCES_PATH = Path(
    os.environ.get(
        "YT_DOWNLOADER_PREFS_PATH",
        str(Path.home() / ".config" / "yt_downloader" / "preferences.json"),
    )
)

ALLOWED_TRANSCRIPT_FORMATS = {"txt", "md", "pdf"}
VIDEO_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]{11}$")
QUALITY_PROFILES = {
    "best": "bestvideo*+bestaudio/best",
    "balanced": "best[ext=mp4]/best",
    "small": "worst[ext=mp4]/worst",
}
DEFAULT_PREFERENCES = {
    "quality_profile": "balanced",
    "transcript_format": "txt",
}


def _require_yt_dlp():
    try:
        import yt_dlp  # type: ignore
    except Exception as exc:
        raise RuntimeError("yt-dlp is not installed. Install backend dependencies.") from exc
    return yt_dlp


def _require_transcript_api():
    try:
        from youtube_transcript_api import YouTubeTranscriptApi  # type: ignore
    except Exception as exc:
        raise RuntimeError("youtube-transcript-api is not installed. Install backend dependencies.") from exc
    return YouTubeTranscriptApi


def _require_fpdf():
    try:
        from fpdf import FPDF  # type: ignore
    except Exception as exc:
        raise RuntimeError("fpdf2 is not installed. Install backend dependencies.") from exc
    return FPDF


def _safe_filename(name: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9 _.-]", "", name).strip()
    return cleaned or "video"


def _normalize_video_id(candidate: Optional[str]) -> Optional[str]:
    if not candidate:
        return None

    trimmed = candidate.strip()
    if VIDEO_ID_PATTERN.match(trimmed):
        return trimmed
    return None


def _is_allowed_host(host: str, root: str) -> bool:
    return host == root or host.endswith(f".{root}")


def extract_video_id(url: str) -> Optional[str]:
    """Extract a YouTube video ID from common URL variants."""
    if not url:
        return None

    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()

    if _is_allowed_host(host, "youtu.be"):
        candidate = parsed.path.strip("/").split("/")[0]
        return _normalize_video_id(candidate)

    if _is_allowed_host(host, "youtube.com") or _is_allowed_host(host, "youtube-nocookie.com"):
        if parsed.path == "/watch":
            candidate = parse_qs(parsed.query).get("v", [None])[0]
            return _normalize_video_id(candidate)

        if (
            parsed.path.startswith("/shorts/")
            or parsed.path.startswith("/embed/")
            or parsed.path.startswith("/live/")
        ):
            parts = [part for part in parsed.path.split("/") if part]
            if len(parts) >= 2:
                return _normalize_video_id(parts[1])

    return None


def _ffmpeg_location_if_local() -> Optional[str]:
    ffmpeg_binary = Path(__file__).resolve().parent / "ffmpeg"
    if ffmpeg_binary.exists():
        return str(ffmpeg_binary.parent)
    return None


def _resolve_quality_profile(profile: str) -> str:
    normalized = (profile or "balanced").lower().strip()
    if normalized not in QUALITY_PROFILES:
        raise ValueError(
            f"Unsupported quality profile '{profile}'. "
            f"Use one of: {sorted(QUALITY_PROFILES.keys())}"
        )
    return normalized


def _resolve_transcript_format(fmt: str) -> str:
    normalized = (fmt or "txt").lower().strip()
    if normalized not in ALLOWED_TRANSCRIPT_FORMATS:
        raise ValueError(
            f"Unsupported format '{fmt}'. Use one of: {sorted(ALLOWED_TRANSCRIPT_FORMATS)}"
        )
    return normalized


def _normalize_preferences(data: dict) -> dict:
    quality_profile = _resolve_quality_profile(data.get("quality_profile", DEFAULT_PREFERENCES["quality_profile"]))
    transcript_format = _resolve_transcript_format(data.get("transcript_format", DEFAULT_PREFERENCES["transcript_format"]))
    return {
        "quality_profile": quality_profile,
        "transcript_format": transcript_format,
    }


def load_preferences() -> dict:
    if not PREFERENCES_PATH.exists():
        return DEFAULT_PREFERENCES.copy()

    try:
        raw = json.loads(PREFERENCES_PATH.read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            return DEFAULT_PREFERENCES.copy()
        return _normalize_preferences(raw)
    except Exception:
        return DEFAULT_PREFERENCES.copy()


def save_preferences(preferences: dict) -> dict:
    normalized = _normalize_preferences(preferences)
    PREFERENCES_PATH.parent.mkdir(parents=True, exist_ok=True)
    PREFERENCES_PATH.write_text(json.dumps(normalized, indent=2), encoding="utf-8")
    return normalized


def get_video_info(url: str):
    ydl_opts = {"quiet": True, "noplaylist": True}
    yt_dlp = _require_yt_dlp()
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return {
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail"),
            "duration": info.get("duration"),
            "id": info.get("id"),
        }


def download_video(url: str, quality_profile: str = "balanced"):
    profile = _resolve_quality_profile(quality_profile)

    ydl_opts = {
        "format": QUALITY_PROFILES[profile],
        "outtmpl": str(Path(DOWNLOAD_DIR) / "%(title)s.%(ext)s"),
        "overwrites": True,
        "noplaylist": True,
    }

    ffmpeg_location = _ffmpeg_location_if_local()
    if ffmpeg_location:
        ydl_opts["ffmpeg_location"] = ffmpeg_location

    yt_dlp = _require_yt_dlp()
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return {"status": "success", "path": DOWNLOAD_DIR, "quality_profile": profile}


def get_transcript_text(video_id: str):
    try:
        # Primary path
        YouTubeTranscriptApi = _require_transcript_api()
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    except AttributeError:
        # Compatibility path with instantiated API
        YouTubeTranscriptApi = _require_transcript_api()
        api = YouTubeTranscriptApi()
        transcript_objects = api.fetch(video_id)
        transcript_list = []
        for t in transcript_objects:
            if hasattr(t, "text"):
                transcript_list.append(
                    {"text": t.text, "start": t.start, "duration": t.duration}
                )
            else:
                transcript_list.append(t)
    except Exception as exc:
        raise RuntimeError(f"Error fetching transcript: {exc}") from exc

    return " ".join(item["text"] for item in transcript_list)


def save_transcript(video_id: Optional[str], title: str, fmt: str, url: str):
    fmt = _resolve_transcript_format(fmt)

    resolved_video_id = _normalize_video_id(video_id) if video_id else extract_video_id(url)
    if video_id and not resolved_video_id:
        raise ValueError(
            "Invalid video_id. Expected 11 characters using letters, numbers, '-' or '_'."
        )

    if not resolved_video_id:
        raise ValueError(
            "Missing video_id and could not extract a valid 11-character ID from URL. "
            "Use a full YouTube URL or provide video_id explicitly."
        )

    text = get_transcript_text(resolved_video_id)
    safe_title = _safe_filename(title)
    filepath = Path(DOWNLOAD_DIR) / f"{safe_title}_transcript.{fmt}"

    if fmt == "txt":
        wrapped_text = textwrap.fill(text, width=80)
        final_content = f"{title}\nSource: {url}\n\n{wrapped_text}"
        filepath.write_text(final_content, encoding="utf-8")

    elif fmt == "md":
        final_content = f"# {title}\n\n**Source**: {url}\n\n{text}"
        filepath.write_text(final_content, encoding="utf-8")

    elif fmt == "pdf":

        FPDF = _require_fpdf()

        class PDF(FPDF):
            def footer(self):
                self.set_y(-15)
                self.set_font("Arial", "I", 8)
                self.cell(0, 10, f"Page {self.page_no()} of {{nb}}", align="C")

            def header(self):
                if hasattr(self, "custom_title"):
                    self.set_font("Arial", "B", 10)
                    self.cell(0, 10, self.custom_title, align="L", ln=1)

                    self.set_font("Arial", size=10)
                    self.cell(0, 10, f"Source: {self.custom_url}", 0, 1, "L")
                    self.ln(4)

        pdf = PDF()
        pdf.alias_nb_pages()
        pdf.set_left_margin(25.4)
        pdf.set_right_margin(25.4)
        pdf.set_top_margin(25.4)
        pdf.set_auto_page_break(auto=True, margin=25.4)

        pdf.custom_title = title
        pdf.custom_url = url

        pdf.add_page()
        pdf.set_font("Arial", size=12)

        clean_text = text.encode("latin-1", "replace").decode("latin-1")
        pdf.multi_cell(0, 5, clean_text)
        pdf.output(str(filepath))

    return {"status": "success", "file": str(filepath)}
