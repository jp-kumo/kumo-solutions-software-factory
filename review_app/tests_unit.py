import unittest

from backend.services import extract_video_id


class ExtractVideoIdTests(unittest.TestCase):
    def test_supported_youtube_variants(self):
        cases = {
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ": "dQw4w9WgXcQ",
            "https://m.youtube.com/watch?v=dQw4w9WgXcQ": "dQw4w9WgXcQ",
            "https://music.youtube.com/watch?v=dQw4w9WgXcQ": "dQw4w9WgXcQ",
            "https://youtu.be/dQw4w9WgXcQ": "dQw4w9WgXcQ",
            "https://www.youtube.com/embed/dQw4w9WgXcQ": "dQw4w9WgXcQ",
            "https://www.youtube.com/shorts/dQw4w9WgXcQ": "dQw4w9WgXcQ",
            "https://www.youtube.com/live/dQw4w9WgXcQ": "dQw4w9WgXcQ",
            "https://www.youtube-nocookie.com/embed/dQw4w9WgXcQ": "dQw4w9WgXcQ",
        }
        for url, expected in cases.items():
            with self.subTest(url=url):
                self.assertEqual(extract_video_id(url), expected)

    def test_rejects_non_youtube_hosts_and_invalid_ids(self):
        cases = [
            "https://google.com/watch?v=dQw4w9WgXcQ",
            "https://youtu.be/not-valid",
            "https://www.youtube.com/watch?v=too_short",
            "invalid",
            "",
        ]
        for url in cases:
            with self.subTest(url=url):
                self.assertIsNone(extract_video_id(url))


if __name__ == "__main__":
    unittest.main()
