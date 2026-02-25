"""YouTube playlist watcher — monitors an unlisted playlist for new videos."""

import logging
from googleapiclient.discovery import build

import config

logger = logging.getLogger("megamind.youtube")


def get_youtube_service():
    """Build a YouTube Data API v3 service using API key."""
    if not config.YOUTUBE_API_KEY:
        raise RuntimeError("YOUTUBE_API_KEY not set. Cannot access YouTube Data API.")
    return build("youtube", "v3", developerKey=config.YOUTUBE_API_KEY)


def get_playlist_videos(playlist_id: str) -> list[dict]:
    """Fetch all videos from a YouTube playlist.

    Returns a list of dicts: [{"video_id": "...", "title": "...", "playlist_item_id": "..."}, ...]
    """
    youtube = get_youtube_service()
    videos = []
    next_page_token = None

    while True:
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token,
        )
        response = request.execute()

        for item in response.get("items", []):
            snippet = item["snippet"]
            video_id = snippet["resourceId"]["videoId"]
            videos.append({
                "video_id": video_id,
                "title": snippet.get("title", "Untitled"),
                "playlist_item_id": item["id"],
                "url": f"https://www.youtube.com/watch?v={video_id}",
            })

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return videos


def is_video_processed(video_id: str) -> bool:
    """Check if a video has already been processed by looking in INDEX.md."""
    if not config.INDEX_FILE.exists():
        return False
    index_content = config.INDEX_FILE.read_text(encoding="utf-8")
    return video_id in index_content


def get_new_videos() -> list[dict]:
    """Compare playlist against INDEX.md and return unprocessed videos."""
    if not config.YOUTUBE_EXTRACT_PLAYLIST_ID:
        logger.warning("YOUTUBE_EXTRACT_PLAYLIST_ID not set. Skipping playlist check.")
        return []

    try:
        all_videos = get_playlist_videos(config.YOUTUBE_EXTRACT_PLAYLIST_ID)
    except Exception as e:
        logger.error(f"Failed to fetch playlist: {e}")
        return []

    new_videos = [v for v in all_videos if not is_video_processed(v["video_id"])]
    logger.info(f"Playlist check: {len(all_videos)} total, {len(new_videos)} new")
    return new_videos


def move_to_completed(playlist_item_id: str) -> bool:
    """Remove a video from the extract playlist.

    This requires OAuth2 credentials (API key alone cannot modify playlists).
    Returns True if successful, False if not possible.
    """
    # OAuth2 is needed to modify playlists. With just an API key, we can only read.
    # For now, log a warning. The video is tracked in INDEX.md so it won't be
    # re-processed. User can manually move it or we add OAuth2 support later.
    logger.info(
        f"Video processed (item {playlist_item_id}). "
        f"Manual move to 'extract-completed' playlist needed "
        f"(OAuth2 support for auto-move coming in a future update)."
    )
    return False
