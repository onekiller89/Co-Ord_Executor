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

    thumbnail = result.metadata.get("thumbnail", "")
    banner_line = f"![banner]({thumbnail})\n\n" if thumbnail else ""

    document = f"""\
{banner_line}# {result.title}

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


def parse_sections(processed_content: str) -> dict[str, str]:
    """Split AI-processed content into named sections.

    Returns dict like {"Summary": "...", "Key Insights": "...", ...}
    """
    sections = {}
    current_key = None
    current_lines = []

    for line in processed_content.split("\n"):
        heading_match = re.match(r"^###\s+(.+)$", line)
        if heading_match:
            if current_key:
                sections[current_key] = "\n".join(current_lines).strip()
            current_key = heading_match.group(1).strip()
            current_lines = []
        elif current_key is not None:
            current_lines.append(line)

    if current_key:
        sections[current_key] = "\n".join(current_lines).strip()

    return sections


def parse_prompts(prompts_section: str) -> list[dict]:
    """Parse the Implementation Prompts section into individual prompts.

    Returns list of dicts: [{"title": "...", "body": "..."}, ...]
    """
    prompts = []
    current_title = None
    current_lines = []

    for line in prompts_section.split("\n"):
        prompt_heading = re.match(r"^####\s+Prompt\s+\d+:\s*(.+)$", line)
        if prompt_heading:
            if current_title:
                prompts.append({
                    "title": current_title,
                    "body": "\n".join(current_lines).strip().strip(">").strip(),
                })
            current_title = prompt_heading.group(1).strip()
            current_lines = []
        elif current_title is not None:
            current_lines.append(line)

    if current_title:
        prompts.append({
            "title": current_title,
            "body": "\n".join(current_lines).strip().strip(">").strip(),
        })

    # Fallback: if no #### Prompt N: headings found, split on blockquotes
    if not prompts and prompts_section.strip():
        blocks = re.split(r"\n(?=>)", prompts_section)
        for i, block in enumerate(blocks, 1):
            body = block.strip().strip(">").strip()
            if body:
                prompts.append({"title": f"Prompt {i}", "body": body})

    return prompts
