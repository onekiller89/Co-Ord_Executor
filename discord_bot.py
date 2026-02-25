#!/usr/bin/env python3
"""
MegaMind — Discord Bot for Co-Ord Executor

Watches #extract for URLs, monitors a YouTube playlist, runs the extraction
pipeline, and posts structured output to #output.

Setup:
  1. Create a bot at https://discord.com/developers/applications
     - Enable MESSAGE CONTENT intent
     - Bot permissions: Send Messages, Embed Links, Read Message History,
       Add Reactions, Use Slash Commands
  2. Add DISCORD_BOT_TOKEN + channel IDs to your .env
  3. Run: python discord_bot.py

Requires: pip install discord.py google-api-python-client
"""

import asyncio
import logging
import re
import subprocess
import traceback
from datetime import datetime, timezone

import discord
from discord import app_commands
from discord.ext import tasks
import requests

import config
from coord import run_pipeline
from outputs.formatter import (
    parse_sections,
    parse_prompts,
    extract_category_from_content,
    extract_tags_from_content,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("megamind")

URL_PATTERN = re.compile(r"https?://[^\s<>\"')}\]]+")

# Colour map for category-based embed colours
CATEGORY_COLOURS = {
    "claude code": 0xD97706,
    "ai agents": 0x7C3AED,
    "ai/ml": 0x2563EB,
    "openclaw": 0x059669,
    "infrastructure as code": 0x6366F1,
    "devops": 0x0891B2,
    "security": 0xDC2626,
    "development": 0x4F46E5,
    "productivity": 0x16A34A,
    "finances": 0xCA8A04,
    "budgeting": 0xCA8A04,
    "fitness": 0xE11D48,
    "mindfulness": 0x8B5CF6,
    "open source": 0x15803D,
}
DEFAULT_COLOUR = 0x5865F2  # Discord blurple


def get_embed_colour(category: str) -> int:
    """Get an embed colour based on category."""
    return CATEGORY_COLOURS.get(category.lower(), DEFAULT_COLOUR)


def truncate(text: str, limit: int) -> str:
    """Truncate text to fit Discord limits."""
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


# ---------------------------------------------------------------------------
# Discord client
# ---------------------------------------------------------------------------

class MegaMind(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.reactions = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self._processing = set()  # Track URLs currently being processed

    async def setup_hook(self):
        if config.DISCORD_SERVER_ID:
            guild = discord.Object(id=config.DISCORD_SERVER_ID)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
        self.youtube_watcher.start()

    async def on_ready(self):
        logger.info(f"MegaMind online as {self.user} (ID: {self.user.id})")
        logger.info(f"Watching #extract ({config.DISCORD_EXTRACT_CHANNEL_ID})")
        logger.info(f"Posting to #output ({config.DISCORD_OUTPUT_CHANNEL_ID})")
        if config.YOUTUBE_EXTRACT_PLAYLIST_ID:
            logger.info(
                f"YouTube playlist watcher active "
                f"(every {config.YOUTUBE_POLL_INTERVAL_MINUTES}m)"
            )

    # ------------------------------------------------------------------
    # Message handler — watch #extract for URLs
    # ------------------------------------------------------------------

    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if message.channel.id != config.DISCORD_EXTRACT_CHANNEL_ID:
            return

        urls = URL_PATTERN.findall(message.content)
        if not urls:
            return

        for url in urls:
            if url in self._processing:
                continue
            self._processing.add(url)
            # Acknowledge receipt
            await message.add_reaction("\U0001F9E0")  # brain emoji
            asyncio.create_task(self._process_url(url, source_note="Discord #extract"))

    # ------------------------------------------------------------------
    # Reaction handler — robot emoji on #output triggers execute queue
    # ------------------------------------------------------------------

    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.channel_id != config.DISCORD_OUTPUT_CHANNEL_ID:
            return
        if str(payload.emoji) != "\U0001F916":  # robot emoji
            return

        # Ignore bot's own reactions
        if payload.user_id == self.user.id:
            return

        channel = self.get_channel(payload.channel_id)
        if not channel:
            return

        try:
            message = await channel.fetch_message(payload.message_id)
        except discord.NotFound:
            return

        # Extract prompt text from the message (look for code blocks)
        prompt_text = self._extract_prompt_from_message(message.content)
        if not prompt_text:
            return

        user = self.get_user(payload.user_id) or await self.fetch_user(payload.user_id)

        # Create GitHub Issue for execution queue
        issue_url = await self._create_execute_issue(prompt_text, user)

        if issue_url:
            await channel.send(
                f"**Queued for execution** by {user.mention}\n"
                f"Issue: {issue_url}\n"
                f"```\n{truncate(prompt_text, 200)}\n```"
            )
        else:
            await channel.send(
                f"Failed to queue prompt for execution. "
                f"Check GITHUB_TOKEN is set in .env"
            )

    # ------------------------------------------------------------------
    # YouTube playlist watcher (runs on configured interval)
    # ------------------------------------------------------------------

    @tasks.loop(minutes=1)  # Actual interval set in before_loop
    async def youtube_watcher(self):
        if not config.YOUTUBE_API_KEY or not config.YOUTUBE_EXTRACT_PLAYLIST_ID:
            return

        try:
            from watchers.youtube_playlist import get_new_videos, move_to_completed

            new_videos = await asyncio.get_event_loop().run_in_executor(
                None, get_new_videos
            )

            extract_channel = self.get_channel(config.DISCORD_EXTRACT_CHANNEL_ID)

            for video in new_videos:
                url = video["url"]
                if url in self._processing:
                    continue
                self._processing.add(url)

                # Post to #extract for audit trail
                if extract_channel:
                    await extract_channel.send(
                        f"**YouTube playlist pickup:** {video['title']}\n{url}"
                    )

                await self._process_url(
                    url,
                    source_note=f"YouTube playlist: {video['title']}",
                )

                # Attempt to move to completed playlist
                await asyncio.get_event_loop().run_in_executor(
                    None, move_to_completed, video["playlist_item_id"]
                )

        except Exception as e:
            logger.error(f"YouTube watcher error: {e}")
            output_channel = self.get_channel(config.DISCORD_OUTPUT_CHANNEL_ID)
            if output_channel:
                await output_channel.send(
                    f"**YouTube Watcher Error**\n```\n{truncate(str(e), 500)}\n```\n"
                    f"Will retry next cycle."
                )

    @youtube_watcher.before_loop
    async def before_youtube_watcher(self):
        await self.wait_until_ready()
        # Set the actual interval from config
        self.youtube_watcher.change_interval(
            minutes=config.YOUTUBE_POLL_INTERVAL_MINUTES
        )

    # ------------------------------------------------------------------
    # Core extraction pipeline
    # ------------------------------------------------------------------

    async def _process_url(self, url: str, source_note: str = ""):
        """Run the extraction pipeline and post results to #output."""
        output_channel = self.get_channel(config.DISCORD_OUTPUT_CHANNEL_ID)
        if not output_channel:
            logger.error(f"Cannot find output channel {config.DISCORD_OUTPUT_CHANNEL_ID}")
            self._processing.discard(url)
            return

        try:
            # Run the blocking pipeline in a thread
            pipeline = await asyncio.get_event_loop().run_in_executor(
                None, run_pipeline, url
            )

            result = pipeline["result"]
            processed = pipeline["processed"]
            filename = pipeline["filename"]

            # Git commit + push
            await asyncio.get_event_loop().run_in_executor(
                None, self._git_commit_and_push, filename, url
            )

            # Post to Discord
            await self._post_output(output_channel, result, processed, url, source_note)

            logger.info(f"Extraction complete: {url} -> {filename}")

        except Exception as e:
            logger.error(f"Extraction failed for {url}: {e}\n{traceback.format_exc()}")
            await output_channel.send(
                f"**Extraction Failed**\n"
                f"**URL:** {url}\n"
                f"**Source:** {source_note}\n"
                f"**Error:** ```\n{truncate(str(e), 500)}\n```\n"
                f"Retry by posting the URL again in <#{config.DISCORD_EXTRACT_CHANNEL_ID}>."
            )
        finally:
            self._processing.discard(url)

    # ------------------------------------------------------------------
    # Discord output formatting
    # ------------------------------------------------------------------

    async def _post_output(
        self,
        channel: discord.TextChannel,
        result,
        processed: str,
        url: str,
        source_note: str,
    ):
        """Post the extraction output to Discord as structured messages."""
        sections = parse_sections(processed)
        category = extract_category_from_content(processed)
        tags = extract_tags_from_content(processed)
        tags_str = " ".join(f"`#{t}`" for t in tags[:6])

        # --- Message 1: Overview embed ---
        embed = discord.Embed(
            title=truncate(result.title, 256),
            url=url,
            colour=get_embed_colour(category),
            timestamp=datetime.now(timezone.utc),
        )
        embed.add_field(name="Category", value=category, inline=True)
        embed.add_field(name="Source", value=result.source_type, inline=True)
        embed.add_field(name="Tags", value=tags_str or "—", inline=False)

        summary = sections.get("Summary", "No summary available.")
        embed.description = truncate(summary, 4000)
        embed.set_footer(text="MegaMind")

        await channel.send(embed=embed)

        # --- Message 2: Key Insights + Actions ---
        insights = sections.get("Key Insights", "")
        actions = sections.get("Actions", "")
        links = sections.get("Links & Resources", "")

        body_parts = []
        if insights:
            body_parts.append(f"**Key Insights**\n{insights}")
        if actions:
            body_parts.append(f"**Actions**\n{actions}")
        if links:
            body_parts.append(f"**Links & Resources**\n{links}")

        body_text = "\n\n".join(body_parts)
        if body_text:
            for chunk in self._chunk_message(body_text):
                await channel.send(chunk)

        # --- Messages 3+: Individual prompts in code blocks ---
        prompts_section = sections.get("Implementation Prompts", "")
        prompts = parse_prompts(prompts_section)

        for i, prompt in enumerate(prompts, 1):
            prompt_msg = (
                f"**Prompt {i}: {prompt['title']}**\n"
                f"```\n{truncate(prompt['body'], 1800)}\n```\n"
                f"React \U0001F916 to queue for execution"
            )
            msg = await channel.send(prompt_msg)
            await msg.add_reaction("\U0001F916")

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _chunk_message(text: str, limit: int = 1950) -> list[str]:
        """Split text into chunks that fit Discord's message limit."""
        if len(text) <= limit:
            return [text]

        chunks = []
        while text:
            if len(text) <= limit:
                chunks.append(text)
                break
            # Find a good break point
            split_at = text.rfind("\n", 0, limit)
            if split_at == -1 or split_at < limit // 2:
                split_at = limit
            chunks.append(text[:split_at])
            text = text[split_at:].lstrip("\n")
        return chunks

    @staticmethod
    def _extract_prompt_from_message(content: str) -> str | None:
        """Extract prompt text from a Discord message containing a code block."""
        match = re.search(r"```\n?(.*?)\n?```", content, re.DOTALL)
        if match:
            return match.group(1).strip()
        return None

    @staticmethod
    def _git_commit_and_push(filename: str, url: str):
        """Commit new extraction files and push to origin."""
        try:
            subprocess.run(
                ["git", "add", "extractions/"],
                cwd=str(config.PROJECT_ROOT),
                capture_output=True,
                check=True,
            )
            # Check if there are staged changes
            diff = subprocess.run(
                ["git", "diff", "--staged", "--quiet"],
                cwd=str(config.PROJECT_ROOT),
                capture_output=True,
            )
            if diff.returncode == 0:
                return  # Nothing to commit

            subprocess.run(
                ["git", "commit", "-m", f"Extract: {url}"],
                cwd=str(config.PROJECT_ROOT),
                capture_output=True,
                check=True,
            )
            subprocess.run(
                ["git", "push"],
                cwd=str(config.PROJECT_ROOT),
                capture_output=True,
                check=True,
            )
            logger.info(f"Git push complete for {filename}")
        except subprocess.CalledProcessError as e:
            logger.warning(f"Git operation failed: {e.stderr.decode() if e.stderr else e}")

    @staticmethod
    async def _create_execute_issue(prompt_text: str, user) -> str | None:
        """Create a GitHub Issue tagged 'execute' with the prompt text."""
        if not config.GITHUB_TOKEN:
            return None

        headers = {
            "Authorization": f"token {config.GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json",
        }
        payload = {
            "title": f"Execute: {prompt_text[:80]}",
            "body": (
                f"**Queued by:** {user.name} via MegaMind Discord bot\n\n"
                f"**Prompt:**\n```\n{prompt_text}\n```\n\n"
                f"React \U0001F916 triggered at {datetime.now(timezone.utc).isoformat()}"
            ),
            "labels": ["execute"],
        }

        try:
            resp = requests.post(
                f"https://api.github.com/repos/{config.GITHUB_REPO}/issues",
                headers=headers,
                json=payload,
                timeout=15,
            )
            if resp.status_code == 201:
                return resp.json().get("html_url", "")
        except Exception as e:
            logger.error(f"GitHub issue creation failed: {e}")
        return None


# ---------------------------------------------------------------------------
# Slash commands
# ---------------------------------------------------------------------------

client = MegaMind()


@client.tree.command(name="extract", description="Extract content from a URL")
@app_commands.describe(url="The URL to extract (YouTube, Twitter, article, GitHub)")
async def slash_extract(interaction: discord.Interaction, url: str):
    """Slash command to manually trigger extraction."""
    if not URL_PATTERN.match(url):
        await interaction.response.send_message(
            "That doesn't look like a valid URL.", ephemeral=True
        )
        return

    await interaction.response.send_message(
        f"Extraction queued: {url}\nResults will appear in <#{config.DISCORD_OUTPUT_CHANNEL_ID}>."
    )
    asyncio.create_task(
        client._process_url(url, source_note=f"/extract by {interaction.user.name}")
    )


@client.tree.command(name="check", description="Manually check YouTube playlist for new videos")
async def slash_check(interaction: discord.Interaction):
    """Slash command to manually trigger YouTube playlist check."""
    if not config.YOUTUBE_API_KEY or not config.YOUTUBE_EXTRACT_PLAYLIST_ID:
        await interaction.response.send_message(
            "YouTube playlist watcher not configured. "
            "Set YOUTUBE_API_KEY and YOUTUBE_EXTRACT_PLAYLIST_ID in .env",
            ephemeral=True,
        )
        return

    await interaction.response.send_message("Checking YouTube playlist...")
    # Manually invoke the watcher
    await client.youtube_watcher()


@client.tree.command(name="status", description="Show MegaMind status and recent extractions")
async def slash_status(interaction: discord.Interaction):
    """Show bot status."""
    from outputs.index import _count_entries, _read_index

    index = _read_index()
    count = _count_entries(index)

    yt_status = "Active" if config.YOUTUBE_EXTRACT_PLAYLIST_ID else "Not configured"
    embed = discord.Embed(
        title="MegaMind Status",
        colour=0x5865F2,
    )
    embed.add_field(name="Extractions", value=str(count), inline=True)
    embed.add_field(name="YouTube Watcher", value=yt_status, inline=True)
    embed.add_field(
        name="Poll Interval",
        value=f"{config.YOUTUBE_POLL_INTERVAL_MINUTES}m",
        inline=True,
    )
    embed.set_footer(text="MegaMind")
    await interaction.response.send_message(embed=embed)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    if not config.DISCORD_BOT_TOKEN:
        print("Error: DISCORD_BOT_TOKEN not set in .env")
        print()
        print("Setup:")
        print("  1. Go to https://discord.com/developers/applications")
        print("  2. Create a new application -> Bot")
        print("  3. Enable MESSAGE CONTENT intent under Bot -> Privileged Intents")
        print("  4. Copy the bot token and add to .env:")
        print("     DISCORD_BOT_TOKEN=your-token-here")
        print("  5. Invite bot to your server with this OAuth2 URL scope: bot + applications.commands")
        return

    if not config.DISCORD_EXTRACT_CHANNEL_ID or not config.DISCORD_OUTPUT_CHANNEL_ID:
        print("Error: Discord channel IDs not configured in .env")
        print("  DISCORD_EXTRACT_CHANNEL_ID=<your #extract channel ID>")
        print("  DISCORD_OUTPUT_CHANNEL_ID=<your #output channel ID>")
        return

    logger.info("Starting MegaMind...")
    client.run(config.DISCORD_BOT_TOKEN, log_handler=None)


if __name__ == "__main__":
    main()
