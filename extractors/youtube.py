"""YouTube video extraction via captions or manual paste."""

import html
import logging
import re
import sys
import tempfile
import urllib.request
import json
from pathlib import Path

import config
from extractors.base import BaseExtractor, ExtractionResult
from extractors.detector import extract_video_id

log = logging.getLogger("megamind.youtube")


class YouTubeExtractor(BaseExtractor):
    """Extract YouTube video content via captions or manual paste."""

    def extract(self, url: str) -> ExtractionResult:
        video_id = extract_video_id(url)
        canonical_url = f"https://www.youtube.com/watch?v={video_id}" if video_id else url
        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg" if video_id else ""
        snippet = _fetch_youtube_snippet(canonical_url)

        # Use captions tied to this video ID. A model's account of a URL is not
        # evidence that it actually accessed that video's content.
        if video_id:
            try:
                return self._extract_via_transcript_api(
                    canonical_url, video_id, thumbnail_url, snippet,
                )
            except Exception as exc:
                log.warning("YouTube transcript extraction failed for %s: %s", canonical_url, exc)
            try:
                return self._extract_via_ytdlp(
                    canonical_url, video_id, thumbnail_url, snippet,
                )
            except Exception as exc:
                log.warning("yt-dlp subtitle extraction failed for %s: %s", canonical_url, exc)

        # In CI mode, can't prompt for input
        if config.CI_MODE:
            raise RuntimeError(
                "No verifiable YouTube captions were available for this video. "
                "Refusing to generate an extraction from the URL alone."
            )

        # Fall back to manual paste
        return self._extract_via_paste(canonical_url, thumbnail_url)

    def _extract_via_transcript_api(
        self,
        url: str,
        video_id: str,
        thumbnail_url: str = "",
        snippet: dict | None = None,
    ) -> ExtractionResult:
        """Use YouTube captions as the raw extraction source."""
        from youtube_transcript_api import YouTubeTranscriptApi

        transcript = YouTubeTranscriptApi().fetch(
            video_id,
            languages=("en", "en-US", "en-GB", "en-AU"),
            preserve_formatting=False,
        )
        rows = transcript.to_raw_data()
        transcript_text = _format_transcript(rows)
        if len(transcript_text) < 500:
            raise RuntimeError("Transcript was too short to analyse reliably")

        snippet = snippet or {}
        title = snippet.get("title") or _extract_title("", url)
        channel = snippet.get("channelTitle", "Unknown")
        published_at = snippet.get("publishedAt", "")

        raw_content = "\n".join(
            part for part in [
                f"Video Title: {title}",
                f"Channel: {channel}",
                f"Published: {published_at}" if published_at else "",
                f"URL: {url}",
                "Transcript source: YouTube captions",
                "",
                "Transcript:",
                transcript_text,
            ]
            if part != ""
        )

        return ExtractionResult(
            title=title,
            url=url,
            source_type="YouTube",
            raw_content=raw_content,
            metadata={
                "extraction_method": "youtube_transcript_api",
                "thumbnail": thumbnail_url,
                "channel": channel,
            },
        )

    def _extract_via_ytdlp(
        self,
        url: str,
        video_id: str,
        thumbnail_url: str = "",
        snippet: dict | None = None,
    ) -> ExtractionResult:
        """Use yt-dlp subtitle download as a fallback transcript source."""
        from yt_dlp import YoutubeDL

        with tempfile.TemporaryDirectory(prefix="megamind-youtube-") as tmpdir:
            outtmpl = str(Path(tmpdir) / "%(id)s.%(ext)s")
            options = {
                "skip_download": True,
                "writesubtitles": True,
                "writeautomaticsub": True,
                "subtitleslangs": ["en.*", "en"],
                "subtitlesformat": "vtt",
                "outtmpl": outtmpl,
                "quiet": True,
                "no_warnings": True,
            }
            with YoutubeDL(options) as ydl:
                info = ydl.extract_info(url, download=True) or {}

            vtt_files = sorted(Path(tmpdir).glob(f"{video_id}*.vtt"))
            if not vtt_files:
                raise RuntimeError("No English subtitle file downloaded")

            preferred = next((path for path in vtt_files if ".en-orig." in path.name), vtt_files[0])
            transcript_text = _parse_vtt_transcript(preferred.read_text(encoding="utf-8"))
            if len(transcript_text) < 500:
                raise RuntimeError("yt-dlp transcript was too short to analyse reliably")

        snippet = snippet or {}
        title = snippet.get("title") or info.get("title") or _extract_title("", url)
        channel = snippet.get("channelTitle") or info.get("channel") or info.get("uploader") or "Unknown"
        published_at = snippet.get("publishedAt") or info.get("upload_date", "")

        raw_content = "\n".join(
            part for part in [
                f"Video Title: {title}",
                f"Channel: {channel}",
                f"Published: {published_at}" if published_at else "",
                f"URL: {url}",
                "Transcript source: yt-dlp subtitles",
                "",
                "Transcript:",
                transcript_text,
            ]
            if part != ""
        )

        return ExtractionResult(
            title=title,
            url=url,
            source_type="YouTube",
            raw_content=raw_content,
            metadata={
                "extraction_method": "yt_dlp_subtitles",
                "thumbnail": thumbnail_url,
                "channel": channel,
            },
        )

    def _extract_via_paste(self, url: str, thumbnail_url: str = "") -> ExtractionResult:
        """Prompt user to paste an actual transcript manually."""
        print(f"\n{'='*60}")
        print(f"  MANUAL EXTRACTION: YouTube Video")
        print(f"  URL: {url}")
        print(f"{'='*60}")
        print("\nNo verifiable captions were available automatically. Please:")
        print("  1. Open the video and show its transcript or captions.")
        print("  2. Copy the actual transcript for this video.")
        print("  3. Paste it below, then press Enter twice.")
        print("\nPaste the transcript:\n")

        lines = []
        empty_count = 0
        try:
            while True:
                line = input()
                if line == "":
                    empty_count += 1
                    if empty_count >= 2:
                        break
                    lines.append(line)
                else:
                    empty_count = 0
                    lines.append(line)
        except EOFError:
            pass

        content = "\n".join(lines).strip()
        if not content:
            print("No content provided. Exiting.", file=sys.stderr)
            sys.exit(1)

        # Ask for title
        title = input("\nVideo title (or press Enter to auto-detect): ").strip()
        if not title:
            first_line = content.split("\n")[0].strip().lstrip("#").strip()
            if ":" in first_line and len(first_line.split(":")[0].split()) <= 3:
                title = first_line.split(":", 1)[1].strip()
            else:
                title = first_line[:80] if first_line else "Untitled Video"

        return ExtractionResult(
            title=title,
            url=url,
            source_type="YouTube",
            raw_content=content,
            metadata={"extraction_method": "manual_paste", "thumbnail": thumbnail_url},
        )


