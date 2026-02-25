#!/usr/bin/env bash
# Stop MegaMind bot (dashboard stops automatically as a child process).

LOG_DIR="$HOME/.megamind"
PID_FILE="$LOG_DIR/megamind.pid"

if [ ! -f "$PID_FILE" ]; then
    echo "[MegaMind] No PID file — may not be running."
    exit 0
fi

PID=$(cat "$PID_FILE")
if kill -0 "$PID" 2>/dev/null; then
    kill "$PID"
    rm -f "$PID_FILE"
    echo "[MegaMind] Stopped (PID $PID)."
else
    rm -f "$PID_FILE"
    echo "[MegaMind] Process $PID not found — cleaning up stale PID file."
fi
