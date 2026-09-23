"""Check that every MegaMind extraction index link resolves inside the repo."""

from collections import defaultdict
from pathlib import Path
import re
import sys


root = Path(__file__).resolve().parents[1] / "extractions"
index = root / "INDEX.md"
references = defaultdict(list)
missing = []

for number, line in enumerate(index.read_text(encoding="utf-8").splitlines(), start=1):
    if not line.startswith("|") or line.startswith(("| #", "|---")):
        continue
    match = re.search(r"\[[^]]+\]\(\./([^)]*)\)", line)
    if not match:
        missing.append(f"line {number}: no file link")
        continue
    target = (root / match.group(1)).resolve()
    if not target.is_relative_to(root.resolve()) or not target.is_file():
        missing.append(f"line {number}: {match.group(1)}")
    references[str(target)].append(number)

duplicates = {path: lines for path, lines in references.items() if len(lines) > 1}
print(f"Index rows: {sum(len(lines) for lines in references.values())}")
print(f"Missing or invalid links: {len(missing)}")
print(f"Repeated file links: {len(duplicates)}")
for item in missing:
    print(item)
for path, lines in duplicates.items():
    print(f"Repeated: {Path(path).name} on lines {','.join(map(str, lines))}")
sys.exit(1 if missing else 0)
