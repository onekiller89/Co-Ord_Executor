# MegaMind — Content Extraction & Knowledge Pipeline

Drop a URL into Discord or add a video to your YouTube playlist — MegaMind extracts the content, processes it through AI into structured insights with actionable prompts, and delivers the output to Discord, Obsidian, and a central index. React with a robot emoji to queue a prompt for execution.

## How It Works

```
INPUT                           PROCESS                         OUTPUT
─────                           ───────                         ──────
Discord #extract ──┐                                      ┌──→ Discord #output (embed + prompts)
  (post any URL)   │                                      │
                   ├──→ MegaMind Bot ──→ Pipeline ────────┼──→ Obsidian vault (markdown)
                   │     detect → extract → AI → format   │
YouTube playlist ──┘     (hourly poll)                    └──→ INDEX.md (central catalogue)
  (add a video)
                              │
                    🤖 React on a prompt
                              │
                    Queue → GitHub Issue (execute label)
                              │
                    OpenClaw picks up and runs it
```

## Quick Start

### 1. Clone and install

```bash
git clone https://github.com/onekiller89/Co-Ord_Executor.git
cd Co-Ord_Executor
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure

```bash
cp .env.example .env
```

Edit `.env` with your keys:

| Key | Required | Purpose |
|-----|----------|---------|
| `ANTHROPIC_API_KEY` | Yes | Claude API for AI processing |
| `XAI_API_KEY` | Optional | Grok API for YouTube/Twitter extraction |
| `DISCORD_BOT_TOKEN` | Yes | MegaMind Discord bot token |
| `DISCORD_SERVER_ID` | Yes | Your Discord server ID |
| `DISCORD_EXTRACT_CHANNEL_ID` | Yes | Channel ID for `#extract` |
| `DISCORD_OUTPUT_CHANNEL_ID` | Yes | Channel ID for `#output` |
| `YOUTUBE_API_KEY` | Optional | YouTube Data API for playlist watcher |
| `YOUTUBE_EXTRACT_PLAYLIST_ID` | Optional | YouTube playlist to watch |
| `OBSIDIAN_VAULT_PATH` | Optional | Obsidian vault path for auto-sync |

### 3. Create the Discord bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. New Application → Bot → copy the token
3. Enable **MESSAGE CONTENT** intent under Bot → Privileged Gateway Intents
4. OAuth2 → URL Generator → scopes: `bot` + `applications.commands`
5. Bot permissions: Send Messages, Embed Links, Read Message History, Add Reactions, Use Slash Commands
6. Invite to your server using the generated URL

### 4. Run MegaMind

```bash
python discord_bot.py
```

MegaMind will:
- Watch `#extract` for URLs and process them automatically
- Poll your YouTube playlist every hour for new videos
- Post results to `#output` with embedded summaries and code-block prompts
- Listen for robot emoji reactions on prompts to queue them for execution

## Usage

### Discord commands

| Command | Description |
|---------|-------------|
| Post a URL in `#extract` | Auto-detected and processed |
| `/extract <url>` | Manual extraction trigger |
| `/check` | Force-check YouTube playlist now |
| `/status` | Show MegaMind stats |
| React 🤖 on a prompt in `#output` | Queue prompt for execution |

### CLI (still works)

```bash
python coord.py <URL>                        # Extract from URL
python coord.py --paste <type>               # Manual paste mode
python coord.py --list                       # Show all extractions
python coord.py --list --filter "TODO"       # Filter by status
python coord.py --status 3 "In Progress"     # Update entry status
```

## Output Format

### Discord `#output`

1. **Embed** — Title, summary, category, tags, source
2. **Body** — Key insights, actions, links & resources
3. **Prompts** — Each implementation prompt in its own message with a code block, reactable with 🤖

### Markdown file (repo + Obsidian)

```
# [Title]
> Source: YouTube | Extracted: 2026-02-25 14:30 UTC | Method: grok_api
> URL: https://...

### Summary         — What this content is about
### Key Insights    — Bullet list of takeaways
### Actions         — Checkbox list of concrete next steps
### Implementation Prompts — Numbered prompts with code-block-ready text
### Links & Resources     — All referenced URLs/tools
### Tags            — For categorisation
### Category        — AI-determined (dynamic, not a fixed list)
```

## Categories

MegaMind uses AI to dynamically assign the best category — it's not limited to a fixed list. Examples include:

> Claude Code, AI Agents, AI/ML, OpenClaw, Infrastructure as Code, DevOps, Security, Development, Productivity, Finances, Budgeting, Fitness, Mindfulness, Career, Business, Open Source, Kubernetes, Data Engineering, Automation, Homelab, Leadership...

