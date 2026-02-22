# Co-Ord Executor

Co-ordinate valuable resources and make them actionable. Drop a URL, get structured markdown with insights, actions, implementation prompts, and links — ready to pick up and execute later.

## What It Does

1. **Drop a URL** — YouTube video, X/Twitter thread, GitHub repo, or any article
2. **Auto-extracts content** — Uses Grok for YouTube/Twitter (platform-aware), scraping for the rest
3. **AI-processes into structured markdown** — Insights, actions, implementation prompts, links, tags
4. **Context-aware** — If content relates to Claude Code, prompts are tailored for Claude Code CLI
5. **Saves everywhere** — To this repo's `extractions/` folder AND your Obsidian vault
6. **Tracks in a central index** — Categorised, tagged, with status tracking (Backlog → TODO → In Progress → Done)

## Quick Start

### 1. Clone and install

```bash
git clone https://github.com/onekiller89/Co-Ord_Executor.git
cd Co-Ord_Executor
python -m venv .venv
source .venv/bin/activate  # On WSL/Linux
pip install -r requirements.txt
```

### 2. Configure

```bash
cp .env.example .env
```

Edit `.env` with your API keys:

| Key | Required | Purpose |
|-----|----------|---------|
| `ANTHROPIC_API_KEY` | Yes | Claude API for AI summarisation of articles/GitHub repos |
| `XAI_API_KEY` | Optional | Grok API for YouTube/Twitter extraction (falls back to manual paste) |
| `OBSIDIAN_VAULT_PATH` | Optional | Path to your Obsidian vault folder for auto-sync |

### 3. Extract

```bash
# YouTube video (via Grok)
python coord.py https://www.youtube.com/watch?v=dQw4w9WgXcQ

# X/Twitter thread (via Grok)
python coord.py https://x.com/user/status/1234567890

# GitHub repo (scraped + Claude summary)
python coord.py https://github.com/anthropics/claude-code

# Any article/blog post
python coord.py https://example.com/great-article

# Manual paste mode (when you already have the content)
python coord.py --paste youtube
python coord.py --paste twitter
```

## Usage

```
python coord.py <URL>                        Extract from URL
python coord.py --paste <type>               Manual paste (youtube|twitter|github|article)
python coord.py --list                       Show all extractions
python coord.py --list --filter "TODO"       Filter by status
python coord.py --status 3 "In Progress"     Update entry #3 status
python coord.py --status 5 "Done"            Mark entry #5 as done
```

## Output Format

Every extraction produces a markdown file with:

```
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

## Central Index

All extractions are tracked in [`extractions/INDEX.md`](extractions/INDEX.md):

| # | Title | Source | Category | Tags | Status | Date | File |
|---|-------|--------|----------|------|--------|------|------|
| 1 | Claude Code Tips | YouTube | Claude Code | `#claude-code` | Backlog | 2025-01-15 | [view](./2025-01-15_claude-code-tips.md) |
| 2 | AI Agents Thread | Twitter/X | AI/ML | `#agents` | TODO | 2025-01-16 | [view](./2025-01-16_ai-agents-thread.md) |

Status workflow: **Backlog** → **TODO** → **In Progress** → **Done**

## How Extraction Works

| Source | Extraction Method | AI Processing |
|--------|-------------------|---------------|
| YouTube | Grok API (or manual paste) | Claude structures insights |
| Twitter/X | Grok API (or manual paste) | Claude structures insights |
| GitHub | GitHub API + README scrape | Claude summarises & extracts |
| Article | readability-lxml + BeautifulSoup | Claude structures insights |

**Context awareness:** When content mentions Claude Code, Anthropic, MCP, or similar tools, the Implementation Prompts section is automatically tailored with Claude Code-specific commands, slash commands, hooks, and CLAUDE.md patterns.

## Obsidian Integration

Set `OBSIDIAN_VAULT_PATH` in `.env` to your vault's target folder. Every extraction is automatically copied there, ready to browse in Obsidian with full tag support.

Example:
```
OBSIDIAN_VAULT_PATH=/mnt/c/Users/YourName/Documents/Obsidian/Co-Ord
```

## Project Structure

```
Co-Ord_Executor/
├── coord.py              # CLI entry point
├── config.py             # Configuration (.env, paths, API keys)
├── requirements.txt      # Python dependencies
├── .env.example          # Template for API keys and config
├── extractors/
│   ├── detector.py       # URL → source type detection
│   ├── base.py           # Base extractor interface
│   ├── youtube.py        # YouTube via Grok API / manual paste
│   ├── twitter.py        # Twitter/X via Grok API / manual paste
│   ├── github.py         # GitHub via API + scraping
│   └── article.py        # Articles via readability + scraping
├── processors/
│   └── ai_processor.py   # Claude API insight extraction
├── outputs/
│   ├── formatter.py      # Markdown document formatting
│   ├── index.py          # Central INDEX.md management
│   └── storage.py        # File storage (repo + Obsidian)
└── extractions/
    └── INDEX.md          # Centralised extraction tracker
```

## Requirements

- Python 3.11+
- Windows 11 / WSL
- Anthropic API key (for Claude summarisation)
- xAI API key (optional, for Grok YouTube/Twitter extraction)
