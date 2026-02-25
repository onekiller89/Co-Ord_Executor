#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────
#  MegaMind auto-start script (runs inside WSL)
#
#  This script is invoked by the Windows startup shortcut/task.
#  It waits for networking, activates the venv (if present),
#  and launches the Discord bot in the background.
#
#  Usage (manual):   ./start_megamind.sh
#  Logs:             ~/.megamind/megamind.log
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

# ── Wait for network (DNS resolution) ──
echo "[MegaMind] Waiting for network..."
for i in $(seq 1 30); do
    if ping -c1 -W2 discord.com &>/dev/null; then
        echo "[MegaMind] Network ready."
        break
    fi
    sleep 2
done

cd "$PROJECT_DIR"

# ── Activate venv if it exists ──
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
fi

# ── Launch MegaMind Discord Bot ──
echo "[MegaMind] Starting bot at $(date)..." | tee -a "$LOG_FILE"
nohup python3 discord_bot.py >> "$LOG_FILE" 2>&1 &
BOT_PID=$!
echo "$BOT_PID" > "$PID_FILE"
echo "[MegaMind] Bot started (PID $BOT_PID). Logs: $LOG_FILE"

# ── Launch Dashboard (optional) ──
DASHBOARD_LOG="$LOG_DIR/dashboard.log"
DASHBOARD_PID_FILE="$LOG_DIR/dashboard.pid"
if [ "${MEGAMIND_DASHBOARD:-1}" = "1" ]; then
    echo "[MegaMind] Starting dashboard..." | tee -a "$DASHBOARD_LOG"
    nohup python3 dashboard.py >> "$DASHBOARD_LOG" 2>&1 &
    DASH_PID=$!
    echo "$DASH_PID" > "$DASHBOARD_PID_FILE"
    echo "[MegaMind] Dashboard started (PID $DASH_PID, port ${DASHBOARD_PORT:-8050}). Logs: $DASHBOARD_LOG"
fi
