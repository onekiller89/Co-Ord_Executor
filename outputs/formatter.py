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

*Extracted by [MegaMind](https://github.com/onekiller89/Co-Ord_Executor)*
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
    safe_title = re.sub(r"[^\w\s-]", "", result.title)
    safe_title = re.sub(r"\s+", "-", safe_title).strip("-").lower()
    safe_title = safe_title[:60]
    return f"{date_str}_{safe_title}.md"


def parse_sections(processed_content: str) -> dict[str, str]:
    """Parse AI-processed content into named sections.

    Returns a dict like {"Summary": "...", "Key Insights": "...", ...}
    """
    sections = {}
    current_section = None
    current_lines = []

    for line in processed_content.split("\n"):
        header_match = re.match(r"^###\s+(.+)$", line)
        if header_match and not line.startswith("####"):
            if current_section:
                sections[current_section] = "\n".join(current_lines).strip()
            current_section = header_match.group(1).strip()
            current_lines = []
        else:
            current_lines.append(line)

    if current_section:
        sections[current_section] = "\n".join(current_lines).strip()

    return sections


def parse_prompts(prompts_section: str) -> list[dict[str, str]]:
    """Parse the Implementation Prompts section into individual prompts.

    Returns a list of dicts: [{"title": "...", "body": "..."}, ...]
    """
    prompts = []
    current_title = None
    current_lines = []

    for line in prompts_section.split("\n"):
        prompt_match = re.match(r"^####\s+Prompt\s+\d+:\s*(.+)$", line)
        if prompt_match:
            if current_title:
                prompts.append({
                    "title": current_title,
                    "body": "\n".join(current_lines).strip(),
                })
            current_title = prompt_match.group(1).strip()
            current_lines = []
        elif current_title is not None:
            current_lines.append(line)

    if current_title:
        prompts.append({
            "title": current_title,
            "body": "\n".join(current_lines).strip(),
        })

    # Fallback: if no #### headers found, treat the whole section as one prompt
    if not prompts and prompts_section.strip():
        prompts.append({
            "title": "Implementation",
            "body": prompts_section.strip(),
        })

    return prompts
