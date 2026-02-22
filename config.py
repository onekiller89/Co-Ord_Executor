"""Configuration management for Co-Ord Executor."""

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

# User-Agent for web scraping
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)
