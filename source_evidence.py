"""Private, local evidence behind MegaMind notes and source review decisions."""

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import config

SNAPSHOT_DIR = config.PROJECT_ROOT / "data" / "source_snapshots"
REVIEWS_FILE = config.PROJECT_ROOT / "data" / "source_reviews.json"
REVIEW_STATES = {"unreviewed", "checked", "flagged"}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _snapshot_path(filename: str) -> Path:
    # A hash keeps index filenames out of paths and prevents traversal.
    return SNAPSHOT_DIR / (hashlib.sha256(filename.encode("utf-8")).hexdigest()[:24] + ".json")


def save_snapshot(filename: str, raw_content: str, url: str, method: str, *, recovered: bool = False) -> dict:
    """Preserve the first source text used for an extraction; never overwrite it."""
    path = _snapshot_path(filename)
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.parent.chmod(0o700)
    data = {"filename": filename, "url": url, "method": method,
            "captured_at": _now(), "recovered": recovered,
            "sha256": hashlib.sha256(raw_content.encode("utf-8")).hexdigest(),
            "text": raw_content}
    temp = path.with_suffix(".tmp")
    temp.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    temp.chmod(0o600)
    temp.replace(path)
    return data


def load_snapshot(filename: str) -> dict | None:
    path = _snapshot_path(filename)
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _load_reviews() -> dict:
    if not REVIEWS_FILE.exists():
        return {}
    try:
        data = json.loads(REVIEWS_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def get_review(filename: str) -> dict:
    return _load_reviews().get(filename, {"state": "unreviewed", "note": ""})


def set_review(filename: str, state: str, note: str = "") -> dict:
    if state not in REVIEW_STATES:
        raise ValueError("Invalid review state")
    parts = Path(filename).parts
    if (len(filename) > 220 or Path(filename).is_absolute() or ".." in parts
            or not re.fullmatch(r"[\w .()'!/-]+\.md", filename)):
        raise ValueError("Invalid extraction filename")
    reviews = _load_reviews()
    record = {"state": state, "note": note.strip()[:500], "updated_at": _now()}
    reviews[filename] = record
    REVIEWS_FILE.parent.mkdir(parents=True, exist_ok=True)
    REVIEWS_FILE.parent.chmod(0o700)
    temp = REVIEWS_FILE.with_suffix(".tmp")
    temp.write_text(json.dumps(reviews, ensure_ascii=False, indent=2), encoding="utf-8")
    temp.chmod(0o600)
    temp.replace(REVIEWS_FILE)
    return record
