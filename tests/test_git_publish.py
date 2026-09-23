import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import config
from discord_bot import _git_commit_sync


class GitPublishTests(unittest.TestCase):
    def test_rejects_feature_branch_and_excludes_staged_code_on_main(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            remote = root / "remote.git"
            checkout = root / "checkout"

            def git(*args: str, cwd: Path = checkout) -> str:
                completed = subprocess.run(
                    ["git", *args], cwd=cwd, check=True, capture_output=True, text=True
                )
                return completed.stdout.strip()

            git("init", "--bare", str(remote), cwd=root)
            git("init", "-b", "main", str(checkout), cwd=root)
            git("config", "user.name", "Test")
            git("config", "user.email", "test@example.invalid")
            git("remote", "add", "origin", str(remote))
            (checkout / "extractions").mkdir()
            (checkout / "extractions" / "INDEX.md").write_text("# Index\n")
            (checkout / "app.py").write_text("original\n")
            git("add", ".")
            git("commit", "-m", "Initial")
            git("push", "-u", "origin", "main")
            initial_head = git("rev-parse", "HEAD")

            result = {"title": "Example", "source_type": "YouTube", "filename": "new.md"}
            with patch.object(config, "PROJECT_ROOT", checkout):
                git("switch", "-c", "feature")
                (checkout / "extractions" / "new.md").write_text("new extraction\n")
                _git_commit_sync(result)
                self.assertEqual(initial_head, git("rev-parse", "refs/heads/main"))

                git("switch", "main")
                (checkout / "app.py").write_text("unrelated staged code\n")
                git("add", "app.py")
                _git_commit_sync(result)

            remote_head = git("rev-parse", "refs/heads/main", cwd=remote)
            self.assertEqual(git("rev-parse", "HEAD"), remote_head)
            self.assertEqual("new extraction", git("show", "HEAD:extractions/new.md"))
            self.assertEqual("original", git("show", "HEAD:app.py"))
            self.assertEqual("M", git("diff", "--cached", "--name-status", "--", "app.py").split()[0])

            other = root / "other"
            git("clone", "--branch", "main", str(remote), str(other), cwd=root)
            git("config", "user.name", "Other", cwd=other)
            git("config", "user.email", "other@example.invalid", cwd=other)
            (other / "extractions" / "other.md").write_text("remote update\n")
            git("add", "extractions/other.md", cwd=other)
            git("commit", "-m", "Other extraction", cwd=other)
            git("push", "origin", "main", cwd=other)

            (checkout / "extractions" / "later.md").write_text("local update\n")
            with patch.object(config, "PROJECT_ROOT", checkout):
                _git_commit_sync({**result, "filename": "later.md"})
            self.assertEqual(remote_head, git("rev-parse", "HEAD"))
            self.assertTrue((checkout / "extractions" / "later.md").exists())


if __name__ == "__main__":
    unittest.main()
