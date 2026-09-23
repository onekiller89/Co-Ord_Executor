# MegaMind collaboration rules

MegaMind has one reviewed code line: `origin/main`. Codex and Hermes use separate worktrees and short feature branches based on a freshly fetched `origin/main`. The running service checkout is for production and generated extraction data, not agent development.

Before changing code:

1. Run `git fetch origin` and `git status --short --branch` in the relevant worktree.
2. Compare `git rev-list --left-right --count origin/main...HEAD` and inspect uncommitted files. Preserve another agent's edits; never reset, clean, rebase or stash them without that agent's handoff.
3. Create a new worktree from `origin/main`, or continue the named worktree that owns the task. Record the base commit and intended files in the handoff.

For handoff, report the branch, base and tip commits, changed files, tests run, unresolved conflicts and any production effect. Integrate through one reviewed pull request. Do not directly push agent code to `main`, switch the live checkout's branch, or restart the service as a side effect of development. Generated extraction commits are the only automated GitHub writes; the bot must stop publishing if the live checkout is not `main` or is behind `origin/main`.

Keep `.env`, OAuth files, tokens, local intake records and other runtime state out of Git and agent handoffs. Reactions record pending work only. Execution, deployment and external messages require an explicit task with a named executor, target, branch and scope.

The canonical WSL checkout is `/home/aaa/MegaMind`, the repository is `https://github.com/onekiller89/MegaMind`, and `megamind.service` runs from that checkout. The legacy and Hermes intake directories are rollback archives. The Codex desktop saved-project link still needs to be added for the new folder; do not start new work from the archived checkout.
