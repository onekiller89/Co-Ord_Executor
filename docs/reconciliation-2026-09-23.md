# MegaMind reconciliation audit, 23 September 2026

## Observed state

| Location | State at audit |
| --- | --- |
| GitHub `onekiller89/Co-Ord_Executor` | Public repository, default branch `main` at `72e4ff7`. The remote Claude branch is at `e983afc`. |
| Live WSL checkout `~/Co-Ord_Executor` | `claude/resume-previous-session-zbmzR` at `e983afc`, 73 commits ahead and 1 merge commit behind `origin/main`. Seven tracked code files are modified, plus `.hermes.md` and a Zone.Identifier metadata file untracked. The 73 commits include 67 extraction files. |
| Hermes worktree `~/Co-Ord_Executor-hermes-intake` | `hermes/megamind-safe-intake` at `c89a19f`, nine extraction commits behind the live branch. Four tracked files are modified; `work_intake.py` and two tests are untracked. |
| Live service | `megamind.service` was active. Its unit uses `~/Co-Ord_Executor` and that checkout's `.venv`. |
| Codex project | The current task uses the old WSL folder, but the app's project listing did not show a saved MegaMind project at audit time. Confirm the saved project path and label during cutover. |

The one `main`-only commit is the GitHub merge of the live branch's earlier ancestor. It made no additional tree changes relative to that ancestor. Merging the live branch into a branch based on `origin/main` completed without conflict.

## Prepared locally

- Created `~/MegaMind-reconcile` on `codex/megamind-reconcile-20260923`, based on `origin/main`. Its merge commit `474c647` brings the committed live branch history onto the GitHub main line. The branch is published as draft pull request #8; it has not been merged.
- Captured the live checkout's seven-file diff in a private local patch at `~/.local/share/megamind-reconcile/live-20260923.patch` and applied it to the reconciliation worktree. The live checkout was not changed.
- Copied and integrated Hermes' pending intake implementation into the reconciliation worktree. It remains disabled by default. The Hermes worktree was not changed.
- Replaced active source, example config, workflow and documentation references with MegaMind in the reconciliation worktree. Historical extraction records were left intact to preserve provenance.
- Changed automated extraction publishing to require the `main` branch and an exact match with `origin/main`, commit only extraction files, and push explicitly to `main`. A competing remote commit makes the push fail safely.
- Added agent handoff rules in `AGENTS.md`, a dedicated intake ignore rule, and a Windows launcher that starts the existing systemd service.
- Audited all 69 YouTube records against current YouTube oEmbed metadata. The 36 URL-only `grok_api` files are preserved under `extractions/quarantine/`, with original index metadata in a manifest. Forty-eight index rows are marked `Unverified` with their original status values retained. Future YouTube extraction now requires captions tied to the video ID or an interactive transcript paste.

## Validation and remaining gates

Seven local unit tests passed, including a temporary Git remote that proved the publisher refuses a feature branch, excludes staged code from an extraction commit and pauses when the remote advances. The new test confirms that missing captions cannot fall through to Grok. Index validation found no broken links; it found four repeated file links inherited from earlier filename collisions. `git diff --check` and Python compilation passed. The production virtual environment contains `youtube-transcript-api` 1.2.4 and `yt-dlp` 2026.6.9. This is code validation only: the running bot, Discord delivery, YouTube extraction, GitHub Actions and the new path have not been exercised with these changes.

Before cutover, re-fetch GitHub and re-check both worktrees because the live bot may create more extraction commits. The quarantine files must not be used as source evidence until re-extracted. One confirmed source/content mismatch described a Tetris tutorial for a video YouTube identifies as “How I Turn Any Business Task Into a Reusable AI Skill” by Sean Kochel. The other 33 YouTube files were sourced from captions, but their full summaries have not been individually checked. Run a representative end-to-end extraction after restart.

The planned cutover needs one coordinated sequence: review/push the integration branch, merge to GitHub `main`, rename the GitHub repository, update remotes and documented URLs, stop the service, preserve ignored runtime files, move the production checkout to `~/MegaMind`, update the systemd unit, point the Codex project at the new folder, restart, then verify a real extraction and its GitHub commit. Retain the old checkout path and unit backup until that verification succeeds. Do not switch the production checkout while its service is running.

The original production and Hermes worktrees remain available as rollback evidence. The repository rename, production path move, service restart and Codex project relink have not been performed.
