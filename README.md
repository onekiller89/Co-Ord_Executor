# MegaMind

Personal content capture, extraction & knowledge pipeline with agent-driven execution.

Drop a URL — get structured, actionable markdown. React with :robot: — queue it for execution.

---

## What Is This?

MegaMind is a frictionless content capture and execution system. You drop a link (YouTube video, X/Twitter thread, GitHub repo, or article) and MegaMind:

1. **Extracts** the content using the best available method per source
2. **Distils** it into structured markdown with insights, actions, and implementation prompts
3. **Posts** the output to Discord with numbered, actionable prompts
4. **Indexes** it in a centralised catalogue with category, tags, and status tracking
5. **Stores** it in Obsidian for offline access across all devices
6. **Queues execution** — react with :robot: on any prompt and it creates a GitHub Issue for action

The goal: capture great content on the go (mobile, work desktop, home PC), and when you're ready, trigger execution with a single emoji — no desktop required.

---

## Architecture

```
┌────────────────────────── INPUTS ────────────────────────────┐
│                                                               │
│  Discord #extract             YouTube Playlist "extract"     │
│  Drop any URL from any        (auto-watched, posts to        │
│  device                        #extract as audit trail)      │
│                                                               │
│  Telegram Bot                 GitHub Issues (extract label)  │
│  Forward URLs from phone      Mobile capture via GH app      │
│                                                               │
└───────────────────────────┬───────────────────────────────────┘
                            │
                            ▼
┌─────────────────── EXTRACTION ENGINE ────────────────────────┐
│                                                               │
│  Source Router → detects URL type → dispatches:               │
│                                                               │
│  YouTube    → Grok API (transcript + summary via xAI)        │
│  X/Twitter  → Grok API (thread extraction via xAI)           │
│  Articles   → readability-lxml + BeautifulSoup               │
│  GitHub     → GitHub API + README scrape                     │
│                                                               │
└───────────────────────────┬───────────────────────────────────┘
                            │
                            ▼
┌──────────────────── AI PROCESSING ───────────────────────────┐
│                                                               │
│  Claude Sonnet processes raw content into:                    │
│                                                               │
│  → Summary                                                    │
│  → Key Insights (numbered, digestible)                        │
│  → Action Items (concrete next steps)                         │
│  → Implementation Prompts (numbered, copy-paste ready)        │
│  → Context Awareness (Claude Code? OpenClaw? tailored output)│
│  → Tags + Category                                            │
│  → Source links + references                                  │
│                                                               │
└───────────────────────────┬───────────────────────────────────┘
                            │
                            ▼
┌──────────────────── OUTPUTS ─────────────────────────────────┐
│                                                               │
│  Discord #output                                              │
│     → Header embed + thread with full details                │
│     → React :robot: on any prompt to queue execution         │
│                                                               │
│  Obsidian Vault                                               │
│     → Full markdown synced across all devices                │
│                                                               │
│  extractions/INDEX.md                                         │
│     → Central catalogue: title, source, category, status     │
│                                                               │
│  Web Dashboard (localhost:8050)                               │
│     → Knowledge graph, status management, budget tracking    │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

---

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

Edit `.env` with your API keys:

| Key | Required | Purpose |
|-----|----------|---------|
| `ANTHROPIC_API_KEY` | Yes | Claude API for AI processing |
| `XAI_API_KEY` | Optional | Grok API for YouTube/Twitter extraction |
| `DISCORD_BOT_TOKEN` | For bot | Discord bot token for MegaMind |
| `DISCORD_SERVER_ID` | For bot | RussHub server ID |
| `DISCORD_EXTRACT_CHANNEL_ID` | For bot | #extract channel ID |
| `DISCORD_OUTPUT_CHANNEL_ID` | For bot | #output channel ID |
| `YOUTUBE_API_KEY` | Optional | YouTube Data API v3 for playlist watcher |
| `OBSIDIAN_VAULT_PATH` | Optional | Path to Obsidian vault for auto-sync |
| `GITHUB_TOKEN` | Optional | GitHub PAT for execute queue + Telegram bot |
| `TELEGRAM_BOT_TOKEN` | Optional | Telegram bot for mobile URL capture |

### 3. Run

```bash
# CLI — one-off extraction
python coord.py https://www.youtube.com/watch?v=example

