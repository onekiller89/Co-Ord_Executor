"""Markdown document formatter — wraps AI-processed content into a final document."""

import re
from datetime import datetime, timezone

from extractors.base import ExtractionResult


def format_document(result: ExtractionResult, processed_content: str) -> str:
    """Wrap the AI-processed content into a complete markdown document.

    Returns the final markdown string ready to be saved.
    """
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    extraction_method = result.metadata.get("extraction_method", "scrape")

    document = f"""\
# {result.title}

> **Source:** {result.source_type} | **Extracted:** {now} | **Method:** {extraction_method}
> **URL:** {result.url}

---

{processed_content}

---

*Extracted by [Co-Ord Executor](https://github.com/onekiller89/Co-Ord_Executor)*
"""
    return document


def extract_tags_from_content(processed_content: str) -> list[str]:
    """Pull tag strings from the processed content's Tags section."""
    tags = re.findall(r"`#([^`]+)`", processed_content)
    return tags


def extract_category_from_content(processed_content: str) -> str:
    """Pull category from the processed content's Category section."""
    match = re.search(r"###\s*Category\s*\n+(.+)", processed_content)
    if match:
        return match.group(1).strip().strip("`").strip()
    return "Other"


def generate_filename(result: ExtractionResult) -> str:
    """Generate a filesystem-safe filename from the extraction result."""
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    # Clean title for filename
    safe_title = re.sub(r"[^\w\s-]", "", result.title)
    safe_title = re.sub(r"\s+", "-", safe_title).strip("-").lower()
    safe_title = safe_title[:60]  # Keep it reasonable length
    return f"{date_str}_{safe_title}.md"
