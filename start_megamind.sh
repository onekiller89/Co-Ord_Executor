#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────
#  MegaMind start script
#
#  Starts the MegaMind Discord bot (and dashboard) inside an
#  already-running WSL environment.  WSL and Docker lifecycle
#  are managed by OpenClaw — this script only starts MegaMind.
#
#  Usage:   ./start_megamind.sh
#  Logs:    ~/.megamind/megamind.log
# ──────────────────────────────────────────────────────────────

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_DIR="$HOME/.megamind"
LOG_FILE="$LOG_DIR/megamind.log"
PID_FILE="$LOG_DIR/megamind.pid"

mkdir -p "$LOG_DIR"

# ── Guard against duplicate instances ──
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if kill -0 "$OLD_PID" 2>/dev/null; then
        echo "[MegaMind] Already running (PID $OLD_PID). Exiting."
        exit 0
    fi
fi

cd "$PROJECT_DIR"

# ── Activate venv if it exists ──
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
fi

# ── Launch MegaMind Discord Bot (dashboard auto-starts with it) ──
echo "[MegaMind] Starting bot at $(date)..." | tee -a "$LOG_FILE"
nohup python3 discord_bot.py >> "$LOG_FILE" 2>&1 &
BOT_PID=$!
echo "$BOT_PID" > "$PID_FILE"
echo "[MegaMind] Bot started (PID $BOT_PID). Logs: $LOG_FILE"
