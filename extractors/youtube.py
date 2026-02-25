"""YouTube video extraction via Grok API or manual paste."""

import sys
from openai import OpenAI

import config
from extractors.base import BaseExtractor, ExtractionResult
from extractors.detector import extract_video_id


GROK_SYSTEM_PROMPT = """You are extracting content from a YouTube video. Given the video URL, provide a comprehensive extraction including:

1. The exact video title
2. The channel/creator name
3. A detailed summary of the video content
4. All key points, insights, and takeaways discussed
5. Any tools, frameworks, libraries, or resources mentioned (with links if stated)
6. Any step-by-step instructions or tutorials shown
7. Any code snippets or commands demonstrated
8. Timestamps for major sections if apparent

Be thorough - capture everything valuable. Format as structured text, not markdown."""


class YouTubeExtractor(BaseExtractor):
    """Extract YouTube video content via Grok or manual paste."""

    def extract(self, url: str) -> ExtractionResult:
        video_id = extract_video_id(url)
        canonical_url = f"https://www.youtube.com/watch?v={video_id}" if video_id else url
        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg" if video_id else ""

        # Try Grok API first
        if config.XAI_API_KEY:
            return self._extract_via_grok(canonical_url, thumbnail_url)

        # In CI mode, can't prompt for input
        if config.CI_MODE:
            raise RuntimeError(
                "Cannot extract YouTube without XAI_API_KEY in CI mode. "
                "Add XAI_API_KEY to your GitHub Secrets."
            )

        # Fall back to manual paste
        return self._extract_via_paste(canonical_url, thumbnail_url)

    def _extract_via_grok(self, url: str, thumbnail_url: str = "") -> ExtractionResult:
        """Use Grok API to extract video content."""
        client = OpenAI(
            api_key=config.XAI_API_KEY,
            base_url=config.GROK_API_BASE,
        )

        response = client.chat.completions.create(
            model=config.GROK_MODEL,
            messages=[
                {"role": "system", "content": GROK_SYSTEM_PROMPT},
                {"role": "user", "content": f"Extract all content from this YouTube video: {url}"},
            ],
        )

        content = response.choices[0].message.content
        # Try to parse title from first line of response
        lines = content.strip().split("\n")
        title = lines[0].strip().lstrip("#").strip() if lines else "Untitled Video"
        # Clean up title if it has a label prefix like "Title: ..."
        if ":" in title and len(title.split(":")[0].split()) <= 3:
            title = title.split(":", 1)[1].strip()

        return ExtractionResult(
            title=title,
            url=url,
            source_type="YouTube",
            raw_content=content,
            metadata={"extraction_method": "grok_api", "thumbnail": thumbnail_url},
        )

    def _extract_via_paste(self, url: str, thumbnail_url: str = "") -> ExtractionResult:
        """Prompt user to paste Grok output manually."""
        print(f"\n{'='*60}")
        print(f"  MANUAL EXTRACTION: YouTube Video")
        print(f"  URL: {url}")
        print(f"{'='*60}")
        print(f"\nNo Grok API key configured. Please:")
        print(f"  1. Open Grok (grok.x.ai) or X with Grok")
        print(f"  2. Ask Grok to summarise this video:")
        print(f"     \"{url}\"")
        print(f"  3. Paste the full response below.")
        print(f"\nPaste Grok's response (press Enter twice when done):\n")

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
