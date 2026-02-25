@echo off
REM ──────────────────────────────────────────────────────────────
REM  MegaMind Windows Startup Script
REM
REM  Launches the MegaMind Discord bot inside WSL on boot.
REM
REM  Setup (one-time):
REM    1. Press Win+R → type: shell:startup → Enter
REM    2. Copy this file (or a shortcut) into that Startup folder
REM       OR create a Task Scheduler task (see below)
REM
REM  Task Scheduler (recommended, runs even without sign-in):
REM    1. Open Task Scheduler → Create Task
REM    2. Trigger: "At startup" or "At log on"
REM    3. Action: Start a program
REM       Program: wsl.exe
REM       Arguments: -d Ubuntu -- bash -lc "/home/user/Co-Ord_Executor/start_megamind.sh"
REM    4. Conditions: uncheck "Start only if on AC power"
REM    5. Settings: check "Run task as soon as possible after scheduled start is missed"
REM ──────────────────────────────────────────────────────────────

REM Adjust the WSL distro name if yours isn't "Ubuntu"
wsl -d Ubuntu -- bash -lc "/home/user/Co-Ord_Executor/start_megamind.sh"
