"""Configuration management for Co-Ord Executor / MegaMind."""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Project root
PROJECT_ROOT = Path(__file__).parent.resolve()

# API Keys
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
XAI_API_KEY = os.getenv("XAI_API_KEY", "")

# Models
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-20250514")
GROK_MODEL = os.getenv("GROK_MODEL", "grok-3-latest")

# Storage paths
EXTRACTIONS_PATH = Path(os.getenv("EXTRACTIONS_PATH", PROJECT_ROOT / "extractions")).resolve()
OBSIDIAN_VAULT_PATH = os.getenv("OBSIDIAN_VAULT_PATH", "")
INDEX_FILE = EXTRACTIONS_PATH / "INDEX.md"

# Grok API (xAI uses OpenAI-compatible endpoint)
GROK_API_BASE = "https://api.x.ai/v1"

# CI mode — detected automatically in GitHub Actions, or set CI=true
CI_MODE = os.getenv("CI", "").lower() in ("true", "1") or os.getenv("GITHUB_ACTIONS", "") == "true"

# User-Agent for web scraping
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)

# === Discord (MegaMind Bot) ===
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "")
DISCORD_SERVER_ID = int(os.getenv("DISCORD_SERVER_ID", "0"))
DISCORD_EXTRACT_CHANNEL_ID = int(os.getenv("DISCORD_EXTRACT_CHANNEL_ID", "0"))
DISCORD_OUTPUT_CHANNEL_ID = int(os.getenv("DISCORD_OUTPUT_CHANNEL_ID", "0"))

# === YouTube Playlist Watcher ===
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
YOUTUBE_EXTRACT_PLAYLIST_ID = os.getenv("YOUTUBE_EXTRACT_PLAYLIST_ID", "")
YOUTUBE_COMPLETED_PLAYLIST_ID = os.getenv("YOUTUBE_COMPLETED_PLAYLIST_ID", "")
YOUTUBE_POLL_INTERVAL_MINUTES = int(os.getenv("YOUTUBE_POLL_INTERVAL_MINUTES", "60"))

# === GitHub (for issue creation on robot react) ===
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_REPO = os.getenv("GITHUB_REPO", "onekiller89/Co-Ord_Executor")
