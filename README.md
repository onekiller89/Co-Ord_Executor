# MegaMind

Personal content capture, extraction & controlled work intake.

Drop a URL for structured, actionable markdown. An authorised 🤖 reaction can record a pending work intake.

---

## What Is This?

MegaMind is a content capture and work intake system. You drop a link (primarily YouTube, also GitHub or an article) and MegaMind:

1. **Extracts** the content using the best available method per source
2. **Distils** it into structured markdown with insights, actions, and implementation prompts
3. **Posts** the output to a Discord Forum channel with auto-categorised topic tags
4. **Indexes** it in a centralised catalogue with category, tags, and status tracking
5. **Stores** it in Obsidian for offline access across all devices
6. **Captures work intake** — an authorised 🤖 reaction records a pending request for separate approval

The goal: capture useful content on the go, then review implementation requests before any agent acts.

---

## Architecture

```
┌────────────────────────── INPUTS ────────────────────────────┐
│                                                               │
│  Discord #extract             YouTube Playlist "extract"     │
│  Drop any URL from any        (auto-watched, posts to        │
│  device                        #extract as audit trail)      │
│                                                               │
│  GitHub Issues (extract label)                                │
│  Mobile capture via GH app                                   │
│                                                               │
└───────────────────────────┬───────────────────────────────────┘
                            │
                            ▼
┌─────────────────── EXTRACTION ENGINE ────────────────────────┐
│                                                               │
│  Source Router → detects URL type → dispatches:               │
│                                                               │
│  YouTube    → verified captions + preserved local snapshot   │
│  X/Twitter  → existing URL handler; further work in backlog  │
│  Articles   → readability-lxml + BeautifulSoup               │
│  GitHub     → GitHub API + README scrape                     │
│                                                               │
└───────────────────────────┬───────────────────────────────────┘
                            │
                            ▼
┌──────────────────── AI PROCESSING ───────────────────────────┐
│                                                               │
│  GPT-6 Astra via Codex, with Claude Opus 5.5 API fallback:   │
│                                                               │
│  → Summary                                                    │
│  → Four source-specific insights                              │
│  → Three concrete next steps                                  │
│  → Zero or one copy-ready implementation prompt              │
│  → Tags + Category (auto-mapped to Forum topic tags)          │
│  → Source links + references                                  │
│                                                               │
└───────────────────────────┬───────────────────────────────────┘
                            │
                            ▼
┌──────────────────── OUTPUTS ─────────────────────────────────┐
│                                                               │
│  Discord Forum (#output)                                      │
│     → Each extraction = Forum post with topic tags            │
│     → Auto-categorised with up to 5 tags per post             │
│     → Filterable by tag — browse by topic                     │
│     → Authorised 🤖 reaction records a pending work intake  │
│                                                               │
│  Obsidian Vault                                               │
│     → Full markdown synced across all devices                │
│                                                               │
│  extractions/INDEX.md                                         │
│     → Central catalogue: title, source, category, status     │
│                                                               │
│  Web Dashboard (localhost:8050)                               │
│     → Searchable library, source review, Forum activity       │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## Quick Start

### 1. Clone and install

```bash
git clone https://github.com/onekiller89/MegaMind.git
cd MegaMind
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
| `XAI_API_KEY` | Optional | Grok API for X/Twitter extraction |
| `DISCORD_BOT_TOKEN` | For bot | Discord bot token for MegaMind |
| `DISCORD_SERVER_ID` | For bot | RussHub server ID |
| `DISCORD_EXTRACT_CHANNEL_ID` | For bot | #extract channel ID |
| `DISCORD_OUTPUT_CHANNEL_ID` | For bot | Forum channel ID (`1478880776291487785`) |
| `YOUTUBE_API_KEY` | Optional | YouTube Data API v3 for playlist watcher |
| `OBSIDIAN_VAULT_PATH` | Optional | Path to Obsidian vault for auto-sync |
| `DISCORD_WORK_INTAKE_ENABLED` | Optional | Enables pending intake capture; defaults to `false` |
| `DISCORD_WORK_INTAKE_REACTOR_IDS` | Optional | Comma-separated IDs authorised to capture intakes |
| `WORK_INTAKE_ALLOWED_EXECUTORS` | Optional | Executor names allowed for later approval |
| `WORK_INTAKE_ALLOWED_TARGETS` | Optional | Project aliases allowed for later approval |

### 3. Run

