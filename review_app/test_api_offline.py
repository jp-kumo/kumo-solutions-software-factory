import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.main import app
from backend.services import extract_video_id


class ApiOfflineTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch("backend.main.get_video_info")
    def test_post_info_success(self, mock_get_video_info):
        mock_get_video_info.return_value = {
            "title": "Sample",
            "thumbnail": "https://example.com/thumb.jpg",
            "duration": 123,
            "id": "abc123",
        }

        response = self.client.post(
            "/api/info", json={"url": "https://www.youtube.com/watch?v=abc123"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], "abc123")

    @patch("backend.main.download_video")
    def test_download_profile_passed_through(self, mock_download_video):
        mock_download_video.return_value = {
            "status": "success",
            "path": "/tmp/downloads",
            "quality_profile": "small",
        }

        response = self.client.post(
            "/api/download",
            json={
                "url": "https://www.youtube.com/watch?v=abc123",
                "quality_profile": "small",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["quality_profile"], "small")
        mock_download_video.assert_called_once()

    @patch("backend.main.download_video")
    def test_download_invalid_profile_returns_400(self, mock_download_video):
        mock_download_video.side_effect = ValueError("Unsupported quality profile 'ultra'.")

        response = self.client.get(
            "/api/download",
            params={
                "url": "https://www.youtube.com/watch?v=abc123",
                "quality_profile": "ultra",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("Unsupported quality profile", response.json()["detail"])

    @patch("backend.main.save_transcript")
    def test_transcript_invalid_format_returns_400(self, mock_save_transcript):
        mock_save_transcript.side_effect = ValueError("Unsupported format 'docx'.")

        response = self.client.post(
            "/api/transcript",
            json={
                "url": "https://www.youtube.com/watch?v=abc123",
                "video_id": "abc123",
                "title": "Sample Title",
                "fmt": "docx",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("Unsupported format", response.json()["detail"])

    @patch("backend.main.save_transcript")
    def test_transcript_provider_failure_returns_502(self, mock_save_transcript):
        mock_save_transcript.side_effect = RuntimeError("Error fetching transcript: upstream error")

        response = self.client.get(
            "/api/transcript",
            params={
                "url": "https://www.youtube.com/watch?v=abc123",
                "video_id": "abc123",
                "title": "Sample Title",
                "fmt": "txt",
            },
        )

        self.assertEqual(response.status_code, 502)
        self.assertIn("Error fetching transcript", response.json()["detail"])

    @patch("backend.main.load_preferences")
    def test_get_preferences(self, mock_load_preferences):
        mock_load_preferences.return_value = {
            "quality_profile": "best",
            "transcript_format": "md",
        }

        response = self.client.get("/api/preferences")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["quality_profile"], "best")
        self.assertEqual(response.json()["transcript_format"], "md")

    @patch("backend.main.save_preferences")
    def test_post_preferences(self, mock_save_preferences):
        mock_save_preferences.return_value = {
            "quality_profile": "small",
            "transcript_format": "pdf",
        }

        response = self.client.post(
            "/api/preferences",
            json={"quality_profile": "small", "transcript_format": "pdf"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["quality_profile"], "small")
        self.assertEqual(response.json()["transcript_format"], "pdf")

    @patch("backend.main.save_transcript")
    def test_transcript_post_without_video_id(self, mock_save_transcript):
        mock_save_transcript.return_value = {
            "status": "success",
            "file": "/tmp/sample.txt",
        }

        response = self.client.post(
            "/api/transcript",
            json={
                "url": "https://www.youtube.com/watch?v=abc123",
                "title": "Sample Title",
                "fmt": "txt",
            },
        )

        self.assertEqual(response.status_code, 200)
        mock_save_transcript.assert_called_once_with(
            None,
            "Sample Title",
            "txt",
            "https://www.youtube.com/watch?v=abc123",
        )


class ServiceHelperTests(unittest.TestCase):
    def test_extract_video_id_variants(self):
        cases = {
            "https://www.youtube.com/watch?v=abc123XYZ_0": "abc123XYZ_0",
            "https://youtu.be/abc123XYZ_0": "abc123XYZ_0",
            "https://www.youtube.com/shorts/abc123XYZ_0": "abc123XYZ_0",
            "https://www.youtube.com/embed/abc123XYZ_0": "abc123XYZ_0",
            "https://www.youtube.com/live/abc123XYZ_0": "abc123XYZ_0",
        }

        for url, expected in cases.items():
            with self.subTest(url=url):
                self.assertEqual(extract_video_id(url), expected)

    def test_extract_video_id_rejects_invalid_ids(self):
        invalid_cases = [
            "https://www.youtube.com/watch?v=short",
            "https://youtu.be/toolongvideoid123",
            "https://www.youtube.com/watch?v=abc123XYZ!0",
            "https://example.com/watch?v=abc123XYZ_0",
        ]

        for url in invalid_cases:
            with self.subTest(url=url):
                self.assertIsNone(extract_video_id(url))


if __name__ == "__main__":
    unittest.main()
