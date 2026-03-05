# Cross-Bot Integration — OpenClaw ↔ MegaMind

Paste this into a fresh Claude Code session at `\\wsl.localhost\Ubuntu\`.

---

## Context

I have two Discord bots running on the same server (RussHub):

1. **OpenClaw** — AI assistant bot (Node.js, runs as systemd service). Handles chat, skills (email, GitHub, Obsidian, weather, etc.), model switching, bash execution. Configured via `~/.openclaw/openclaw.json`.
2. **MegaMind** — Content extraction bot (Python/discord.py, runs as systemd service at `~/Co-Ord_Executor/`). Extracts content from URLs, posts to Discord Forum channel with auto-tagging.

Currently they're independent. I want them to be aware of each other and able to trigger actions cross-bot.

## Environment

- **WSL2 Ubuntu**, user `aaa`
- **OpenClaw:** `~/.npm-global/bin/openclaw`, config at `~/.openclaw/openclaw.json`, service: `openclaw-gateway.service`
  - Gateway API: `http://localhost:18789`
  - Skills dir: `~/.openclaw/workspace-main/skills/` & bundled `~/.openclaw/skills/`
  - 24 eligible skills including email, GitHub, Notion, Obsidian, etc.
  - Discord channels: #general, #ai-control, #testing, #reports, etc.
- **MegaMind:** `~/Co-Ord_Executor/discord_bot.py`, service: `megamind.service`
  - Dashboard: `http://localhost:8050`
  - Discord channels: #extract (input), #output (Forum, output)
  - Budget tracking in `~/Co-Ord_Executor/budget.py`
  - Extraction index in `~/Co-Ord_Executor/extractions/INDEX.md`

## Integration Ideas

### 1. OpenClaw skill to trigger MegaMind extraction
Create an OpenClaw skill that:
- Accepts a URL
- Calls MegaMind's extraction pipeline directly (or posts to #extract channel)
- Returns the result in the current OpenClaw conversation
- This lets users extract content from any OpenClaw channel, not just #extract

### 2. MegaMind notifying OpenClaw of new extractions
After MegaMind posts a new extraction:
- Send a summary to OpenClaw's gateway API so it's aware of new knowledge
- OpenClaw could reference recent extractions in conversations ("you recently extracted a video about CSS Grid...")
- Could use OpenClaw's Obsidian skill to ensure the extraction is indexed

### 3. Shared knowledge base queries
- OpenClaw `/search` or natural language queries that search MegaMind's extraction index
- "What have I extracted about AI agents?" → searches Forum posts and returns links
- Could use the local INDEX.md or query the Forum channel directly

### 4. Cross-bot status dashboard
- OpenClaw's `/status` could include MegaMind's status (extraction count, last extraction, budget)
- MegaMind's `/status` could show if OpenClaw is online
- Health checks between the two bots

### 5. Execution pipeline
- MegaMind extracts content with action items
- React with 🤖 on a prompt → OpenClaw picks it up and executes it
- This is partially built (GitHub Issue creation) but could be expanded to direct OpenClaw task execution

## Key Technical Details

### OpenClaw Gateway API
- Port 18789
- Can receive messages via API
- Has a skill system — custom skills are markdown files in `~/.openclaw/workspace-main/skills/`
- Skills can execute bash commands, call APIs, etc.

### MegaMind API
- No REST API currently (only Discord bot interface)
- Could add a simple Flask/FastAPI endpoint for cross-bot communication
- Extraction pipeline: `ai_processor.py` → `formatter.py` → `discord_bot.py`

### Discord Channel IDs
- Server: 1474002241319866439
- #general: 1474002242175762549
- #ai-control: 1474022861936132178
- #extract: 1476145053721301149
- #output (Forum): 1478880776291487785
- OpenClaw bot ID: 1474002760612708544
- MegaMind bot ID: 1476156237904085032

## What To Build (Start Small)
Start with the highest-value integration first:
1. **OpenClaw skill for extraction** — simplest path, just have OpenClaw post to #extract and let MegaMind handle it
2. **Shared search** — let OpenClaw query MegaMind's extraction index
3. **Status awareness** — each bot knows if the other is online

Read the existing OpenClaw skill format first: `ls ~/.openclaw/workspace-main/skills/` and read a few examples to understand the pattern. Then read `~/Co-Ord_Executor/discord_bot.py` to understand MegaMind's architecture.

Build iteratively — get one integration working end-to-end before adding more.
