#!/usr/bin/env python3
"""Local MegaMind library, Forum overview and source review dashboard."""

import argparse
import json
import os
import re
from collections import Counter
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import config
from forum_index import forum_stats, load_forum_index
from outputs.formatter import parse_sections
from outputs.index import _read_index, update_status
from source_evidence import get_review, load_snapshot, save_snapshot, set_review

DASHBOARD_PORT = int(os.getenv("DASHBOARD_PORT", "8050"))
UI_FILE = Path(__file__).with_name("dashboard_ui.html")
ALLOWED_STATUSES = ("Backlog", "TODO", "In Progress", "Done", "Cancel")


def _plain(value: str) -> str:
    value = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", value)
    return value.replace("**", "").replace("*", "").replace("`", "").strip()


def _bullets(value: str, *, checkboxes: bool = False) -> list[str]:
    pattern = r"^\s*-\s+\[[ xX]\]\s+(.+)" if checkboxes else r"^\s*[-*]\s+(.+)"
    return [_plain(match.group(1)) for line in value.splitlines()
            if (match := re.match(pattern, line))]


def _safe_file(filename: str) -> Path | None:
    if not filename:
        return None
    root = config.EXTRACTIONS_PATH.resolve()
    path = (root / filename).resolve()
    return path if path.is_relative_to(root) and path.suffix == ".md" and path.is_file() else None


def _source_state(source: str, category: str, filename: str, method: str) -> str:
    if category.casefold() == "unverified" or filename.startswith("quarantine/"):
        return "quarantined"
    if source.casefold() == "youtube" and method in {"youtube_transcript_api", "yt_dlp_subtitles"}:
        return "caption_backed"
    if method == "manual_paste":
        return "manual_input"
    if method == "grok_api":
        return "model_only"
    if source.casefold() in {"article", "github"}:
        return "fetched_text"
    return "unknown"


def _parse_index_entries() -> list[dict]:
    """Join catalogue rows to saved notes and local review evidence."""
    forum = load_forum_index()
    by_filename = {p.get("filename"): p for p in forum.get("posts", []) if p.get("filename")}
    by_title = {p.get("title", "").casefold(): p for p in forum.get("posts", [])}
    entries = []
    for line in _read_index().splitlines():
        if not re.match(r"^\|\s*\d+\s*\|", line):
            continue
        cells = [cell.strip() for cell in line.split("|")]
        if len(cells) < 10:
            continue
        number = int(cells[1])
        file_match = re.search(r"\]\(\./(.+?)\)", cells[8])
        filename = file_match.group(1) if file_match else ""
        path = _safe_file(filename)
        document = path.read_text(encoding="utf-8") if path else ""
        full_title = re.search(r"^#\s+(.+)$", document, re.M)
        url = re.search(r"^>\s*\*\*URL:\*\*\s+(https?://\S+)", document, re.M)
        method = re.search(r"\*\*Method:\*\*\s*([^\n|]+)", document)
        analysis = re.search(r"\*\*Analysis:\*\*\s*([^\n|]+)", document)
        sections = parse_sections(document.split("\n---\n", 1)[-1]) if document else {}
        title = full_title.group(1).strip() if full_title else cells[2]
        method_name = method.group(1).strip() if method else "unknown"
        state = _source_state(cells[3], cells[4], filename, method_name)
        review = get_review(filename)
        forum_post = by_filename.get(filename) or by_title.get(title[:100].casefold())
        entries.append({
            "num": number, "title": title, "source": cells[3], "category": cells[4],
            "tags": re.findall(r"`#([^`]+)`", cells[5]), "status": cells[6],
            "date": cells[7], "filename": filename, "source_url": url.group(1) if url else "",
            "source_method": method_name, "source_state": state, "review": review,
            "analysis_model": analysis.group(1).strip() if analysis else "not recorded",
            "has_snapshot": bool(load_snapshot(filename)),
            "summary": _plain(sections.get("Summary", "")),
            "insights": _bullets(sections.get("Key Insights", "")),
            "actions": _bullets(sections.get("Actions", ""), checkboxes=True),
            "prompt": _plain(sections.get("Implementation Prompts", ""))[:900],
            "forum_url": forum_post.get("url", "") if forum_post else "",
            "available": bool(path),
        })
    return sorted(entries, key=lambda entry: (entry["date"], entry["num"]), reverse=True)


