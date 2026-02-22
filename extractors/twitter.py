"""Twitter/X thread extraction via Grok API or manual paste."""

import sys
from openai import OpenAI

import config
from extractors.base import BaseExtractor, ExtractionResult
from extractors.detector import extract_tweet_id


GROK_SYSTEM_PROMPT = """You are extracting content from a Twitter/X thread or post. Given the URL, provide a comprehensive extraction including:

1. The author's name and handle
2. The full text of every tweet/post in the thread (in order)
3. All key points, insights, and takeaways
4. Any links, tools, resources, or references mentioned
5. Any images or media described (describe what they show)
6. Any code snippets shared
7. The overall topic and context of the thread

Be thorough - capture the complete thread content. Format as structured text, not markdown."""


class TwitterExtractor(BaseExtractor):
    """Extract Twitter/X thread content via Grok or manual paste."""

    def extract(self, url: str) -> ExtractionResult:
        tweet_id = extract_tweet_id(url)

        # Try Grok API first
        if config.XAI_API_KEY:
            return self._extract_via_grok(url)

        # In CI mode, can't prompt for input
        if config.CI_MODE:
            raise RuntimeError(
                "Cannot extract Twitter/X without XAI_API_KEY in CI mode. "
                "Add XAI_API_KEY to your GitHub Secrets."
            )

        # Fall back to manual paste
        return self._extract_via_paste(url)

    def _extract_via_grok(self, url: str) -> ExtractionResult:
        """Use Grok API to extract thread content."""
        client = OpenAI(
            api_key=config.XAI_API_KEY,
            base_url=config.GROK_API_BASE,
        )

        response = client.chat.completions.create(
            model=config.GROK_MODEL,
            messages=[
                {"role": "system", "content": GROK_SYSTEM_PROMPT},
                {"role": "user", "content": f"Extract the full content from this Twitter/X thread: {url}"},
            ],
        )

        content = response.choices[0].message.content
        lines = content.strip().split("\n")
        title = lines[0].strip().lstrip("#").strip() if lines else "Untitled Thread"
        if ":" in title and len(title.split(":")[0].split()) <= 3:
            title = title.split(":", 1)[1].strip()

        return ExtractionResult(
            title=title,
            url=url,
            source_type="Twitter/X",
            raw_content=content,
            metadata={"extraction_method": "grok_api"},
        )

    def _extract_via_paste(self, url: str) -> ExtractionResult:
        """Prompt user to paste Grok output manually."""
        print(f"\n{'='*60}")
        print(f"  MANUAL EXTRACTION: Twitter/X Thread")
        print(f"  URL: {url}")
        print(f"{'='*60}")
        print(f"\nNo Grok API key configured. Please:")
        print(f"  1. Open Grok (grok.x.ai) or X with Grok")
        print(f"  2. Ask Grok to extract this thread:")
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

        title = input("\nThread title/topic (or press Enter to auto-detect): ").strip()
        if not title:
            first_line = content.split("\n")[0].strip().lstrip("#").strip()
            if ":" in first_line and len(first_line.split(":")[0].split()) <= 3:
                title = first_line.split(":", 1)[1].strip()
            else:
                title = first_line[:80] if first_line else "Untitled Thread"

        return ExtractionResult(
            title=title,
            url=url,
            source_type="Twitter/X",
            raw_content=content,
            metadata={"extraction_method": "manual_paste"},
        )
