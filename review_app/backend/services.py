import os
import re
import textwrap
from pathlib import Path
from typing import Optional

import yt_dlp
from fpdf import FPDF
from youtube_transcript_api import YouTubeTranscriptApi

DOWNLOAD_DIR = os.environ.get(
    "DOWNLOAD_DIR", str(Path.home() / "Downloads" / "YT_Downloader")
)
Path(DOWNLOAD_DIR).mkdir(parents=True, exist_ok=True)

ALLOWED_TRANSCRIPT_FORMATS = {"txt", "md", "pdf"}
QUALITY_PROFILES = {
    "best": "bestvideo*+bestaudio/best",
    "balanced": "best[ext=mp4]/best",
    "small": "worst[ext=mp4]/worst",
}


def _safe_filename(name: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9 _.-]", "", name).strip()
    return cleaned or "video"


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


def get_video_info(url: str):
    ydl_opts = {"quiet": True, "noplaylist": True}
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

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return {"status": "success", "path": DOWNLOAD_DIR, "quality_profile": profile}


def get_transcript_text(video_id: str):
    try:
        # Primary path
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    except AttributeError:
        # Compatibility path with instantiated API
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


def save_transcript(video_id: str, title: str, fmt: str, url: str):
    fmt = (fmt or "").lower().strip()
    if fmt not in ALLOWED_TRANSCRIPT_FORMATS:
        raise ValueError(f"Unsupported format '{fmt}'. Use one of: {sorted(ALLOWED_TRANSCRIPT_FORMATS)}")

    text = get_transcript_text(video_id)
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