def _load_budget() -> dict:
    path = config.PROJECT_ROOT / "api_budget.json"
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            calls = data.get("extraction_count", 0)
            return {"total_cost": data.get("total_cost", 0) if calls else None,
                    "call_count": calls, "subscription_runs": data.get("subscription_runs", 0),
                    "note": "Tracked API estimate; subscription usage has no per-call dollar figure."}
        except (OSError, json.JSONDecodeError):
            pass
    return {"total_cost": None, "call_count": 0, "subscription_runs": 0,
            "note": "No reliable API cost record is available."}


def _overview() -> dict:
    entries = _parse_index_entries()
    forum_data = load_forum_index()
    today = datetime.now(timezone.utc).date()
    recent = 0
    for entry in entries:
        try:
            recent += (today - datetime.fromisoformat(entry["date"]).date()).days <= 30
        except ValueError:
            pass
    high_review = sum(entry["source_state"] in {"quarantined", "model_only", "unknown"}
                      or entry["review"]["state"] == "flagged" for entry in entries)
    return {"entries": entries, "forum": forum_data, "forum_stats": forum_stats(forum_data),
            "budget": _load_budget(), "counts": {
                "total": len(entries), "action_queue": sum(e["status"] in {"TODO", "In Progress"} for e in entries),
                "ideas_to_try": sum(bool(e["actions"]) and e["source_state"] in {"caption_backed", "fetched_text"}
                                    and e["status"] not in {"Done", "Cancel"} for e in entries),
                "source_review": high_review, "recent_30d": recent,
                "by_status": dict(Counter(e["status"] for e in entries)),
                "by_source": dict(Counter(e["source"] for e in entries)),
                "by_category": dict(Counter(e["category"] for e in entries)),
                "by_tag": dict(Counter(t for e in entries for t in e["tags"])),
            }}


def _entry(number: int) -> dict | None:
    return next((e for e in _parse_index_entries() if e["num"] == number), None)


def _source_text(entry: dict) -> dict:
    snapshot = load_snapshot(entry["filename"])
    if snapshot:
        return snapshot
    if entry["source"].casefold() != "youtube" or not entry["source_url"]:
        raise FileNotFoundError("No local source text was preserved for this item.")
    from extractors.detector import extract_video_id
    from extractors.youtube import YouTubeExtractor
    video_id = extract_video_id(entry["source_url"])
    if not video_id:
        raise FileNotFoundError("The saved YouTube URL has no valid video ID.")
    canonical = f"https://www.youtube.com/watch?v={video_id}"
    extractor = YouTubeExtractor()
    try:
        result = extractor._extract_via_transcript_api(canonical, video_id)
    except Exception:
        result = extractor._extract_via_ytdlp(canonical, video_id)
    method = result.metadata.get("extraction_method", "")
    if method not in {"youtube_transcript_api", "yt_dlp_subtitles"}:
        raise FileNotFoundError("Verified captions could not be recovered.")
    transcript = result.raw_content
    if len(transcript) < 500:
        raise FileNotFoundError("Captions were too short to review.")
    return save_snapshot(entry["filename"], transcript, entry["source_url"],
                         method, recovered=True)


