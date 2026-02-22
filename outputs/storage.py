"""Storage manager — saves extractions to Obsidian vault and local repo."""

import shutil
from pathlib import Path

import config


def save_extraction(filename: str, content: str) -> dict:
    """Save the extraction markdown to configured locations.

    Returns a dict of paths where the file was saved.
    """
    saved_to = {}

    # Always save to the extractions folder in the repo
    config.EXTRACTIONS_PATH.mkdir(parents=True, exist_ok=True)
    repo_path = config.EXTRACTIONS_PATH / filename
    repo_path.write_text(content, encoding="utf-8")
    saved_to["repo"] = str(repo_path)

    # Optionally copy to Obsidian vault
    if config.OBSIDIAN_VAULT_PATH:
        obsidian_dir = Path(config.OBSIDIAN_VAULT_PATH)
        if obsidian_dir.exists():
            obsidian_path = obsidian_dir / filename
            obsidian_path.write_text(content, encoding="utf-8")
            saved_to["obsidian"] = str(obsidian_path)
        else:
            print(f"  Warning: Obsidian vault path does not exist: {obsidian_dir}")
            print(f"  Skipping Obsidian sync. Update OBSIDIAN_VAULT_PATH in .env")

    return saved_to
