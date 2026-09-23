"""Run one real source through the configured MegaMind model route."""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from extractors.base import ExtractionResult
from processors.ai_processor import REQUIRED_SECTIONS, _missing_required_sections, process_extraction


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source_file", type=Path)
    parser.add_argument("--url", required=True)
    args = parser.parse_args()
    result = ExtractionResult(title="Model route smoke source", url=args.url, source_type="YouTube",
                              raw_content=args.source_file.read_text(encoding="utf-8"), metadata={})
    output = process_extraction(result)
    missing = _missing_required_sections(output)
    if missing:
        raise RuntimeError(f"Missing sections: {', '.join(missing)}")
    print(f"Model: {result.metadata.get('analysis_model', 'unknown')}; words: {len(output.split())}; sections: {len(REQUIRED_SECTIONS)}")


if __name__ == "__main__":
    main()