def _extract_title(content: str, url: str) -> str:
    """Extract video title from supplied text or YouTube API.

    Tries in order:
    1. Explicit "Title:" or "Video Title:" lines in the response
    2. YouTube Data API (if API key available)
    3. First non-preamble line of the response
    """
    # 1. Look for explicit title patterns in the response
    for line in content.split("\n")[:15]:
        line = line.strip().lstrip("#").strip()
        m = re.match(
            r"^(?:\*{0,2})(?:Video\s+)?Title(?:\*{0,2})\s*[:]\s*(.+)",
            line, re.IGNORECASE,
        )
        if m:
            title = m.group(1).strip().strip('"').strip("*").strip()
            if title:
                return title[:200]

    # 2. Try YouTube Data API
    video_id = extract_video_id(url)
    if video_id and config.YOUTUBE_API_KEY:
        try:
            api_url = (
                f"https://www.googleapis.com/youtube/v3/videos"
                f"?id={video_id}&part=snippet&key={config.YOUTUBE_API_KEY}"
            )
            with urllib.request.urlopen(api_url, timeout=5) as resp:
                data = json.loads(resp.read())
                items = data.get("items", [])
                if items:
                    return items[0]["snippet"]["title"][:200]
        except Exception:
            pass

    # 3. First non-preamble line
    preamble_starts = (
        "below is", "here is", "here's", "i'll provide", "i will provide",
        "the following", "this is a", "let me", "certainly",
    )
    for line in content.split("\n")[:10]:
        line = line.strip().lstrip("#").strip()
        if not line:
            continue
        if any(line.lower().startswith(p) for p in preamble_starts):
            continue
        # Clean up label prefixes like "Channel: ..."
        if ":" in line and len(line.split(":")[0].split()) <= 3:
            line = line.split(":", 1)[1].strip()
        if line:
            return line[:200]

    return "Untitled Video"