# Discord bot (includes dashboard, YouTube watcher)
python discord_bot.py

# Or use the startup script
./start_megamind.sh
```

---

## Usage

### CLI

```
python coord.py <URL>                        Extract from URL
python coord.py --paste <type>               Manual paste (youtube|twitter|github|article)
python coord.py --list                       Show all extractions
python coord.py --list --filter "TODO"       Filter by status
python coord.py --status 3 "In Progress"     Update entry #3 status
```

### Discord Bot

The MegaMind Discord bot provides the full pipeline:

| Command | Description |
|---------|-------------|
| `/extract <url>` | Extract insights from a URL |
| `/check` | Force check the YouTube playlist now |
| `/status` | Show MegaMind bot status |
| `/search <query>` | Search extractions by category or tag |
| `/budget` | Show API usage and cost tracking |
| `/dashboard` | Get the dashboard link |

Drop any URL in **#extract** and MegaMind processes it automatically. Results appear in **#output** as a thread with full details.

### Dashboard

Auto-starts with the Discord bot (or run standalone with `python dashboard.py`).

- Interactive knowledge graph of categories, tags, and extractions
- Zoom in/out (buttons + scroll wheel), pan (click-drag)
- Graph-only mode for full-screen visualisation
- Status management directly from the dashboard
- API budget overview

Disable auto-start with `MEGAMIND_DASHBOARD=0`.

---

## Content Output Format

Every extraction produces a markdown file:

```markdown
# [Title]
> Source: YouTube | Extracted: 2025-01-15 14:30 UTC | Method: grok_api
> URL: https://...

### Summary         — What this content is about
### Key Insights    — Bullet list of takeaways
### Actions         — Checkbox list of concrete next steps
### Implementation Prompts — Copy-paste-ready prompts for Claude Code
### Links & Resources     — All referenced URLs/tools
### Tags            — For categorisation
### Category        — Primary category
```

**Context awareness:** When content mentions Claude Code, Anthropic, MCP, or similar tools, Implementation Prompts are automatically tailored with Claude Code-specific commands, slash commands, hooks, and CLAUDE.md patterns.

---

## Platform-Specific Extraction

| Source | Method | Why |
|--------|--------|-----|
| YouTube | Grok API (xAI) | Best transcript extraction, handles long videos |
| X/Twitter | Grok API (xAI) | Platform access — only xAI can reliably pull threads |
| Articles/Blogs | readability-lxml + BeautifulSoup | Clean extraction, handles most sites |
| GitHub repos | GitHub API + README scrape | Structured repo info + documentation |

All sources fall back to manual paste mode (`--paste`) if API keys aren't configured.

---

## Central Index

All extractions are tracked in [`extractions/INDEX.md`](extractions/INDEX.md):

| # | Title | Source | Category | Tags | Status | Date | File |
|---|-------|--------|----------|------|--------|------|------|
| 1 | Claude Code Tips | YouTube | Claude Code | `#claude-code` | Backlog | 2025-01-15 | [view](./2025-01-15_claude-code-tips.md) |
| 2 | AI Agents Thread | Twitter/X | AI Agents | `#agents` | TODO | 2025-01-16 | [view](./2025-01-16_ai-agents-thread.md) |

Status flow: **Backlog** → **TODO** → **In Progress** → **Done**

---

## Mobile Capture

Drop URLs from your phone — they get processed automatically.

### Option A: Discord (lowest friction)

Drop a URL in **#extract** from the Discord mobile app. MegaMind picks it up automatically.

