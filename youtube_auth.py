#!/usr/bin/env python3
"""One-time OAuth2 setup for YouTube playlist management.

Run this script once to authorize MegaMind to manage your playlists:

    python youtube_auth.py

It opens a browser for Google sign-in, then saves a refresh token to
youtube_token.json.  The bot uses this token automatically from then on.
"""

import sys
from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow

# Scope needed: manage (add/remove) playlist items
SCOPES = ["https://www.googleapis.com/auth/youtube"]

PROJECT_ROOT = Path(__file__).parent.resolve()
CLIENT_SECRET_FILE = PROJECT_ROOT / "client_secret.json"
TOKEN_FILE = PROJECT_ROOT / "youtube_token.json"


def main():
    if not CLIENT_SECRET_FILE.exists():
        print(
            "ERROR: client_secret.json not found in project root.\n"
            "Download it from Google Cloud Console > APIs & Services > Credentials\n"
            "and save it as client_secret.json in the Co-Ord_Executor folder."
        )
        sys.exit(1)

    print("Starting OAuth2 flow — a browser window will open.")
    print("Sign in with the Google account that owns your YouTube playlists.\n")

    flow = InstalledAppFlow.from_client_secrets_file(
        str(CLIENT_SECRET_FILE), scopes=SCOPES
    )
    creds = flow.run_local_server(port=8090, prompt="consent")

    # Persist the credentials (including refresh token)
    TOKEN_FILE.write_text(creds.to_json())
    print(f"\nToken saved to {TOKEN_FILE}")
    print("You're all set — the bot will auto-refresh this token as needed.")


if __name__ == "__main__":
    main()