def _fetch_youtube_snippet(url: str) -> dict:
    """Fetch basic YouTube metadata when the Data API key is configured."""
    video_id = extract_video_id(url)
    if not video_id or not config.YOUTUBE_API_KEY:
        return {}

    try:
        api_url = (
            "https://www.googleapis.com/youtube/v3/videos"
            f"?id={video_id}&part=snippet&key={config.YOUTUBE_API_KEY}"
        )
        with urllib.request.urlopen(api_url, timeout=5) as resp:
            data = json.loads(resp.read())
            items = data.get("items", [])
            if items:
                return items[0].get("snippet", {})
    except Exception:
        return {}

    return {}


def _format_transcript(rows: list[dict]) -> str:
    """Group caption rows into readable timestamped transcript paragraphs."""
    chunks = []
    current_lines = []
    current_start = None

    for row in rows:
        text = html.unescape(str(row.get("text", ""))).strip()
        text = re.sub(r"\s+", " ", text)
        if not text:
            continue

        start = float(row.get("start", 0) or 0)
        if current_start is None:
            current_start = start

        if current_lines and start - current_start >= 30:
            chunks.append(f"[{_format_timestamp(current_start)}] {' '.join(current_lines)}")
            current_lines = []
            current_start = start

        current_lines.append(text)

    if current_lines and current_start is not None:
        chunks.append(f"[{_format_timestamp(current_start)}] {' '.join(current_lines)}")

    return "\n".join(chunks)


def _format_timestamp(seconds: float) -> str:
    """Format seconds as mm:ss or h:mm:ss."""
    total = int(seconds)
    hours, remainder = divmod(total, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def _parse_vtt_transcript(vtt: str) -> str:
    """Extract readable timestamped text from a WebVTT subtitle file."""
    chunks = []
    current_time = None
    current_lines = []
    last_text = None

    def flush() -> None:
        nonlocal current_time, current_lines, last_text
        if current_time and current_lines:
            tagged_lines = [clean for raw, clean in current_lines if "<" in raw]
            cleaned_lines = tagged_lines or [clean for _, clean in current_lines]
            text = " ".join(cleaned_lines).strip()
            if text and text != last_text:
                chunks.append(f"[{current_time}] {text}")
                last_text = text
        current_time = None
        current_lines = []

    for raw_line in vtt.splitlines():
        line = raw_line.strip()
        if not line or line.startswith(("WEBVTT", "Kind:", "Language:", "NOTE")):
            flush()
            continue

        timestamp_match = re.match(r"^(\d{2}:)?(\d{2}:\d{2})\.\d{3}\s+-->", line)
        if timestamp_match:
            flush()
            current_time = timestamp_match.group(1) or ""
            current_time += timestamp_match.group(2)
            continue

        if line.isdigit():
            continue

        cleaned = re.sub(r"<[^>]+>", "", line)
        cleaned = html.unescape(cleaned)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        if not cleaned:
            continue
        current_lines.append((line, cleaned))

    flush()
    return "\n".join(chunks)