### Option B: Telegram Bot

Forward/share URLs from any app to your personal Telegram bot. The bot creates a GitHub Issue, which GitHub Actions processes.

```bash
python telegram_bot.py
```

### Option C: GitHub Mobile App

1. Open the repo in the GitHub mobile app
2. Create a new issue — paste the URL as the title
3. Add the `extract` label
4. GitHub Actions processes it, commits the extraction, and closes the issue

### Mobile Capture Flow

```
Phone                          Cloud                         Desktop
─────                          ─────                         ───────
Share URL
  ├→ Discord #extract ──────→ MegaMind bot ────→ Extraction
  ├→ Telegram Bot ──────────→ GitHub Issue ─┐    committed
  └→ GitHub App → Issue ───────────────────┘    to repo
                               GitHub Actions     updates INDEX
                               runs coord.py      posts to #output
                               closes issue
                                                          git pull
                                                          Obsidian sync
                                                          Pick up & implement
```

---

## YouTube Playlist Watcher

MegaMind automatically polls a YouTube playlist for new videos:

1. Add videos to your "extract" playlist from any device
2. MegaMind detects them on the next poll (default: every hour)
3. Posts an audit trail message to #extract
4. Extracts and processes the video
5. Moves the video to a "completed" playlist (requires OAuth2)

**OAuth2 setup** (for playlist management):
```bash
# 1. Create OAuth Desktop credentials at console.cloud.google.com
# 2. Download JSON → save as client_secret.json in project root
python youtube_auth.py
```

---

## API Budget Tracking

MegaMind tracks token usage and estimated costs for every extraction:

- Per-extraction cost breakdown (input/output tokens, model, cost)
- Running session totals
- Last 100 entries in history
- Available via `/budget` slash command or on the dashboard

Data is persisted to `api_budget.json` and survives restarts.

---

## Discord Server Layout

| Channel | ID | Purpose |
|---------|-----|---------|
| #extract | `1476145053721301149` | **INPUT** — Drop URLs here from any device. YouTube watcher also posts here as audit trail. |
| #output | `1476146453121601639` | **OUTPUT** — Processed extracts with threaded details. React :robot: to queue execution. |

Server: **RussHub** (`1474002241319866439`)

---

## Execution Queue

When you react with :robot: on an implementation prompt in #output:

1. MegaMind detects the reaction
2. Extracts the prompt text from the code block
3. Creates a GitHub Issue tagged `execute` with the full prompt and context
4. Posts confirmation to #output with the issue link

This creates a queue of actionable tasks ready for execution.

---

## Startup

MegaMind runs inside WSL. WSL and Docker lifecycle are managed by OpenClaw — MegaMind only needs to start itself.

```bash
./start_megamind.sh    # Start bot + dashboard (background)
./stop_megamind.sh     # Stop everything
```

The dashboard auto-starts as a subprocess of the bot. Logs go to `~/.megamind/megamind.log`.

---

## Categories

| Category | Covers |
|----------|--------|
| Claude Code | Claude Code CLI, MCP servers, Anthropic SDK, prompt engineering |
| AI Agents | Agentic AI, agent frameworks, orchestration patterns |
| OpenClaw | OpenClaw bot, skills, memory, Discord/Telegram integration |
| DevOps | Ansible, Docker, Kubernetes, CI/CD, IaC, Terraform, GitOps |
| Infrastructure | VMware, networking, storage, cloud, Linux admin |
| Security | Cybersecurity, SIEM, hardening, compliance |
| Development | Python, JavaScript, shell scripting, software patterns |
| Productivity | Obsidian, PKM, workflows, time management, tools |
| Finances | Budgeting, investing, super, tax, financial planning |
| Fitness | Training, nutrition, health |
| Mindfulness | Mental health, meditation, stoicism, self-improvement |
| Machine Learning | ML, data engineering, model training |
| Automation | Scripting, scheduling, workflow automation |
| Open Source | OSS projects, contributions, community |