class DashboardHandler(BaseHTTPRequestHandler):
    """Only serve known routes; browser writes require same-origin JSON requests."""

    def _host_allowed(self) -> bool:
        host = self.headers.get("Host", "").split(":", 1)[0].lower()
        extra_clients = {ip.strip() for ip in os.getenv("DASHBOARD_ALLOWED_CLIENTS", "").split(",") if ip.strip()}
        return host in self._allowed_hosts() and self.client_address[0] in {"127.0.0.1", "::1"} | extra_clients

    @staticmethod
    def _allowed_hosts() -> set[str]:
        extra = os.getenv("DASHBOARD_ALLOWED_HOSTS", "")
        return {"localhost", "127.0.0.1"} | {h.strip().lower() for h in extra.split(",") if h.strip()}

    def _send(self, code: int, body: bytes, mime: str):
        self.send_response(code)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Connection", "close")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' https://img.youtube.com; connect-src 'self'; base-uri 'none'; frame-ancestors 'none'")
        self.end_headers()
        # WSL mirrored-network loopback can retain the final TCP segment until
        # a later write. Keep extra bytes outside Content-Length as a flush.
        self.wfile.write(body + b" " * 2048)
        self.wfile.flush()

    def _json(self, data: dict | list, code: int = 200):
        self._send(code, json.dumps(data, ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8")

    def do_GET(self):
        if not self._host_allowed():
            self.send_error(403)
            return
        route = urlparse(self.path)
        query = parse_qs(route.query)
        if route.path in {"/", "/dashboard"}:
            self._send(200, UI_FILE.read_bytes(), "text/html; charset=utf-8")
        elif route.path == "/api/overview":
            self._json(_overview())
        elif route.path == "/api/health":
            self._json({"ok": True})
        elif route.path in {"/api/source", "/api/note"}:
            try:
                number = int(query.get("num", [""])[0])
            except ValueError:
                self._json({"error": "Invalid item number"}, 400)
                return
            entry = _entry(number)
            if not entry:
                self._json({"error": "Item not found"}, 404)
                return
            if route.path == "/api/note":
                path = _safe_file(entry["filename"])
                if not path:
                    self._json({"error": "Note unavailable"}, 404)
                    return
                self._send(200, path.read_bytes(), "text/markdown; charset=utf-8")
            else:
                try:
                    self._json(_source_text(entry))
                except Exception as exc:
                    self._json({"error": f"Source text unavailable: {type(exc).__name__}"}, 404)
        else:
            self.send_error(404)

    def do_POST(self):
        if not self._host_allowed() or self.headers.get("X-MegaMind-Local") != "1":
            self.send_error(403)
            return
        origin = self.headers.get("Origin")
        if origin:
            parsed = urlparse(origin)
            if parsed.hostname not in self._allowed_hosts() or parsed.port != self.server.server_port:
                self.send_error(403)
                return
        if self.headers.get("Content-Type", "").split(";", 1)[0] != "application/json":
            self._json({"error": "JSON required"}, 415)
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if not 0 < size <= 4096:
                raise ValueError("Invalid request size")
            data = json.loads(self.rfile.read(size))
            number = int(data.get("num"))
            entry = _entry(number)
            if not entry:
                self._json({"error": "Item not found"}, 404)
                return
            if urlparse(self.path).path == "/api/status":
                status = data.get("status", "")
                if status not in ALLOWED_STATUSES:
                    raise ValueError("Invalid status")
                self._json({"ok": update_status(number, status)})
            elif urlparse(self.path).path == "/api/review":
                review = set_review(entry["filename"], data.get("state", ""), data.get("note", ""))
                self._json({"ok": True, "review": review})
            else:
                self.send_error(404)
        except (ValueError, TypeError, json.JSONDecodeError) as exc:
            self._json({"error": str(exc)[:160]}, 400)

    def log_message(self, format, *args):
        pass


def main():
    parser = argparse.ArgumentParser(description="MegaMind local dashboard")
    parser.add_argument("--port", type=int, default=DASHBOARD_PORT)
    parser.add_argument("--host", default=os.getenv("DASHBOARD_HOST", "0.0.0.0"))
    args = parser.parse_args()
    server = ThreadingHTTPServer((args.host, args.port), DashboardHandler)
    print(f"MegaMind Dashboard running at http://localhost:{args.port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
