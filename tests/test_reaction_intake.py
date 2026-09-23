import asyncio
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

import config
from discord_bot import MegaMind
from work_intake import WorkIntakeStore


class ReactionCaptureTests(unittest.TestCase):
    def test_allowlisted_robot_reaction_records_pending_intake_without_executor(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            previous = {
                "enabled": config.DISCORD_WORK_INTAKE_ENABLED,
                "reactors": config.DISCORD_WORK_INTAKE_REACTOR_IDS,
                "executors": config.WORK_INTAKE_ALLOWED_EXECUTORS,
                "targets": config.WORK_INTAKE_ALLOWED_TARGETS,
                "output": config.DISCORD_OUTPUT_CHANNEL_ID,
            }
            try:
                config.DISCORD_WORK_INTAKE_ENABLED = True
                config.DISCORD_WORK_INTAKE_REACTOR_IDS = {101}
                config.WORK_INTAKE_ALLOWED_EXECUTORS = {"hermes"}
                config.WORK_INTAKE_ALLOWED_TARGETS = {"MegaMind"}
                config.DISCORD_OUTPUT_CHANNEL_ID = 2
                message = SimpleNamespace(
                    author=SimpleNamespace(id=777),
                    content="**Prompt**\n```Build docs only```",
                    jump_url="https://discord.example/channels/1/2/3",
                )

                class Channel:
                    id = 2

                    async def fetch_message(self, message_id):
                        if message_id != 3:
                            raise AssertionError(f"unexpected message id: {message_id}")
                        return message

                fake_bot = SimpleNamespace(
                    user=SimpleNamespace(id=777),
                    get_channel=lambda channel_id: Channel(),
                    work_intakes=WorkIntakeStore(root / "records.json", root / "audit.jsonl"),
                )
                payload = SimpleNamespace(
                    user_id=101, emoji="🤖", channel_id=2, message_id=3, guild_id=1
                )

                asyncio.run(MegaMind.on_raw_reaction_add(fake_bot, payload))

                records = fake_bot.work_intakes.list_records()
                self.assertEqual(1, len(records))
                self.assertEqual("pending_confirmation", records[0]["status"])
                self.assertEqual("Build docs only", records[0]["prompt"])
                self.assertIsNone(records[0]["executor"])
            finally:
                config.DISCORD_WORK_INTAKE_ENABLED = previous["enabled"]
                config.DISCORD_WORK_INTAKE_REACTOR_IDS = previous["reactors"]
                config.WORK_INTAKE_ALLOWED_EXECUTORS = previous["executors"]
                config.WORK_INTAKE_ALLOWED_TARGETS = previous["targets"]
                config.DISCORD_OUTPUT_CHANNEL_ID = previous["output"]


if __name__ == "__main__":
    unittest.main()