```bash
# CLI — one-off extraction
python coord.py https://www.youtube.com/watch?v=example

# Discord bot (includes dashboard, YouTube watcher)
python discord_bot.py

# Or via systemd (recommended)
systemctl --user start megamind.service
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

### Discord Bot — Slash Commands

| Command | Description |
|---------|-------------|
| `/extract <url>` | Extract insights from a URL |
| `/check` | Force check the YouTube playlist now |
| `/status` | Show MegaMind bot status |
| `/search <query>` | Find Forum posts by title or topic tag, with links |
| `/stats` | Forum post counts, topic activity and recent posts |
| `/budget` | Show API usage and cost tracking |
| `/dashboard` | Get the dashboard link |

Drop any URL in **#extract** and MegaMind processes it automatically. Results appear in the **#output** Forum as tagged posts.

### Dashboard

Auto-starts with the Discord bot (or run standalone with `python dashboard.py`).

- Searchable, filterable note library with readable insights and actions
- One-click source text review, method labels, flags and reviewer notes
- Workflow status editing that preserves tags in the catalogue
- Forum topics and recent posts, with links back to Discord
- Model and partial API cost provenance; Codex subscription runs have no API dollar charge

Disable auto-start with `MEGAMIND_DASHBOARD=0`.

Source review records and raw source snapshots stay under ignored local `data/` files. For older YouTube notes, **View source text** can recover captions from the same video ID; it labels these as recovered, not as the original ingestion snapshot. The source method says how text was obtained, not whether every claim in the source is true.

Dashboard workflow status edits update the local `extractions/INDEX.md`. GitHub receives them when the next extraction is published from a current production `main`. Source review decisions remain private to this WSL installation.

Model selection lives in `.env`: `MODEL_PROVIDER=codex` and `CODEX_MODEL=gpt-6-astra` use the local Codex CLI sign-in and subscription allowance. If Codex is unavailable, MegaMind uses the Anthropic API key with `CLAUDE_MODEL=claude-opus-5-5`. ChatGPT/Codex subscriptions do not pay ordinary OpenAI API charges. The concise analysis prompt is in `prompts/analysis-v2.md`.

---

## Discord Forum & Auto-Tagging

The **#output** channel is a Discord Forum (channel type 15). Each extraction becomes a Forum post, auto-tagged based on AI-detected category.

### Forum Tags (13 topic tags)

| Tag | Emoji | Covers |
|-----|-------|--------|
| AI Agents | 🤖 | Agentic AI, agent frameworks, orchestration |
| AI Tools | 🔧 | AI products, SDKs, Claude Code, APIs |
| AI Strategy | 🧠 | AI business strategy, adoption, industry trends |
| Prompting | 💬 | Prompt engineering, system prompts, techniques |
| Automation | ⚡ | Workflow automation, scripting, scheduling |
| Productivity | 📈 | PKM, Obsidian, tools, time management |
| Development | 💻 | Python, JS, web dev, software patterns |
| DevOps | 🚀 | Docker, Kubernetes, CI/CD, IaC, GitOps |
| Content Creation | 🎬 | Video, writing, design, media production |
| Data Science | 📊 | ML, data engineering, analytics, models |
| Security | 🔒 | Cybersecurity, hardening, compliance |
| Fitness | 💪 | Training, nutrition, health, mindfulness |
| Finance | 💰 | Budgeting, investing, tax, financial planning |

### Multi-Tag Support

Posts can have up to **5 tags** (Discord's limit). The AI processor assigns a primary category, which maps to one or more Forum tags via `CATEGORY_TO_FORUM_TAGS`. For example:

- "ai image generation" → **AI Tools** + **Content Creation**
- "prompt engineering" → **Prompting** + **AI Strategy**
- "data science" → **Data Science**

Tags are resolved in `discord_bot.py` via `resolve_forum_tags()` and matched against `channel.available_tags`.

### Browsing & Filtering

- Click any tag chip at the top of the Forum to filter by topic
- Posts auto-archive after inactivity but remain visible and filterable
- Archived posts unarchive when someone replies

---

## Content Output Format

Every extraction produces a markdown file and a Forum post:

```markdown
# [Title]
> Source: YouTube | Extracted: 2026-09-23 14:30 UTC | Method: youtube_transcript_api | Analysis: gpt-6-astra
> URL: https://...

