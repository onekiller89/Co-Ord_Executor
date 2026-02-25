"""YouTube playlist watcher — polls a playlist for new videos to extract.

Uses YouTube Data API v3 to list playlist items and tracks which videos
have already been processed via a local state file + INDEX.md.
"""

import json
import logging
from pathlib import Path

import requests

import config

log = logging.getLogger("megamind.youtube")

# Local state file to track processed video IDs
STATE_FILE = config.PROJECT_ROOT / ".youtube_processed.json"


def _load_processed() -> set[str]:
    """Load the set of already-processed video IDs."""
    if STATE_FILE.exists():
        try:
            data = json.loads(STATE_FILE.read_text())
            return set(data.get("processed", []))
        except (json.JSONDecodeError, KeyError):
            return set()
    return set()


def _save_processed(video_ids: set[str]):
    """Save the set of processed video IDs."""
    STATE_FILE.write_text(json.dumps({"processed": sorted(video_ids)}, indent=2))


def mark_video_processed(video_id: str):
    """Mark a video as processed."""
    processed = _load_processed()
    processed.add(video_id)
    _save_processed(processed)


def get_playlist_videos() -> list[dict]:
    """Fetch all videos from the YouTube extract playlist.

    Returns list of dicts with video_id, title, playlist_item_id.
    """
    if not config.YOUTUBE_API_KEY or not config.YOUTUBE_EXTRACT_PLAYLIST_ID:
        return []

    videos = []
    page_token = None

    while True:
        params = {
            "part": "snippet",
            "playlistId": config.YOUTUBE_EXTRACT_PLAYLIST_ID,
            "maxResults": 50,
            "key": config.YOUTUBE_API_KEY,
        }
        if page_token:
            params["pageToken"] = page_token

        resp = requests.get(
            "https://www.googleapis.com/youtube/v3/playlistItems",
            params=params,
        )

        if resp.status_code != 200:
            log.error(f"YouTube API error: {resp.status_code} {resp.text}")
            break

        data = resp.json()

        for item in data.get("items", []):
            snippet = item["snippet"]
            video_id = snippet.get("resourceId", {}).get("videoId")
            if video_id:
                videos.append({
                    "video_id": video_id,
                    "title": snippet.get("title", "Unknown"),
                    "playlist_item_id": item["id"],
                    "published_at": snippet.get("publishedAt", ""),
                })

        page_token = data.get("nextPageToken")
        if not page_token:
            break

    return videos


def get_new_playlist_videos() -> list[dict]:
    """Return only videos that haven't been processed yet."""
    all_videos = get_playlist_videos()
    processed = _load_processed()

    # Also check INDEX.md for YouTube URLs already extracted
    index_video_ids = _get_indexed_youtube_ids()
    already_done = processed | index_video_ids

    new_videos = [v for v in all_videos if v["video_id"] not in already_done]

    if new_videos:
        log.info(f"Found {len(new_videos)} new video(s) in playlist")
    return new_videos


def _get_indexed_youtube_ids() -> set[str]:
    """Scan INDEX.md for already-extracted YouTube video IDs."""
    ids = set()
    if config.INDEX_FILE.exists():
        content = config.INDEX_FILE.read_text()
        import re
        # Match YouTube video IDs in index entries
        for match in re.finditer(r"youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})", content):
            ids.add(match.group(1))
        for match in re.finditer(r"youtu\.be/([a-zA-Z0-9_-]{11})", content):
            ids.add(match.group(1))
    return ids


def remove_from_playlist(playlist_item_id: str) -> bool:
    """Remove a video from the extract playlist (requires OAuth2).

    Note: This requires OAuth2 authentication, not just an API key.
    With an API key only, this will fail. For now we track state locally
    and log a warning. Full playlist management requires OAuth2 setup.
    """
    if not config.YOUTUBE_API_KEY:
        return False

    # API key auth cannot delete playlist items — needs OAuth2
    log.info(
        f"Video {playlist_item_id} processed. "
        f"Playlist removal requires OAuth2 — tracked in local state instead."
    )
    return False
