"""Detect source type from a URL or reference string."""

import re
from enum import Enum
from urllib.parse import urlparse


class SourceType(Enum):
    YOUTUBE = "YouTube"
    TWITTER = "Twitter/X"
    GITHUB = "GitHub"
    ARTICLE = "Article"


def detect_source(url: str) -> SourceType:
    """Identify the source type from a URL."""
    parsed = urlparse(url)
    host = parsed.netloc.lower().replace("www.", "")

    # YouTube
    if host in ("youtube.com", "youtu.be", "m.youtube.com"):
        return SourceType.YOUTUBE

    # Twitter / X
    if host in ("twitter.com", "x.com", "mobile.twitter.com", "mobile.x.com"):
        return SourceType.TWITTER

    # GitHub
    if host in ("github.com", "raw.githubusercontent.com"):
        return SourceType.GITHUB

    # Default to article for any other URL
    return SourceType.ARTICLE


def extract_video_id(url: str) -> str | None:
    """Extract YouTube video ID from URL."""
    patterns = [
        r"(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/|youtube\.com/shorts/)([a-zA-Z0-9_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def extract_tweet_id(url: str) -> str | None:
    """Extract tweet/post ID from Twitter/X URL."""
    match = re.search(r"(?:twitter\.com|x\.com)/\w+/status/(\d+)", url)
    return match.group(1) if match else None


def extract_github_parts(url: str) -> dict | None:
    """Extract owner/repo from GitHub URL."""
    match = re.search(r"github\.com/([^/]+)/([^/]+?)(?:\.git|/|$)", url)
    if match:
        return {"owner": match.group(1), "repo": match.group(2)}
    return None
