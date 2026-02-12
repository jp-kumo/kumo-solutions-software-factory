import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.main import app


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


if __name__ == "__main__":
    unittest.main()
