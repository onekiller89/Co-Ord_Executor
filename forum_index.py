"""Small Discord Forum catalogue shared by the bot and local dashboard."""

import json
from collections import Counter
from datetime import datetime, timezone

import config

INDEX_FILE = config.PROJECT_ROOT / "data" / "forum_index.json"


def load_forum_index() -> dict:
    if INDEX_FILE.exists():
        try:
            data = json.loads(INDEX_FILE.read_text(encoding="utf-8"))
            if isinstance(data, dict) and isinstance(data.get("posts"), list):
                return data
        except (OSError, json.JSONDecodeError):
            pass
    return {"updated_at": None, "posts": []}


def _save(data: dict) -> None:
    INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    temp = INDEX_FILE.with_suffix(".tmp")
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    temp.replace(INDEX_FILE)


def _post_from_thread(channel, thread, previous: dict | None = None) -> dict:
    tag_names = {str(tag.id): tag.name for tag in channel.available_tags}
    tags = []
    for tag in getattr(thread, "applied_tags", []):
        name = getattr(tag, "name", None) or tag_names.get(str(getattr(tag, "id", tag)))
        if name:
            tags.append(name)
    created = getattr(thread, "created_at", None)
    return {"id": str(thread.id), "title": thread.name,
            "url": f"https://discord.com/channels/{channel.guild.id}/{thread.id}",
            "created_at": created.isoformat() if created else None,
            "tags": tags, "archived": bool(getattr(thread, "archived", False)),
            "filename": (previous or {}).get("filename", "")}


async def refresh_forum_index(channel) -> dict:
    """Fetch active and archived posts without trusting a stale prompt's tag IDs."""
    previous = {p["id"]: p for p in load_forum_index()["posts"] if "id" in p}
    posts = {}
    for thread in channel.threads:
        posts[str(thread.id)] = _post_from_thread(channel, thread, previous.get(str(thread.id)))
    async for thread in channel.archived_threads(limit=None):
        posts[str(thread.id)] = _post_from_thread(channel, thread, previous.get(str(thread.id)))
    data = {"updated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "posts": sorted(posts.values(), key=lambda p: p.get("created_at") or "", reverse=True)}
    _save(data)
    return data


def record_published(channel, thread, filename: str) -> None:
    data = load_forum_index()
    by_id = {p["id"]: p for p in data["posts"] if "id" in p}
    post = _post_from_thread(channel, thread, by_id.get(str(thread.id)))
    post["filename"] = filename
    by_id[post["id"]] = post
    data["posts"] = sorted(by_id.values(), key=lambda p: p.get("created_at") or "", reverse=True)
    data["updated_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    _save(data)


def forum_stats(data: dict) -> dict:
    posts = data.get("posts", [])
    tags = Counter(tag for post in posts for tag in post.get("tags", []))
    return {"available": bool(data.get("updated_at")), "updated_at": data.get("updated_at"),
            "total": len(posts), "by_tag": sorted(tags.items(), key=lambda pair: (-pair[1], pair[0])),
            "recent": posts[:5]}


def search_forum(data: dict, query: str, limit: int = 10) -> list[dict]:
    needle = query.casefold().strip().lstrip("#")
    if not needle:
        return []
    return [post for post in data.get("posts", [])
            if needle in post.get("title", "").casefold()
            or any(needle in tag.casefold() for tag in post.get("tags", []))][:limit]