Categories are not fixed — the AI processor creates new ones as needed.

---

## Project Structure

```
Co-Ord_Executor/
├── coord.py                  # CLI entry point
├── discord_bot.py            # MegaMind Discord bot
├── dashboard.py              # Web dashboard (knowledge graph + status)
├── budget.py                 # API usage and cost tracking
├── telegram_bot.py           # Telegram bot for mobile URL capture
├── youtube_auth.py           # YouTube OAuth2 setup helper
├── config.py                 # Configuration (.env, paths, API keys)
├── start_megamind.sh         # Startup script
├── stop_megamind.sh          # Shutdown script
├── requirements.txt          # Python dependencies
├── .env.example              # Template for API keys and config
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
│   └── ai_processor.py       # Claude API insight extraction
├── outputs/
│   ├── formatter.py          # Markdown document formatting
│   ├── index.py              # Central INDEX.md management
│   └── storage.py            # File storage (repo + Obsidian)
├── watchers/
│   └── youtube_playlist.py   # YouTube playlist auto-watcher
└── extractions/
    └── INDEX.md              # Centralised extraction tracker
```

---

## Tech Stack

| Component | Tool |
|-----------|------|
| Runtime | Python 3.11+ on WSL2 (Ubuntu) |
| Discord Bot | discord.py — watches #extract, posts to #output, reacts to :robot: |
| YouTube Watcher | google-api-python-client — playlist polling + OAuth2 management |
| Grok/xAI | OpenAI-compatible client — transcripts + thread extraction |
| LLM | Anthropic Claude Sonnet (primary) |
| Articles | readability-lxml + BeautifulSoup |
| Obsidian | File-based via WSL mount, synced via Obsidian Sync |
| Dashboard | Python HTTPServer + Canvas-based force graph |
| Mobile Capture | Telegram bot + GitHub Actions (issue-driven) |
| Budget | JSON-based tracking with per-model pricing |

---

## Access Matrix

| Device | Input | View Output |
|--------|-------|-------------|
| Phone (Discord) | Drop URL in #extract | Read #output threads |
| Phone (Telegram) | Forward URL to bot | — |
| Work Desktop | Discord web + CLI | #output + Obsidian |
| Home PC | CLI + Discord + vault | Full access |
| Any Device | Obsidian Sync | Read-only |
| Any Browser | GitHub repo | Read-only |

---

## Roadmap

- [x] Core extraction pipeline (YouTube, Twitter, GitHub, Article)
- [x] AI processing with Claude (context-aware prompts)
- [x] CLI tool (`coord.py`)
- [x] Discord bot — watch #extract, post to #output with threads
- [x] YouTube playlist watcher with auto-extraction
- [x] Obsidian vault + GitHub storage
- [x] Central INDEX.md with status tracking
- [x] Mobile capture (Telegram bot + GitHub Actions)
- [x] :robot: reaction → GitHub Issue execute queue
- [x] API budget tracking
- [x] Web dashboard (knowledge graph, zoom/pan, status management)
- [x] Automated startup/shutdown scripts
- [ ] Risk classification per prompt (Low / Medium / High)
- [ ] OpenClaw dispatch — route low/medium prompts directly for execution
- [ ] Notion routing — high-risk prompts go to approval queue
- [ ] Execution result reporting back to #output
- [ ] PDF/DOCX document extraction
- [ ] Jina Reader API as alternative article extractor
- [ ] Native OpenClaw skill integration
- [ ] Repo rename to MegaMind

---

## Requirements

- Python 3.11+
- WSL2 (Ubuntu) on Windows 11
- Anthropic API key (for Claude processing)
- xAI API key (optional, for Grok YouTube/Twitter extraction)
- Discord bot token (for MegaMind bot)

---

## License

MIT — Russ Thompson
