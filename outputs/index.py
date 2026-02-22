"""Centralised index manager — maintains INDEX.md with all extractions."""

import re
from pathlib import Path

import config
from extractors.base import ExtractionResult
from outputs.formatter import extract_tags_from_content, extract_category_from_content


INDEX_HEADER = """\
# Co-Ord Extraction Index

> Centralised tracker for all extracted resources. Managed by Co-Ord Executor.

| # | Title | Source | Category | Tags | Status | Date | File |
|---|-------|--------|----------|------|--------|------|------|
"""


def _read_index() -> str:
    """Read the current index file, or return the header if it doesn't exist."""
    if config.INDEX_FILE.exists():
        return config.INDEX_FILE.read_text(encoding="utf-8")
    return INDEX_HEADER


def _count_entries(index_content: str) -> int:
    """Count existing entries in the index table."""
    lines = index_content.strip().split("\n")
    count = 0
    for line in lines:
        if line.startswith("|") and not line.startswith("| #") and not line.startswith("|---"):
            count += 1
    return count


def add_to_index(
    result: ExtractionResult,
    processed_content: str,
    filename: str,
    date_str: str,
    status: str = "Backlog",
) -> None:
    """Add a new entry to the centralised index."""
    config.EXTRACTIONS_PATH.mkdir(parents=True, exist_ok=True)

    index_content = _read_index()
    entry_num = _count_entries(index_content) + 1

    tags = extract_tags_from_content(processed_content)
    category = extract_category_from_content(processed_content)

    tags_str = " ".join(f"`#{t}`" for t in tags[:4])
    # Truncate title for table readability
    title_display = result.title[:50] + "..." if len(result.title) > 50 else result.title
    file_link = f"[view](./{filename})"

    new_row = (
        f"| {entry_num} | {title_display} | {result.source_type} "
        f"| {category} | {tags_str} | {status} | {date_str} | {file_link} |\n"
    )

    # Append the new row
    if index_content.rstrip().endswith("|"):
        index_content = index_content.rstrip() + "\n" + new_row
    else:
        index_content = index_content + new_row

    config.INDEX_FILE.write_text(index_content, encoding="utf-8")


def update_status(entry_num: int, new_status: str) -> bool:
    """Update the status of an entry in the index.

    Returns True if the entry was found and updated.
    """
    if not config.INDEX_FILE.exists():
        return False

    content = config.INDEX_FILE.read_text(encoding="utf-8")
    lines = content.split("\n")
    updated = False

    for i, line in enumerate(lines):
        if line.startswith("|") and not line.startswith("| #") and not line.startswith("|---"):
            cells = [c.strip() for c in line.split("|")]
            # cells[0] is empty (before first |), cells[1] is the number
            if cells[1] == str(entry_num):
                # Status is in the 6th column (index 5)
                cells[5] = f" {new_status} "
                lines[i] = "|".join(cells)
                updated = True
                break

    if updated:
        config.INDEX_FILE.write_text("\n".join(lines), encoding="utf-8")

    return updated


def list_entries(status_filter: str | None = None) -> str:
    """Return a formatted view of index entries, optionally filtered by status."""
    if not config.INDEX_FILE.exists():
        return "No index file found. Run an extraction first."

    content = _read_index()
    if status_filter is None:
        return content

    lines = content.split("\n")
    filtered = []
    for line in lines:
        if line.startswith("| #") or line.startswith("|---"):
            filtered.append(line)
        elif line.startswith("|"):
            if status_filter.lower() in line.lower():
                filtered.append(line)
        else:
            filtered.append(line)

    return "\n".join(filtered)
