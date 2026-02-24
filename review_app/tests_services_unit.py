import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import backend.services as services


class PreferencesTests(unittest.TestCase):
    def test_load_preferences_returns_defaults_when_file_missing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            prefs_path = Path(tmpdir) / "prefs.json"
            with patch.object(services, "PREFERENCES_PATH", prefs_path):
                self.assertEqual(services.load_preferences(), services.DEFAULT_PREFERENCES)

    def test_load_preferences_returns_defaults_on_invalid_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            prefs_path = Path(tmpdir) / "prefs.json"
            prefs_path.write_text("{not-json", encoding="utf-8")
            with patch.object(services, "PREFERENCES_PATH", prefs_path):
                self.assertEqual(services.load_preferences(), services.DEFAULT_PREFERENCES)

    def test_save_preferences_normalizes_values(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            prefs_path = Path(tmpdir) / "prefs.json"
            with patch.object(services, "PREFERENCES_PATH", prefs_path):
                saved = services.save_preferences(
                    {"quality_profile": " BEST ", "transcript_format": " PDF "}
                )
                self.assertEqual(
                    saved,
                    {"quality_profile": "best", "transcript_format": "pdf"},
                )

                loaded = json.loads(prefs_path.read_text(encoding="utf-8"))
                self.assertEqual(loaded["quality_profile"], "best")
                self.assertEqual(loaded["transcript_format"], "pdf")


class ValidationTests(unittest.TestCase):
    def test_quality_profile_validation_rejects_unknown_value(self):
        with self.assertRaises(ValueError):
            services._resolve_quality_profile("ultra")

    def test_transcript_format_validation_rejects_unknown_value(self):
        with self.assertRaises(ValueError):
            services._resolve_transcript_format("docx")

    def test_save_transcript_rejects_invalid_explicit_video_id(self):
        with self.assertRaises(ValueError):
            services.save_transcript(
                video_id="bad",
                title="Sample",
                fmt="txt",
                url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            )

    def test_save_transcript_rejects_non_youtube_url_when_video_id_missing(self):
        with self.assertRaises(ValueError):
            services.save_transcript(
                video_id=None,
                title="Sample",
                fmt="txt",
                url="https://example.com/video?id=123",
            )


if __name__ == "__main__":
    unittest.main()
