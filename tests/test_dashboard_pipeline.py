"""Regression checks for the dashboard catalogue and evidence path."""

import asyncio
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import config
import forum_index
import source_evidence
from dashboard import DashboardHandler
from outputs.formatter import extract_tags_from_content, generate_filename, parse_prompts
from extractors.base import ExtractionResult
from outputs.index import update_status


class DashboardPipelineTests(unittest.TestCase):
    def test_dashboard_rejects_lan_client_even_with_localhost_host(self):
        handler = DashboardHandler.__new__(DashboardHandler)
        handler.headers = {"Host": "localhost:8050"}
        handler.client_address = ("192.168.1.50", 41000)
        with patch.dict("os.environ", {"DASHBOARD_ALLOWED_CLIENTS": ""}):
            self.assertFalse(handler._host_allowed())
        handler.client_address = ("127.0.0.1", 41000)
        self.assertTrue(handler._host_allowed())

    def test_status_updates_status_without_erasing_tags(self):
        with tempfile.TemporaryDirectory() as directory:
            index = Path(directory) / "INDEX.md"
            index.write_text(
                "| # | Title | Source | Category | Tags | Status | Date | File |\n"
                "| 1 | Useful video | YouTube | AI Agents | `#agents` `#notes` | Backlog | 2026-09-23 | [view](./note.md) |\n",
                encoding="utf-8",
            )
            with patch.object(config, "INDEX_FILE", index):
                self.assertTrue(update_status(1, "TODO"))
            self.assertIn("| `#agents` `#notes` | TODO |", index.read_text(encoding="utf-8"))
            row = index.read_text(encoding="utf-8").splitlines()[1].split("|")
            self.assertEqual(row[5].strip(), "`#agents` `#notes`")
            self.assertEqual(row[6].strip(), "TODO")

    def test_source_snapshot_is_immutable_and_review_is_private(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with patch.object(source_evidence, "SNAPSHOT_DIR", root / "snapshots"), \
                 patch.object(source_evidence, "REVIEWS_FILE", root / "reviews.json"):
                first = source_evidence.save_snapshot("note.md", "Actual captions", "https://example.org", "captions")
                second = source_evidence.save_snapshot("note.md", "Changed captions", "https://example.org", "captions")
                self.assertEqual(first, second)
                self.assertEqual(source_evidence.load_snapshot("note.md")["text"], "Actual captions")
                self.assertEqual(source_evidence.set_review("note.md", "flagged", "Check the claim")["state"], "flagged")
                self.assertEqual(source_evidence.get_review("note.md")["note"], "Check the claim")

    def test_tag_parser_ignores_other_sections(self):
        text = "### Summary\nA `#misleading` phrase.\n\n### Tags\n`#agents` `#source-review`\n\n### Category\nAI"
        self.assertEqual(extract_tags_from_content(text), ["agents", "source-review"])

    def test_repeated_source_title_gets_unique_filename(self):
        source = ExtractionResult(title="Untitled Video", url="https://youtube.com/watch?v=example",
                                  source_type="YouTube", raw_content="captions", metadata={})
        first = generate_filename(source)
        second = generate_filename(source)
        self.assertNotEqual(first, second)
        self.assertTrue(first.endswith(".md"))

    def test_no_implementation_prompt_does_not_create_forum_work_item(self):
        self.assertEqual(parse_prompts("None"), [])

    def test_forum_catalogue_counts_active_and_archived_posts(self):
        with tempfile.TemporaryDirectory() as directory:
            index = Path(directory) / "forum_index.json"
            tag = SimpleNamespace(id=7, name="AI Agents")
            active = SimpleNamespace(id=10, name="New agent", created_at=None, applied_tags=[tag], archived=False)
            archived = SimpleNamespace(id=11, name="Older agent", created_at=None, applied_tags=[tag], archived=True)

            class Channel:
                guild = SimpleNamespace(id=5)
                available_tags = [tag]
                threads = [active]

                async def archived_threads(self, limit=None):
                    yield archived

            with patch.object(forum_index, "INDEX_FILE", index):
                data = asyncio.run(forum_index.refresh_forum_index(Channel()))
                self.assertEqual(forum_index.forum_stats(data)["total"], 2)
                self.assertEqual(dict(forum_index.forum_stats(data)["by_tag"]), {"AI Agents": 2})
                self.assertEqual(len(forum_index.search_forum(data, "#agents")), 2)
                self.assertTrue(data["posts"][0]["url"].startswith("https://discord.com/channels/5/"))


if __name__ == "__main__":
    unittest.main()