### Summary         — Two plain sentences about value
### Key Insights    — Four source-specific takeaways
### Actions         — Three concrete next steps
### Implementation Prompts — At most one useful prompt, or None
### Links & Resources     — Original URL and explicitly mentioned resources
### Tags            — For categorisation
### Category        — Primary category (maps to Forum tags)
```

The analysis target is 400 words or fewer. Claims stay attributed to the speaker when MegaMind has not independently verified them.

---

## Platform-Specific Extraction

| Source | Method | Why |
|--------|--------|-----|
| YouTube | YouTube captions or yt-dlp subtitles | Transcript tied to the requested video ID |
| X/Twitter | Existing Grok URL handler | Improvements deferred; YouTube is the priority |
| Articles/Blogs | readability-lxml + BeautifulSoup | Clean extraction, handles most sites |
| GitHub repos | GitHub API + README scrape | Structured repo info + documentation |

YouTube refuses automated extraction when no verifiable captions are available. Interactive use can accept a manually copied transcript.

YouTube metadata supplies the video title when available. A model's description of a URL alone is never accepted as the video's content.

Older URL-only Grok outputs with unverified content are preserved under `extractions/quarantine/`. Their index rows are marked `Unverified`; use a transcript-backed re-extraction before relying on them.

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

Drop a URL in **#extract** from the Discord mobile app. MegaMind picks it up automatically. Results appear in the Forum with proper tagging.

### Option B: GitHub Mobile App

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
  └→ GitHub App → Issue ────→ GitHub Actions      committed
                               runs coord.py      to repo
                               closes issue       updates INDEX
                                                  posts to Forum
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
python youtube_auth.py
```

---

## API Budget Tracking

MegaMind counts Codex subscription analyses separately from tracked Anthropic API calls:

- Anthropic API cost estimate from input/output tokens and model rate
- Codex run count without a fabricated API charge
- Last 100 entries in history
- Available via `/budget`, `/stats`, or the dashboard footer

Data is persisted to `api_budget.json` and survives restarts.

---

## Discord Server Layout

| Channel | Type | ID | Purpose |
|---------|------|----|---------|
| #extract | Text | `1476145053721301149` | **INPUT** — Drop URLs here from any device. YouTube watcher posts here as audit trail. |
| #output | Forum | `1478880776291487785` | **OUTPUT** — Forum with 13 topic tags. Each extraction = tagged post. Filter by topic. |
| #general | Text | `1474002242175762549` | General chat — OpenClaw responds here. |
| #ai-control | Text | `1474022861936132178` | OpenClaw admin — model switching, status, skill management. |
| #testing | Text | `1474023043885174836` | Experimentation — test both bots freely. |

Server: **RussHub** (`1474002241319866439`)

### Bot Presence

| Bot | ID | Channels |
|-----|----|----------|
| **OpenClaw** | `1474002760612708544` | #general, #ai-control, #testing, #reports |
| **MegaMind** | `1476156237904085032` | #extract, #output (Forum) |

---

## Controlled Work Intake

When intake is enabled and an authorised user reacts with 🤖 on a MegaMind implementation prompt in the Forum:

1. MegaMind detects the reaction
2. Extracts the prompt text from the code block
3. Records a `pending_confirmation` intake with source IDs and an idempotency key
4. Appends an audit event locally

This does not execute code, create an issue or branch, or message anyone. A separate approval records the executor, target and bounded scope. Executor handoff still requires its own reviewed implementation.

Intakes are written to `data/work-intakes.json` and `data/work-intake-audit.jsonl`, which are ignored by Git. Keep their contents private.

---

## Running as a Service

MegaMind runs as a **systemd user service** on WSL2 Ubuntu:

```bash
# Service management
systemctl --user start megamind.service
systemctl --user stop megamind.service
systemctl --user restart megamind.service
systemctl --user status megamind.service

# View logs
journalctl --user -u megamind.service -f

# Service file location
~/.config/systemd/user/megamind.service
```

The service auto-starts on WSL boot (user linger enabled). The dashboard auto-starts as a subprocess.

---

## Project Structure

