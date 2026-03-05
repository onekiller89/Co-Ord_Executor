#!/usr/bin/env python3
"""
MegaMind — Discord bot for Co-Ord Executor.

Watches #extract for URLs, processes them through the extraction pipeline,
and posts structured output to #output. Also integrates with the YouTube
playlist watcher for automated video extraction.

Usage:
    python discord_bot.py
"""

import asyncio
import logging
import os
import re
import subprocess
import sys

import discord
from discord import app_commands
from discord.ext import tasks

import config
from coord import run_pipeline
from outputs.formatter import parse_sections, parse_prompts, extract_category_from_content

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger("megamind")

# URL pattern to detect links in messages
URL_PATTERN = re.compile(r"https?://[^\s<>\"']+")

# Category colours for Discord embeds
CATEGORY_COLOURS = {
    "claude code": 0xD97706,      # amber
    "ai agents": 0x7C3AED,        # violet
    "openclaw": 0xDC2626,         # red
    "infrastructure as code": 0x0891B2,  # cyan
    "devops": 0x2563EB,           # blue
    "security": 0xB91C1C,         # dark red
    "development": 0x059669,      # emerald
    "productivity": 0xD97706,     # amber
    "finances": 0x16A34A,         # green
    "budgeting": 0x16A34A,        # green
    "fitness": 0xEA580C,          # orange
    "mindfulness": 0x8B5CF6,      # purple
    "machine learning": 0x7C3AED, # violet
    "automation": 0x0284C7,       # sky
    "open source": 0x15803D,      # green
}
DEFAULT_COLOUR = 0x5865F2  # discord blurple

# ── Forum tag IDs (from the #output Forum channel) ──
FORUM_TAG_MAP = {
    "AI Agents": "1478894185091301459",
    "AI Tools": "1478894185091301460",
    "AI Strategy": "1478894185091301461",
    "Prompting": "1478894185091301462",
    "Automation": "1478894185091301463",
    "Productivity": "1478894185091301464",
    "Development": "1478894185091301465",
    "DevOps": "1478894185099821087",
    "Content Creation": "1478894185099821088",
    "Data Science": "1478894185099821089",
    "Security": "1478894185099821090",
    "Fitness": "1478894185099821091",
    "Finance": "1478894185099821092",
}

# Map AI-returned categories → forum tag names (supports multi-tag via list)
CATEGORY_TO_FORUM_TAGS = {
    "ai development": ["AI Tools"],
    "ai image generation": ["AI Tools", "Content Creation"],
    "ai saas development": ["AI Tools", "AI Strategy"],
    "ai product strategy": ["AI Strategy"],
    "ai agents": ["AI Agents"],
    "ai": ["AI Tools"],
    "machine learning": ["AI Tools", "Data Science"],
    "claude code": ["AI Tools"],
    "prompt engineering": ["Prompting", "AI Strategy"],
    "computer vision": ["Data Science", "AI Tools"],
    "data analysis": ["Data Science"],
    "data science": ["Data Science"],
    "python development": ["Development"],
    "python programming": ["Development"],
    "python": ["Development"],
    "development": ["Development"],
    "web development": ["Development"],
    "game development": ["Development"],
    "devops": ["DevOps"],
    "infrastructure as code": ["DevOps"],
    "automation": ["Automation"],
    "content creation": ["Content Creation"],
    "productivity": ["Productivity"],
    "security": ["Security"],
    "fitness": ["Fitness"],
    "finance": ["Finance"],
    "budgeting": ["Finance"],
    "finances": ["Finance"],
    "open source": ["AI Tools"],
    "mindfulness": ["Fitness"],
    "other": ["AI Tools"],
}


def get_category_colour(category: str) -> int:
    """Return a Discord embed colour based on category."""
    return CATEGORY_COLOURS.get(category.lower(), DEFAULT_COLOUR)


def resolve_forum_tags(category: str) -> list[str]:
    """Map an AI category to a list of forum tag IDs."""
    tag_names = CATEGORY_TO_FORUM_TAGS.get(category.lower(), ["AI Tools"])
    return [FORUM_TAG_MAP[n] for n in tag_names if n in FORUM_TAG_MAP]


