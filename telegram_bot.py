#!/usr/bin/env python3
"""
Co-Ord Executor — Telegram Bot

Listens for URLs sent via Telegram and creates GitHub Issues
with the 'extract' label. GitHub Actions then processes them.

Setup:
  1. Message @BotFather on Telegram → /newbot → get your bot token
  2. Add TELEGRAM_BOT_TOKEN and GITHUB_TOKEN to your .env
  3. Run: python telegram_bot.py
  4. Send any URL to your bot on Telegram

Requires: pip install python-telegram-bot
"""

import os
import re
import logging
import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_REPO = os.getenv("GITHUB_REPO", "onekiller89/Co-Ord_Executor")
ALLOWED_USERS = os.getenv("TELEGRAM_ALLOWED_USERS", "")  # Comma-separated Telegram usernames

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

URL_PATTERN = re.compile(r"https?://[^\s<>\"')}\]]+")


def check_user_allowed(username: str) -> bool:
    """Check if the Telegram user is allowed to use the bot."""
    if not ALLOWED_USERS:
        return True  # No restriction if not configured
    allowed = [u.strip().lower().lstrip("@") for u in ALLOWED_USERS.split(",")]
    return username.lower() in allowed


def create_github_issue(url: str, notes: str = "") -> dict | None:
    """Create a GitHub Issue with the extract label."""
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }

    body = f"URL submitted via Telegram bot.\n\n{notes}" if notes else "URL submitted via Telegram bot."

    payload = {
        "title": url,
        "body": body,
        "labels": ["extract"],
    }

    resp = requests.post(
        f"https://api.github.com/repos/{GITHUB_REPO}/issues",
        headers=headers,
        json=payload,
        timeout=15,
    )

    if resp.status_code == 201:
        return resp.json()
    else:
        logger.error(f"GitHub API error {resp.status_code}: {resp.text}")
        return None


async def handle_message(update, context) -> None:
    """Handle incoming Telegram messages."""
    message = update.message
    if not message or not message.text:
        return

    # Auth check
    username = message.from_user.username or ""
    if not check_user_allowed(username):
        await message.reply_text("Not authorised. Add your username to TELEGRAM_ALLOWED_USERS in .env")
        return

    text = message.text.strip()

    # Check for URLs in the message
    urls = URL_PATTERN.findall(text)

    if not urls:
        await message.reply_text(
            "No URL detected. Send me a URL and I'll queue it for extraction.\n\n"
            "Supported: YouTube, X/Twitter, GitHub, articles"
        )
        return

    # Extract notes (anything that isn't a URL)
    notes = URL_PATTERN.sub("", text).strip()

    for url in urls:
        issue = create_github_issue(url, notes)
        if issue:
            issue_url = issue.get("html_url", "")
            await message.reply_text(
                f"Queued for extraction!\n"
                f"URL: {url}\n"
                f"Issue: {issue_url}\n\n"
                f"GitHub Actions will process this shortly."
            )
        else:
            await message.reply_text(f"Failed to create issue for: {url}\nCheck bot logs.")


async def handle_start(update, context) -> None:
    """Handle /start command."""
    await update.message.reply_text(
        "Co-Ord Executor Bot\n\n"
        "Send me any URL and I'll queue it for extraction:\n"
        "- YouTube videos\n"
        "- X/Twitter threads\n"
        "- GitHub repos\n"
        "- Articles & blog posts\n\n"
        "The extraction will appear in your repo and Obsidian vault."
    )


def main():
    if not TELEGRAM_BOT_TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN not set in .env")
        print("1. Message @BotFather on Telegram")
        print("2. Create a bot with /newbot")
        print("3. Add the token to your .env file")
        return

    if not GITHUB_TOKEN:
        print("Error: GITHUB_TOKEN not set in .env")
        print("Create a GitHub PAT with 'repo' scope and add it to .env")
        return

    # Import here so missing dependency gives a clear error
    try:
        from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters
    except ImportError:
        print("Missing dependency: pip install python-telegram-bot")
        return

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", handle_start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot started. Send a URL to begin.")
    app.run_polling()


if __name__ == "__main__":
    main()
