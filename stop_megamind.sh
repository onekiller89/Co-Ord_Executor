#!/usr/bin/env bash
# Stop MegaMind bot and dashboard.

LOG_DIR="$HOME/.megamind"

for name in megamind dashboard; do
    PID_FILE="$LOG_DIR/${name}.pid"
    if [ ! -f "$PID_FILE" ]; then
        echo "[MegaMind] No PID file for $name — may not be running."
        continue
    fi
    PID=$(cat "$PID_FILE")
    if kill -0 "$PID" 2>/dev/null; then
        kill "$PID"
        rm -f "$PID_FILE"
        echo "[MegaMind] Stopped $name (PID $PID)."
    else
        rm -f "$PID_FILE"
        echo "[MegaMind] Process $PID ($name) not found — cleaning up stale PID file."
    fi
done