class MegaMind(discord.Client):
    """MegaMind Discord bot client."""

    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.reactions = True
        super().__init__(intents=intents)

        self.tree = app_commands.CommandTree(self)
        self.extraction_count = 0
        self._processing_urls: set[str] = set()  # prevent duplicate processing

    async def setup_hook(self):
        """Register slash commands and start background tasks."""
        self._register_commands()
        if config.DISCORD_SERVER_ID:
            guild = discord.Object(id=config.DISCORD_SERVER_ID)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
        self.youtube_watcher_loop.start()
        log.info("Slash commands synced, YouTube watcher started")

    def _register_commands(self):
        """Register all slash commands."""

        @self.tree.command(name="extract", description="Extract insights from a URL")
        @app_commands.describe(url="The URL to extract content from")
        async def extract_command(interaction: discord.Interaction, url: str):
            await interaction.response.defer(thinking=True)
            try:
                result = await self._process_url(url, source="slash_command", requester_id=interaction.user.id)
                await interaction.followup.send(
                    f"Extraction complete: **{result['title']}** — check <#{config.DISCORD_OUTPUT_CHANNEL_ID}>"
                )
            except Exception as e:
                await interaction.followup.send(f"Extraction failed: {e}")

        @self.tree.command(name="check", description="Force check the YouTube playlist now")
        async def check_command(interaction: discord.Interaction):
            await interaction.response.defer(thinking=True)
            try:
                count = await self._check_youtube_playlist()
                await interaction.followup.send(
                    f"Playlist check complete. Found **{count}** new video(s)."
                )
            except Exception as e:
                await interaction.followup.send(f"Playlist check failed: {e}")

        @self.tree.command(name="status", description="Show MegaMind bot status")
        async def status_command(interaction: discord.Interaction):
            yt_status = "Active" if config.YOUTUBE_API_KEY and config.YOUTUBE_EXTRACT_PLAYLIST_ID else "Not configured"
            budget_info = _load_budget()
            budget_line = (
                f"API spend: **${budget_info['total_cost']:.4f}**"
                if budget_info else "API tracking: not yet started"
            )
            await interaction.response.send_message(
                f"**MegaMind Status**\n"
                f"Extractions this session: **{self.extraction_count}**\n"
                f"YouTube watcher: **{yt_status}**\n"
                f"Poll interval: **{config.YOUTUBE_POLL_INTERVAL // 60} min**\n"
                f"Extract channel: <#{config.DISCORD_EXTRACT_CHANNEL_ID}>\n"
                f"Output channel: <#{config.DISCORD_OUTPUT_CHANNEL_ID}>\n"
                f"{budget_line}"
            )

        @self.tree.command(name="search", description="Search extractions by category or tag")
        @app_commands.describe(query="Category name or tag to search for")
        async def search_command(interaction: discord.Interaction, query: str):
            from outputs.index import list_entries
            results = list_entries(status_filter=None)
            matches = []
            for line in results.split("\n"):
                if line.startswith("|") and not line.startswith("| #") and not line.startswith("|---"):
                    if query.lower() in line.lower():
                        matches.append(line)
            if matches:
                header = "| # | Title | Source | Category | Tags | Status | Date | File |\n|---|-------|--------|----------|------|--------|------|------|\n"
                table = header + "\n".join(matches[:15])
                await interaction.response.send_message(f"**Search results for `{query}`:**\n```\n{table}\n```")
            else:
                await interaction.response.send_message(f"No extractions found matching `{query}`.")

        @self.tree.command(name="budget", description="Show API usage and cost tracking")
        async def budget_command(interaction: discord.Interaction):
            from budget import format_budget_embed_text
            text = format_budget_embed_text()
            embed = discord.Embed(
                title="API Budget",
                description=text,
                colour=0x10B981,  # emerald
            )
            await interaction.response.send_message(embed=embed)

        @self.tree.command(name="dashboard", description="Get the MegaMind dashboard link")
        async def dashboard_command(interaction: discord.Interaction):
            port = int(__import__("os").getenv("DASHBOARD_PORT", "8050"))
            await interaction.response.send_message(
                f"**MegaMind Dashboard**\n"
                f"Knowledge graph, status tracking, and budget overview.\n"
                f"Open: http://localhost:{port}\n\n"
                f"Start it with: `python dashboard.py`"
            )

    async def on_ready(self):
        log.info(f"MegaMind online as {self.user} (ID: {self.user.id})")
        log.info(f"Watching #extract ({config.DISCORD_EXTRACT_CHANNEL_ID})")
        log.info(f"Posting to #output ({config.DISCORD_OUTPUT_CHANNEL_ID})")
        self._start_dashboard()

    def _start_dashboard(self):
        """Launch the dashboard web server as a background subprocess."""
        if os.getenv("MEGAMIND_DASHBOARD", "1") == "0":
            log.info("Dashboard disabled (MEGAMIND_DASHBOARD=0)")
            return
        try:
            port = os.getenv("DASHBOARD_PORT", "8050")
            self._dashboard_proc = subprocess.Popen(
                [sys.executable, str(config.PROJECT_ROOT / "dashboard.py"), "--port", port],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            log.info(f"Dashboard started (PID {self._dashboard_proc.pid}, port {port})")
        except Exception as e:
            log.warning(f"Failed to start dashboard: {e}")

    async def on_message(self, message: discord.Message):
        """Watch #extract channel for URLs."""
        # Ignore own messages
        if message.author == self.user:
            return

        # Only process messages in #extract
        if message.channel.id != config.DISCORD_EXTRACT_CHANNEL_ID:
            return

        # Find URLs in the message
        urls = URL_PATTERN.findall(message.content)
        if not urls:
            return

        # React with brain to acknowledge
        try:
            await message.add_reaction("\U0001F9E0")  # brain emoji
        except discord.HTTPException:
            pass

        # Process each URL
        for url in urls:
            if url in self._processing_urls:
                continue
            try:
                self._processing_urls.add(url)
                result = await self._process_url(url, source="discord_extract", requester_id=message.author.id)
                # React with checkmark on success
                try:
                    await message.add_reaction("\u2705")
                except discord.HTTPException:
                    pass
            except Exception as e:
                log.error(f"Failed to process {url}: {e}")
                try:
                    await message.add_reaction("\u274C")
                except discord.HTTPException:
                    pass
                await self._post_error(url, str(e))
            finally:
                self._processing_urls.discard(url)

    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """Handle robot emoji reaction on prompt messages to queue execution."""
        if payload.user_id == self.user.id:
            return

        if str(payload.emoji) != "\U0001F916":  # robot emoji
            return

        # Prompts live in threads parented to #output, or directly in #output
        channel = self.get_channel(payload.channel_id)
        if not channel:
            return

        # Check if the channel is #output or a thread inside #output
        is_output = payload.channel_id == config.DISCORD_OUTPUT_CHANNEL_ID
        is_output_thread = (
            isinstance(channel, discord.Thread)
            and channel.parent_id == config.DISCORD_OUTPUT_CHANNEL_ID
        )
        if not is_output and not is_output_thread:
            return

        try:
            message = await channel.fetch_message(payload.message_id)
        except discord.HTTPException:
            return

        # Check if the message contains a code block (prompt)
        code_blocks = re.findall(r"```(?:\w*\n)?(.*?)```", message.content, re.DOTALL)
        if not code_blocks:
            return

        prompt_text = code_blocks[0].strip()
        if not prompt_text:
            return

        # Create a GitHub Issue to queue for execution
        await self._create_execute_issue(prompt_text, message, payload)

    async def _process_url(self, url: str, source: str = "unknown", requester_id: int | None = None) -> dict:
        """Run the extraction pipeline on a URL and post results to #output."""
        log.info(f"Processing URL: {url} (source: {source})")

        # Run pipeline in executor to avoid blocking
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, run_pipeline, url)

        self.extraction_count += 1
        log.info(f"Extraction complete: {result['title']} [{result['source_type']}]")

        # Post to #output
        await self._post_output(result, requester_id=requester_id)

        # Git commit + push
        await self._git_commit(result)

        return result

    async def _post_output(self, result: dict, requester_id: int | None = None):
        """Post structured extraction as a Forum post in the #output Forum channel.

        Creates a tagged forum thread with the header embed as the opening message,
        then sends detail sections (summary, insights, prompts, etc.) as replies.
        """
        # Fetch forum channel
        channel = self.get_channel(config.DISCORD_OUTPUT_CHANNEL_ID)
        if not channel:
            try:
                channel = await self.fetch_channel(config.DISCORD_OUTPUT_CHANNEL_ID)
            except discord.HTTPException:
                log.error(f"Output channel {config.DISCORD_OUTPUT_CHANNEL_ID} not found")
                return

        processed = result["processed"]
        sections = parse_sections(processed)
        category = extract_category_from_content(processed)
        tags_text = sections.get("Tags", "")

        # ── Resolve forum tags (supports multi-tag) ──
        tag_ids = resolve_forum_tags(category)
        applied_tags = []
        if tag_ids and isinstance(channel, discord.ForumChannel):
            tag_id_set = set(tag_ids)
            for tag in channel.available_tags:
                if str(tag.id) in tag_id_set:
                    applied_tags.append(tag)
            # Discord allows max 5 applied tags per post
            applied_tags = applied_tags[:5]

        # ── Build the header embed ──
        summary_preview = sections.get("Summary", "")
        if summary_preview and len(summary_preview) > 200:
            summary_preview = summary_preview[:200] + "..."

        embed_title = result["title"]
        if len(embed_title) > 250:
            embed_title = embed_title[:247] + "..."

        embed = discord.Embed(
            title=embed_title,
            url=result["url"],
            description=summary_preview,
            colour=get_category_colour(category),
        )
        embed.add_field(name="Source", value=result["source_type"], inline=True)
        embed.add_field(name="Category", value=category, inline=True)
        if tags_text:
            embed.add_field(name="Tags", value=tags_text, inline=False)

        thumbnail = result.get("metadata", {}).get("thumbnail", "")
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)

        embed.set_footer(text=f"MegaMind | {result['date']} | {result['filename']}")

        # ── Create forum post (thread) ──
        thread_name = result["title"][:100]
        thread = None

        if isinstance(channel, discord.ForumChannel):
            try:
                thread_with_msg = await channel.create_thread(
                    name=thread_name,
                    embed=embed,
                    applied_tags=applied_tags,
                    auto_archive_duration=10080,
                )
                thread = thread_with_msg.thread
            except discord.Forbidden:
                log.error("Bot lacks permission to create forum posts")
            except discord.HTTPException as e:
                log.error(f"Failed to create forum post: {e}")
        else:
            # Fallback for non-forum channels (shouldn't happen, but safe)
            header_msg = await channel.send(embed=embed)
            try:
                thread = await header_msg.create_thread(
                    name=thread_name, auto_archive_duration=10080,
                )
            except discord.HTTPException as e:
                log.error(f"Failed to create thread: {e}")

        if not thread:
            return

        # ── Add the requester to the thread ──
        if requester_id:
            try:
                await thread.add_user(discord.Object(id=requester_id))
            except discord.HTTPException:
                pass

        # ── Detail messages inside the thread ──
        await self._send_thread_details(thread, sections)

        # ── Budget footer ──
        try:
            budget = _load_budget()
            if budget and budget["history"]:
                last = budget["history"][-1]
                await thread.send(
                    f"-# Cost: ${last['cost']:.4f} | "
                    f"Session total: ${budget['total_cost']:.4f} "
                    f"({budget['extraction_count']} extractions)"
                )
        except Exception:
            pass

    async def _send_thread_details(self, thread: discord.Thread, sections: dict):
        """Send all detail sections into an extraction thread."""
        # 1. Summary
        summary = sections.get("Summary", "")
        if summary:
            await thread.send(f"**Summary**\n{summary}")

        # 2. Key Insights
        insights = sections.get("Key Insights", "")
        if insights:
            text = f"**Key Insights**\n{insights}"
            for chunk in _split_message(text):
                await thread.send(chunk)

        # 3. Actions
        actions = sections.get("Actions", "")
        if actions:
            text = f"**Actions**\n{actions}"
            for chunk in _split_message(text):
                await thread.send(chunk)

        # 4. Implementation prompts header
        prompts_section = sections.get("Implementation Prompts", "")
        if prompts_section:
            prompts = parse_prompts(prompts_section)
            if prompts:
                await thread.send(
                    f"**Implementation Prompts** — {len(prompts)} step(s)\n"
                    f"-# React with \U0001F916 on any prompt to queue it for execution"
                )

            # 5. Individual prompts — each in its own message
            for i, prompt in enumerate(prompts, 1):
                parts = [f"**{i}. {prompt['title']}**"]

                # Context summary above the code block
                if prompt.get("context"):
                    parts.append(f"_{prompt['context']}_")

                # Prompt body in a code block
                if prompt.get("body"):
                    parts.append(f"```\n{prompt['body']}\n```")

                prompt_msg = "\n".join(parts)
                if len(prompt_msg) > 1900:
                    prompt_msg = prompt_msg[:1897] + "\n```"
                msg = await thread.send(prompt_msg)
                try:
                    await msg.add_reaction("\U0001F916")
                except discord.HTTPException:
                    pass

        # 6. Links & Resources
        links = sections.get("Links & Resources", "")
        if links:
            text = f"**Links & Resources**\n{links}"
            for chunk in _split_message(text):
                await thread.send(chunk)

    async def _post_error(self, url: str, error_msg: str):
        """Post a failure message to #output Forum channel."""
        channel = self.get_channel(config.DISCORD_OUTPUT_CHANNEL_ID)
        if not channel:
            try:
                channel = await self.fetch_channel(config.DISCORD_OUTPUT_CHANNEL_ID)
            except discord.HTTPException:
                return

        embed = discord.Embed(
            title="Extraction Failed",
            colour=0xEF4444,  # red
        )
        embed.add_field(name="URL", value=url, inline=False)
        embed.add_field(name="Error", value=error_msg[:1000], inline=False)
        embed.set_footer(text="Retry by posting the URL again in #extract, or use /extract <url>")

        if isinstance(channel, discord.ForumChannel):
            try:
                await channel.create_thread(
                    name=f"Failed: {url[:90]}",
                    embed=embed,
                    auto_archive_duration=1440,  # 1 day
                )
            except discord.HTTPException as e:
                log.error(f"Failed to post error to forum: {e}")
        else:
            await channel.send(embed=embed)

    async def _create_execute_issue(self, prompt_text: str, message: discord.Message, payload):
        """Create a GitHub Issue tagged 'execute' with the selected prompt."""
        if not config.GITHUB_TOKEN:
            log.warning("GITHUB_TOKEN not set — cannot create execute issue")
            return

        import requests

        headers = {
            "Authorization": f"token {config.GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json",
        }
        issue_body = (
            f"## Execute Prompt\n\n"
            f"Queued via MegaMind Discord bot (robot emoji reaction).\n\n"
            f"### Prompt\n```\n{prompt_text}\n```\n\n"
            f"### Source\n"
            f"- Discord message: {message.jump_url}\n"
            f"- Queued by: <@{payload.user_id}>\n"
        )

        data = {
            "title": f"[Execute] {prompt_text[:80]}",
            "body": issue_body,
            "labels": ["execute"],
        }

        loop = asyncio.get_event_loop()
        resp = await loop.run_in_executor(
            None,
            lambda: requests.post(
                f"https://api.github.com/repos/{config.GITHUB_REPO}/issues",
                headers=headers,
                json=data,
            ),
        )

        if resp.status_code == 201:
            issue_url = resp.json()["html_url"]
            log.info(f"Created execute issue: {issue_url}")
            # DM the user or post confirmation
            channel = self.get_channel(config.DISCORD_OUTPUT_CHANNEL_ID)
            if channel:
                await channel.send(
                    f"Queued for execution: {issue_url}\n"
                    f"Prompt: `{prompt_text[:100]}...`"
                )
        else:
            log.error(f"Failed to create issue: {resp.status_code} {resp.text}")

    async def _git_commit(self, result: dict):
        """Commit and push new extraction files."""
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, _git_commit_sync, result)
        except Exception as e:
            log.error(f"Git commit failed: {e}")

    # ── YouTube Playlist Watcher ──

    @tasks.loop(seconds=config.YOUTUBE_POLL_INTERVAL)
    async def youtube_watcher_loop(self):
        """Periodically check the YouTube playlist for new videos."""
        if not config.YOUTUBE_API_KEY or not config.YOUTUBE_EXTRACT_PLAYLIST_ID:
            return
        try:
            count = await self._check_youtube_playlist()
            if count > 0:
                log.info(f"YouTube watcher: processed {count} new video(s)")
        except Exception as e:
            log.error(f"YouTube watcher error: {e}")

    @youtube_watcher_loop.before_loop
    async def before_youtube_watcher(self):
        await self.wait_until_ready()

    async def _check_youtube_playlist(self) -> int:
        """Check YouTube playlist for new videos and process them."""
        from watchers.youtube_playlist import (
            get_new_playlist_videos, mark_video_processed, move_video_to_completed,
        )

        loop = asyncio.get_event_loop()
        new_videos = await loop.run_in_executor(None, get_new_playlist_videos)

        if not new_videos:
            return 0

        extract_channel = self.get_channel(config.DISCORD_EXTRACT_CHANNEL_ID)
        processed_count = 0

        for video in new_videos:
            video_url = f"https://www.youtube.com/watch?v={video['video_id']}"
            video_title = video.get("title", "Unknown")

            # Post to #extract for audit trail
            if extract_channel:
                await extract_channel.send(
                    f"[YouTube Playlist] New video detected: **{video_title}**\n{video_url}"
                )

            # Process it
            try:
                result = await self._process_url(video_url, source="youtube_playlist")
                mark_video_processed(video["video_id"])

                # Move video: remove from extract playlist, add to completed
                await loop.run_in_executor(
                    None,
                    move_video_to_completed,
                    video["video_id"],
                    video["playlist_item_id"],
                )

                processed_count += 1
            except Exception as e:
                log.error(f"Failed to process playlist video {video_url}: {e}")
                await self._post_error(video_url, f"YouTube playlist extraction failed: {e}")

        return processed_count


