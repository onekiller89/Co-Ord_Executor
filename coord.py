#!/usr/bin/env python3
"""
Co-Ord Executor — Extract, structure, and track valuable content.

Usage:
    python coord.py <URL>                  Extract content from a URL
    python coord.py --paste <source_type>  Paste content manually
    python coord.py --list                 Show all extractions
    python coord.py --list --status TODO   Filter by status
    python coord.py --status <num> <status> Update entry status
"""

import argparse
import sys
from datetime import datetime, timezone

from extractors import get_extractor
from extractors.detector import SourceType
from extractors.base import ExtractionResult
from processors.ai_processor import process_extraction
from outputs.formatter import format_document, generate_filename
from outputs.index import add_to_index, update_status, list_entries
from outputs.storage import save_extraction


def extract_url(url: str) -> None:
    """Main extraction pipeline for a given URL."""
    print(f"\n  Co-Ord Executor")
    print(f"  {'='*40}")

    # 1. Detect source and get extractor
    extractor, source_type = get_extractor(url)
    print(f"  Source detected: {source_type.value}")
    print(f"  Extracting content...")

    # 2. Extract raw content
    result = extractor.extract(url)
    print(f"  Title: {result.title}")
    print(f"  Raw content: {len(result.raw_content)} chars")

    # 3. Process through AI
    print(f"  Processing with AI...")
    processed = process_extraction(result)
    print(f"  AI processing complete.")

    # 4. Format final document
    document = format_document(result, processed)
    filename = generate_filename(result)
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # 5. Save to storage
    print(f"  Saving extraction...")
    saved = save_extraction(filename, document)
    for location, path in saved.items():
        print(f"    -> {location}: {path}")

    # 6. Update index
    add_to_index(result, processed, filename, date_str)
    print(f"  Index updated.")

    print(f"\n  Done! Extraction saved as: {filename}")
    print(f"  {'='*40}\n")


def paste_content(source_type_str: str) -> None:
    """Handle manual paste mode for any source type."""
    type_map = {
        "youtube": SourceType.YOUTUBE,
        "twitter": SourceType.TWITTER,
        "x": SourceType.TWITTER,
        "github": SourceType.GITHUB,
        "article": SourceType.ARTICLE,
    }

    source_type = type_map.get(source_type_str.lower())
    if not source_type:
        print(f"Unknown source type: {source_type_str}")
        print(f"Valid types: {', '.join(type_map.keys())}")
        sys.exit(1)

    print(f"\n  Co-Ord Executor — Manual Paste Mode")
    print(f"  {'='*40}")
    print(f"  Source type: {source_type.value}")

    url = input("\n  URL (or press Enter if none): ").strip() or "N/A"
    title = input("  Title: ").strip() or "Untitled"

    print(f"\n  Paste content below (press Enter twice when done):\n")
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
        print("No content provided. Exiting.")
        sys.exit(1)

    result = ExtractionResult(
        title=title,
        url=url,
        source_type=source_type.value,
        raw_content=content,
        metadata={"extraction_method": "manual_paste"},
    )

    print(f"  Processing with AI...")
    processed = process_extraction(result)

    document = format_document(result, processed)
    filename = generate_filename(result)
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    saved = save_extraction(filename, document)
    for location, path in saved.items():
        print(f"    -> {location}: {path}")

    add_to_index(result, processed, filename, date_str)
    print(f"\n  Done! Extraction saved as: {filename}")
    print(f"  {'='*40}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Co-Ord Executor — Extract, structure, and track valuable content.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  python coord.py https://youtube.com/watch?v=abc123
  python coord.py https://x.com/user/status/123456
  python coord.py https://github.com/owner/repo
  python coord.py https://example.com/article
  python coord.py --paste youtube
  python coord.py --list
  python coord.py --list --status TODO
  python coord.py --status 3 "In Progress"
""",
    )

    parser.add_argument("url", nargs="?", help="URL to extract content from")
    parser.add_argument("--paste", metavar="TYPE", help="Manual paste mode (youtube, twitter, github, article)")
    parser.add_argument("--list", action="store_true", help="List all extractions from the index")
    parser.add_argument("--status", nargs=2, metavar=("NUM", "STATUS"),
                        help='Update status of entry NUM (e.g., --status 3 "In Progress")')
    parser.add_argument("--filter", metavar="STATUS", help="Filter --list by status (Backlog, TODO, In Progress, Done)")

    args = parser.parse_args()

    if args.list:
        print(list_entries(args.filter))
        return

    if args.status:
        entry_num = int(args.status[0])
        new_status = args.status[1]
        if update_status(entry_num, new_status):
            print(f"  Entry #{entry_num} updated to: {new_status}")
        else:
            print(f"  Entry #{entry_num} not found.")
        return

    if args.paste:
        paste_content(args.paste)
        return

    if args.url:
        extract_url(args.url)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
