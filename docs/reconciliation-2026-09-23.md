# MegaMind reconciliation audit, 23 September 2026

## Completed cutover

The canonical repository is now `https://github.com/onekiller89/MegaMind`. PR #8 merged the live Claude and Hermes work as commit `6411461`. A fresh `~/MegaMind` checkout on `main` runs `megamind.service`; its Discord gateway connected, the dashboard returned HTTP 200, and systemd reported no restarts. The old production and Hermes directories were renamed to `~/MegaMind-legacy-20260923` and `~/MegaMind-hermes-intake-archive`, with uncommitted work preserved and Git worktrees repaired. Protected runtime and unit backups are under `~/.local/share/megamind-migration/20260923-cutover`.

A real user message in Discord `#extract` supplied `https://www.youtube.com/watch?v=5p-sq8v3OXw`. MegaMind acknowledged it, fetched source-linked captions, completed two successful Anthropic API calls, created a 16-message `#output` forum thread with the source URL and MegaMind attribution, and marked the input successful. It committed and pushed extraction `53ad58f` to GitHub `main`; the GitHub Actions test run for that exact commit passed. The bot-owned Discord tracking message for issue #4 was updated to the new repository URL. Branding footers in 34 active extraction files were updated to the canonical URL. Historical OpenClaw audit messages and quarantined extraction records retain the former name as provenance; old GitHub links redirect.

The Codex desktop saved-project list did not contain MegaMind or the former name. No supported project-creation or path-edit tool was available, so the desktop project link remains to be added with folder `\\wsl.localhost\Ubuntu\home\aaa\MegaMind` and label `MegaMind`. Future tasks should use that folder rather than the archived checkout.

## Observed state before cutover

| Location | State at audit |
| --- | --- |
| GitHub `onekiller89/Co-Ord_Executor` | Public repository, default branch `main` at `72e4ff7`. The remote Claude branch is at `e983afc`. |
| Live WSL checkout `~/Co-Ord_Executor` | `claude/resume-previous-session-zbmzR` at `e983afc`, 73 commits ahead and 1 merge commit behind `origin/main`. Seven tracked code files are modified, plus `.hermes.md` and a Zone.Identifier metadata file untracked. The 73 commits include 67 extraction files. |
| Hermes worktree `~/Co-Ord_Executor-hermes-intake` | `hermes/megamind-safe-intake` at `c89a19f`, nine extraction commits behind the live branch. Four tracked files are modified; `work_intake.py` and two tests are untracked. |
| Live service | `megamind.service` was active. Its unit uses `~/Co-Ord_Executor` and that checkout's `.venv`. |
| Codex project | The current task used the old WSL folder, but the app's project listing did not show a saved MegaMind project. |

The one `main`-only commit is the GitHub merge of the live branch's earlier ancestor. It made no additional tree changes relative to that ancestor. Merging the live branch into a branch based on `origin/main` completed without conflict.

## Prepared locally

- Created `~/MegaMind-reconcile` on `codex/megamind-reconcile-20260923`, based on `origin/main`. Its merge commit `474c647` brought the committed live branch history onto the GitHub main line. Pull request #8 was merged.
- Captured the live checkout's seven-file diff in a private local patch at `~/.local/share/megamind-reconcile/live-20260923.patch` and applied it to the reconciliation worktree. The live checkout was not changed.
- Copied and integrated Hermes' pending intake implementation into the reconciliation worktree. It remains disabled by default. The Hermes worktree was not changed.
- Replaced active source, example config, workflow and documentation references with MegaMind in the reconciliation worktree. Quarantined extraction records were left intact to preserve provenance; active extraction footers were subsequently rebranded.
- Changed automated extraction publishing to require the `main` branch and an exact match with `origin/main`, commit only extraction files, and push explicitly to `main`. A competing remote commit makes the push fail safely.
- Added agent handoff rules in `AGENTS.md`, a dedicated intake ignore rule, and a Windows launcher that starts the existing systemd service.
- Audited all 69 YouTube records against current YouTube oEmbed metadata. The 36 URL-only `grok_api` files are preserved under `extractions/quarantine/`, with original index metadata in a manifest. Forty-eight index rows are marked `Unverified` with their original status values retained. Future YouTube extraction now requires captions tied to the video ID or an interactive transcript paste.

## Validation before cutover

Seven local unit tests passed, including a temporary Git remote that proved the publisher refuses a feature branch, excludes staged code from an extraction commit and pauses when the remote advances. The new test confirms that missing captions cannot fall through to Grok. Index validation found no broken links; it found four repeated file links inherited from earlier filename collisions. `git diff --check` and Python compilation passed. The virtual environment contains `youtube-transcript-api` 1.2.4 and `yt-dlp` 2026.6.9. The later live validation is recorded above.

The quarantine files must not be used as source evidence until re-extracted. One confirmed source/content mismatch described a Tetris tutorial for a video YouTube identifies as “How I Turn Any Business Task Into a Reusable AI Skill” by Sean Kochel. The other 33 YouTube files were sourced from captions, but their full summaries have not been individually checked.

The original production and Hermes worktrees remain available as rollback evidence under their renamed directories. The live checkout has a private copy of the ignored runtime state and a repaired virtual environment.