def _split_message(text: str, limit: int = 1900) -> list[str]:
    """Split a message into chunks that fit within Discord's character limit."""
    if len(text) <= limit:
        return [text]

    chunks = []
    lines = text.split("\n")
    current = []
    current_len = 0

    for line in lines:
        line_len = len(line) + 1  # +1 for newline
        if current_len + line_len > limit and current:
            chunks.append("\n".join(current))
            current = [line]
            current_len = line_len
        else:
            current.append(line)
            current_len += line_len

    if current:
        chunks.append("\n".join(current))

    return chunks


def _load_budget() -> dict | None:
    """Load budget summary, returning None if no data yet."""
    try:
        from budget import get_summary
        data = get_summary()
        return data if data.get("extraction_count", 0) > 0 else None
    except Exception:
        return None


def _git_commit_sync(result: dict):
    """Synchronous git add + commit + push."""
    try:
        subprocess.run(["git", "add", "extractions/"], check=True, capture_output=True)
        msg = f"Extract: {result['title'][:60]} [{result['source_type']}]"
        subprocess.run(["git", "commit", "-m", msg], check=True, capture_output=True)
        subprocess.run(["git", "push"], check=True, capture_output=True)
        log.info(f"Git: committed and pushed {result['filename']}")
    except subprocess.CalledProcessError as e:
        log.warning(f"Git operation failed: {e.stderr.decode() if e.stderr else e}")


def main():
    if not config.DISCORD_BOT_TOKEN:
        print("ERROR: DISCORD_BOT_TOKEN not set in .env")
        print("Get your bot token from https://discord.com/developers/applications")
        return

    bot = MegaMind()
    bot.run(config.DISCORD_BOT_TOKEN, log_handler=None)


if __name__ == "__main__":
    main()
