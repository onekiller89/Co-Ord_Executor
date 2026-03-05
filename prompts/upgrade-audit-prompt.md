# OpenClaw Upgrade Audit & Execution Prompt

Paste this into a fresh Claude Code session at `\\wsl.localhost\Ubuntu\`.

---

## Context

I need to upgrade OpenClaw to the latest version. Last upgrade was v2026.2.22-2 (current). Before upgrading, I need a full audit of everything custom we've added since the last upgrade to ensure nothing gets overwritten or lost.

## Environment

- **WSL2 Ubuntu** user `aaa`, sudo password `aaa`
- **OpenClaw** installed globally: `~/.npm-global/lib/node_modules/openclaw/`
- **Config:** `~/.openclaw/openclaw.json`
- **Workspace:** `~/.openclaw/workspace-main/`
- **Service:** `systemctl --user {start|stop|restart|status} openclaw-gateway.service`
- **Secrets:** `~/.openclaw/secrets.env` (12 API keys loaded via EnvironmentFile in systemd)
- **OAuth:** `~/.openclaw/agents/main/agent/auth-profiles.json` (Claude Max subscription tokens)
- **Backup repo:** `~/openclaw-backup/` (GitHub: onekiller89/openclaw-backup)
- **Encrypted backup:** `C:\Users\russe\openclaw-backup\` (AES-256 7z, script at `~/openclaw-backup/encrypt-to-windows.sh`)
- **Upgrade script:** `~/openclaw-backup/upgrade.sh`
- **DR plan:** `~/openclaw-backup/DisasterRecovery.md`

## CRITICAL Known Gotchas

1. **`openclaw update` regenerates the systemd service** from a template — drops custom directives like `EnvironmentFile=`. After upgrade: diff new service file against `~/openclaw-backup/configs/openclaw-gateway.service` before restarting.
2. **secrets.env** holds 12 API keys (incl OLLAMA_API_KEY, ANTHROPIC_OAUTH_TOKEN fallback). Must be preserved.
3. **OAuth token** in auth-profiles.json — do NOT overwrite. Claude Max subscription, not API credits.
4. **Do NOT set `context1m: true`** in agent model params — triggers long context billing rejection on Claude Max.
5. **Keep `contextWindow` at 200000** (not 1000000) for Anthropic models.

## What I Need You To Do

### Phase 1: Pre-Upgrade Audit
1. **Read the current upgrade script** (`~/openclaw-backup/upgrade.sh`) and validate it covers all bases
2. **Audit all custom files** that could be overwritten:
   - `~/.openclaw/openclaw.json` (model config, providers, aliases)
   - `~/.openclaw/secrets.env` (API keys)
   - `~/.openclaw/agents/main/agent/auth-profiles.json` (OAuth tokens)
   - `~/.config/systemd/user/openclaw-gateway.service` (custom EnvironmentFile directive)
   - `~/.openclaw/cron/jobs.json` (cron job definitions)
   - `~/.openclaw/workspace-main/skills/` (custom skills)
   - Any other files in `~/.openclaw/` that have been customised
3. **Check what's new** — run `openclaw update --check` or equivalent to see what version is available
4. **Run encrypted backup** (`~/openclaw-backup/encrypt-to-windows.sh`) — last encrypted backup was Feb 24, needs refreshing
5. **Git backup** — ensure `~/openclaw-backup/` has latest configs committed and pushed
6. **Validate DR plan** accuracy (`~/openclaw-backup/DisasterRecovery.md`) — ensure it reflects current state

### Phase 2: Also Audit MegaMind Custom Files
Since the last upgrade, we've made significant changes to MegaMind (Co-Ord_Executor). Audit these:
- `~/Co-Ord_Executor/discord_bot.py` — Forum channel posting, multi-tag support, requester_id flow
- `~/Co-Ord_Executor/.env` — DISCORD_OUTPUT_CHANNEL_ID changed to Forum channel 1478880776291487785
- `~/Co-Ord_Executor/outputs/formatter.py` — extraction formatting
- `~/.config/systemd/user/megamind.service` — MegaMind systemd service
- Discord Forum channel (1478880776291487785) with 13 topic tags
- Channel topics updated with slash command references

### Phase 3: Execute Upgrade
1. Back up everything identified in Phase 1
2. Run the upgrade
3. Diff the new systemd service file against backup
4. Restore any overwritten custom directives
5. Restart OpenClaw
6. **End-to-end test:** Send a test message in Discord #general AND Telegram, confirm reply comes back (not just channel connection)
7. Verify MegaMind still works (send a /status command)
8. Update DR plan if anything changed

### Phase 4: Post-Upgrade
1. Update `~/openclaw-backup/` with new configs
2. Push to GitHub
3. Sync to Obsidian if relevant docs changed
4. Confirm cron jobs still firing

## Key IDs
- Discord Server: 1474002241319866439
- Russ Discord ID: 520918884350427149
- OpenClaw bot: 1474002760612708544
- MegaMind bot: 1476156237904085032
- Forum channel: 1478880776291487785
- Extract channel: 1476145053721301149
