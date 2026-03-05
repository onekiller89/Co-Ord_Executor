# MegaMind /stats Command — Forum Analytics

Paste this into a fresh Claude Code session at `\\wsl.localhost\Ubuntu\`.

---

## Context

MegaMind is a Discord bot that extracts content from URLs and posts structured results to a Discord Forum channel. I want a `/stats` slash command that shows analytics about the Forum — extraction counts by tag, most active topics, recent activity, etc.

## Environment

- **Bot code:** `~/Co-Ord_Executor/discord_bot.py` (discord.py bot)
- **Bot runs as:** `systemctl --user restart megamind.service`
- **Forum channel ID:** `1478880776291487785`
- **Bot token:** stored in `~/Co-Ord_Executor/.env` as `DISCORD_BOT_TOKEN`
- **Local index:** `~/Co-Ord_Executor/extractions/INDEX.md` (catalogue of all extractions)
- **Dashboard:** Dash app on port 8050 (in `~/Co-Ord_Executor/dashboard.py`)

## Forum Tags (13 topic tags with emoji)
```
AI Agents 🤖:        1478894185091301459
AI Tools 🔧:         1478894185091301460
AI Strategy 🧠:      1478894185091301461
Prompting 💬:        1478894185091301462
Automation ⚡:       1478894185091301463
Productivity 📈:     1478894185091301464
Development 💻:      1478894185091301465
DevOps 🚀:           1478894185099821087
Content Creation 🎬: 1478894185099821088
Data Science 📊:     1478894185099821089
Security 🔒:         1478894185099821090
Fitness 💪:          1478894185099821091
Finance 💰:          1478894185099821092
```

## What To Build

### `/stats` slash command that shows:
1. **Total extractions** — count of Forum posts
2. **By tag breakdown** — how many posts per tag, sorted by count (bar chart style using text/emoji)
3. **Recent activity** — last 5 extractions with titles and dates
4. **Budget summary** — tie into existing `budget.py` module (see `/budget` command in discord_bot.py for reference)
5. **Post as embed** — clean Discord embed with fields, not raw text

### Also improve `/search`:
The current `/search` command searches the local JSON index file, not the actual Forum. Improve it to:
1. Search Forum thread titles and tags via Discord API (channel.threads)
2. Return clickable links to matching Forum posts
3. Support partial matching and case-insensitive search
4. Show tag pills in results

### Implementation Notes
- Read existing slash command patterns in `discord_bot.py` — `/budget`, `/status`, `/search` are already registered
- The `FORUM_TAG_MAP` dict in discord_bot.py has the tag name→ID mappings
- Forum posts can be fetched via `channel.archived_threads()` and `channel.threads` (active)
- discord.py ForumChannel: `isinstance(channel, discord.ForumChannel)`, `channel.available_tags`, `channel.threads`
- Keep it fast — cache tag counts if needed, Discord API calls are rate-limited
- After making changes, restart: `systemctl --user restart megamind.service`
- Test by running `/stats` and `/search test` in Discord

## Key Files to Read First
- `~/Co-Ord_Executor/discord_bot.py` — all bot code lives here
- `~/Co-Ord_Executor/budget.py` — budget tracking module
- `~/Co-Ord_Executor/outputs/index.py` — local extraction index
- `~/Co-Ord_Executor/.env` — environment config
