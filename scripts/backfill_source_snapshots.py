"""Save verified evaluation captions as private, recovered source snapshots.

The corpus and snapshots stay outside Git. Run from the repository root with
MEGAMIND_EVAL_DIR pointing to the local ten-source comparison folder.
"""

import hashlib
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from source_evidence import save_snapshot


def main():
    folder = Path(os.environ["MEGAMIND_EVAL_DIR"])
    rows = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
    count = 0
    for row in rows:
        if row["status"] != "ready":
            continue
        raw = (folder / row["source_file"]).read_text(encoding="utf-8")
        if hashlib.sha256(raw.encode()).hexdigest() != row["source_sha256"]:
            raise ValueError(f"Source hash mismatch for #{row['index_number']}")
        filename = str(Path(row["historical_file"]).relative_to("extractions"))
        saved = save_snapshot(filename, raw, row["url"], row["extraction_method"], recovered=True)
        if saved["sha256"] != row["source_sha256"] or saved["url"] != row["url"]:
            raise ValueError(f"Existing snapshot differs for #{row['index_number']}")
        count += 1
    print(f"Verified private source snapshots: {count}")


if __name__ == "__main__":
    main()