If none of the common categories fit, the AI creates a new one.

## YouTube Playlist Watcher

1. Create an **unlisted** YouTube playlist called "extract"
2. Get the playlist ID from the URL (`list=PLAYLIST_ID`)
3. Set `YOUTUBE_API_KEY` and `YOUTUBE_EXTRACT_PLAYLIST_ID` in `.env`
4. MegaMind polls hourly (configurable via `YOUTUBE_POLL_INTERVAL_MINUTES`)
5. New videos are posted to `#extract` for audit trail, then processed
6. Use `/check` in Discord to trigger an immediate check

## Execution Queue (Phase 1)

React with 🤖 on any prompt message in `#output` to queue it:

1. MegaMind captures the prompt text from the code block
2. Creates a GitHub Issue with the `execute` label
3. Posts confirmation back to `#output`

**Phase 2 (planned):** OpenClaw picks up `execute` issues and runs them autonomously.

## Central Index

All extractions are tracked in [`extractions/INDEX.md`](extractions/INDEX.md):

| # | Title | Source | Category | Tags | Status | Date | File |
|---|-------|--------|----------|------|--------|------|------|
| 1 | Claude Code Tips | YouTube | Claude Code | `#claude-code` | Backlog | 2026-02-25 | [view](./2026-02-25_claude-code-tips.md) |

Status workflow: **Backlog** → **TODO** → **In Progress** → **Done**

## Cross-Device Access

| Device | Input | View Output |
|--------|-------|-------------|
| Mobile | Discord app → `#extract` | Discord app → `#output` |
| Personal PC | Discord + YouTube playlist + CLI | Obsidian + Discord + git pull |
| Work desktop | Discord web → `#extract` | Discord web → `#output` + Obsidian |

## Architecture

```
Discord #extract ──────────────┐
  (URL posted)                 │
                               ▼
YouTube "extract" playlist ──→ MegaMind Bot (runs on personal PC)
  (hourly poll)                │
                               ├─→ Source Detector (YouTube/Twitter/GitHub/Article)
                               ├─→ Content Extractor (Grok API / scraping)
                               ├─→ AI Processor (Claude → insights + prompts)
                               ├─→ Formatter (structured markdown)
                               │
                               ├─→ Discord #output (embed + prompt messages)
                               ├─→ Obsidian vault (MegaMind/Output/)
                               ├─→ extractions/ (git commit + push)
                               └─→ INDEX.md (central catalogue)

🤖 React on prompt ──→ GitHub Issue (execute label) ──→ OpenClaw (Phase 2)
```

| Layer | Components |
|-------|-----------|
| **Input** | Discord `#extract` channel, YouTube playlist watcher, `/extract` slash command, CLI |
| **Extractors** | YouTube/Twitter via Grok API, GitHub via API, Articles via readability-lxml |
| **AI Processor** | Claude API — dynamic categories, numbered implementation prompts |
| **Output** | Discord `#output`, Obsidian vault, GitHub repo, INDEX.md |
| **Execution** | 🤖 react → GitHub Issue → OpenClaw (Phase 2) |

## Project Structure

```
Co-Ord_Executor/
├── discord_bot.py            # MegaMind Discord bot (primary interface)
├── coord.py                  # CLI entry point + reusable pipeline
├── config.py                 # Configuration (.env, paths, API keys)
├── requirements.txt          # Python dependencies
├── .env.example              # Template for all config
├── telegram_bot.py           # Legacy Telegram bot (replaced by Discord)
├── .github/workflows/
│   └── extract.yml           # GitHub Actions extraction workflow
├── extractors/
│   ├── detector.py           # URL → source type detection
│   ├── base.py               # Base extractor interface
│   ├── youtube.py            # YouTube via Grok API / manual paste
│   ├── twitter.py            # Twitter/X via Grok API / manual paste
│   ├── github.py             # GitHub via API + scraping
│   └── article.py            # Articles via readability + scraping
├── processors/
│   └── ai_processor.py       # Claude API — dynamic categories + prompts
├── outputs/
│   ├── formatter.py          # Markdown formatting + section parser
│   ├── index.py              # Central INDEX.md management
│   └── storage.py            # File storage (repo + Obsidian)
├── watchers/
│   └── youtube_playlist.py   # YouTube playlist monitor
└── extractions/
    └── INDEX.md              # Centralised extraction tracker
```

## Requirements

- Python 3.11+
- Anthropic API key (Claude)
- Discord bot token
- xAI API key (optional, for YouTube/Twitter via Grok)
- YouTube Data API key (optional, for playlist watcher)
