import unittest
from unittest.mock import patch

import config
from extractors.youtube import YouTubeExtractor


class YouTubeProvenanceTests(unittest.TestCase):
    def test_automated_extraction_fails_when_no_video_captions_are_available(self):
        extractor = YouTubeExtractor()
        with (
            patch.object(config, "CI_MODE", True),
            patch.object(config, "XAI_API_KEY", "present-but-not-valid"),
            patch("extractors.youtube._fetch_youtube_snippet", return_value={}),
            patch.object(extractor, "_extract_via_transcript_api", side_effect=RuntimeError("no captions")),
            patch.object(extractor, "_extract_via_ytdlp", side_effect=RuntimeError("no subtitles")),
        ):
            with self.assertRaisesRegex(RuntimeError, "No verifiable YouTube captions"):
                extractor.extract("https://www.youtube.com/watch?v=YqREHU0pvUc")


if __name__ == "__main__":
    unittest.main()
