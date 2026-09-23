import json
import tempfile
import unittest
from pathlib import Path

from work_intake import IntakePolicy, WorkIntakeStore


class WorkIntakeStoreTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.store = WorkIntakeStore(self.root / "intakes.json", self.root / "audit.jsonl")
        self.policy = IntakePolicy(
            allowed_reactor_ids={101},
            allowed_executors={"hermes", "codex", "openclaw"},
            allowed_targets={"MegaMind"},
        )
        self.source = {
            "guild_id": 1,
            "channel_id": 2,
            "message_id": 3,
            "message_url": "https://discord.example/channels/1/2/3",
            "message_author_id": 4,
        }

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_capture_creates_pending_record_with_source_and_reaction_metadata(self):
        record, created = self.store.capture(
            prompt="Build the small thing safely.",
            source=self.source,
            reaction={"user_id": 101, "emoji": "🤖"},
            policy=self.policy,
        )

        self.assertTrue(created)
        self.assertEqual("pending_confirmation", record["status"])
        self.assertEqual("Build the small thing safely.", record["prompt"])
        self.assertEqual(self.source, record["source"])
        self.assertEqual({"user_id": 101, "emoji": "🤖"}, record["reaction"])
        self.assertIsNone(record["executor"])
        self.assertIsNone(record["target"])
        self.assertTrue(record["idempotency_key"])

    def test_capture_is_idempotent_for_same_reaction_event(self):
        first, first_created = self.store.capture(
            "A prompt", self.source, {"user_id": 101, "emoji": "🤖"}, self.policy
        )
        second, second_created = self.store.capture(
            "A prompt", self.source, {"user_id": 101, "emoji": "🤖"}, self.policy
        )

        self.assertTrue(first_created)
        self.assertFalse(second_created)
        self.assertEqual(first["id"], second["id"])
        self.assertEqual(1, len(self.store.list_records()))

    def test_capture_rejects_reactor_outside_allowlist(self):
        with self.assertRaisesRegex(PermissionError, "not allowlisted"):
            self.store.capture("A prompt", self.source, {"user_id": 999, "emoji": "🤖"}, self.policy)

    def test_approve_requires_allowlisted_executor_and_target_then_records_audit(self):
        record, _ = self.store.capture(
            "A prompt", self.source, {"user_id": 101, "emoji": "🤖"}, self.policy
        )

        with self.assertRaisesRegex(ValueError, "executor"):
            self.store.approve(record["id"], 101, "unknown", "MegaMind", "docs only", self.policy)
        with self.assertRaisesRegex(ValueError, "target"):
            self.store.approve(record["id"], 101, "hermes", "other-repo", "docs only", self.policy)

        approved = self.store.approve(
            record["id"], 101, "hermes", "MegaMind", "docs only", self.policy
        )

        self.assertEqual("approved", approved["status"])
        self.assertEqual("hermes", approved["executor"])
        self.assertEqual("MegaMind", approved["target"])
        self.assertEqual("docs only", approved["scope"])
        audit_events = [json.loads(line) for line in (self.root / "audit.jsonl").read_text().splitlines()]
        self.assertEqual(["captured", "approved"], [event["event"] for event in audit_events])


if __name__ == "__main__":
    unittest.main()