```
MegaMind/
├── coord.py                  # CLI entry point
├── discord_bot.py            # MegaMind Discord bot (Forum posting, auto-tagging)
├── dashboard.py              # Web dashboard (library + source review + Forum)
├── dashboard_ui.html         # Browser interface
├── source_evidence.py        # Private raw snapshots and review decisions
├── forum_index.py            # Cached Discord Forum post catalogue
├── budget.py                 # API usage and cost tracking
├── youtube_auth.py           # YouTube OAuth2 setup helper
├── config.py                 # Configuration (.env, paths, API keys)
├── requirements.txt          # Python dependencies
├── .env                      # API keys and config (not committed)
├── .env.example              # Template for API keys
├── .github/workflows/
│   └── extract.yml           # GitHub Actions extraction workflow
├── extractors/
│   ├── detector.py           # URL → source type detection
│   ├── base.py               # Base extractor interface
│   ├── youtube.py            # YouTube via captions or manual transcript
│   ├── twitter.py            # Twitter/X via Grok API
│   ├── github.py             # GitHub via API + scraping
│   └── article.py            # Articles via readability + scraping
├── processors/
│   └── ai_processor.py       # Codex analysis + Claude API fallback
├── outputs/
│   ├── formatter.py          # Discord embed + Forum post formatting
│   ├── index.py              # Central INDEX.md management
│   └── storage.py            # File storage (repo + Obsidian)
├── watchers/
│   └── youtube_playlist.py   # YouTube playlist auto-watcher
├── extractions/
│   └── INDEX.md              # Centralised extraction tracker
└── prompts/                  # Session prompts for future work
    ├── upgrade-audit-prompt.md
    ├── forum-stats-prompt.md
    └── cross-bot-integration-prompt.md
```

---

## Tech Stack

| Component | Tool |
|-----------|------|
| Runtime | Python 3.11+ on WSL2 (Ubuntu) |
| Service | systemd user service (`megamind.service`) |
| Discord Bot | discord.py — watches #extract, posts to Forum with auto-tagging |
| YouTube Watcher | google-api-python-client — playlist polling + OAuth2 management |
| Grok/xAI | OpenAI-compatible client for X/Twitter threads |
| LLM | Codex GPT-6 Astra (subscription), Claude Opus 5.5 (API fallback) |
| Articles | readability-lxml + BeautifulSoup |
| Obsidian | File-based via WSL mount, synced via Obsidian Sync |
| Dashboard | Local Python HTTPServer + searchable browser interface |
| Budget | JSON-based tracking with per-model pricing |

---

## Companion Bot: OpenClaw

MegaMind runs alongside **OpenClaw** (AI assistant bot) on the same Discord server:

- **OpenClaw** handles chat, model switching, skills (email, GitHub, Obsidian, weather, etc.)
- **MegaMind** handles content extraction and knowledge capture
- Both run as systemd user services on the same WSL2 instance
- Future: cross-bot integration (OpenClaw triggering extractions, shared search)

---

## Access Matrix

| Device | Input | View Output |
|--------|-------|-------------|
| Phone (Discord) | Drop URL in #extract | Browse Forum by tag |
| Work Desktop | Discord web + CLI | Forum + Obsidian |
| Home PC | CLI + Discord + vault | Full access |
| Any Device | Obsidian Sync | Read-only |
| Any Browser | GitHub repo | Read-only |

---

## Roadmap

- [x] Core extraction pipeline (YouTube, Twitter, GitHub, Article)
- [x] AI processing with Claude (context-aware prompts)
- [x] CLI tool (`coord.py`)
- [x] Discord bot — watch #extract, post to #output
- [x] YouTube playlist watcher with auto-extraction
- [x] Obsidian vault + GitHub storage
- [x] Central INDEX.md with status tracking
- [x] Mobile capture (GitHub Actions)
- [x] Controlled 🤖 reaction → pending local intake (disabled by default)
- [x] API budget tracking
- [x] Web dashboard (searchable library, status, source review, Forum activity)
- [x] systemd user service (`megamind.service`)
- [x] Discord Forum channel with 13 topic tags
- [x] Multi-tag auto-categorisation (up to 5 tags per post)
- [x] YouTube oEmbed title resolution
- [x] Requester ID tracking (thread visibility fix)
- [x] `/stats` command — Forum analytics (posts by tag, recent activity)
- [x] Improved `/search` — Forum thread title and tag search
- [ ] X/Twitter integration improvements — deferred while YouTube is prioritised
- [ ] Re-extraction — re-process existing URLs with updated AI processing
- [ ] OpenClaw skill integration — trigger extractions from any channel
- [ ] Cross-bot status awareness — each bot knows if the other is online
- [ ] Shared knowledge search — OpenClaw queries MegaMind's extraction index
- [ ] Risk classification per prompt (Low / Medium / High)
- [ ] OpenClaw dispatch — route low/medium prompts directly for execution
- [ ] PDF/DOCX document extraction
- [ ] Jina Reader API as alternative article extractor

---

## Requirements

- Python 3.11+
- WSL2 (Ubuntu) on Windows 11
- Anthropic API key (for Claude processing)
- xAI API key (optional, for X/Twitter extraction)
- Discord bot token (for MegaMind bot)

---

## License

MIT — Russ Thompson
