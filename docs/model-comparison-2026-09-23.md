# MegaMind model comparison, 23 September 2026

## Decision

Use **GPT-6 Astra through the signed-in Codex CLI** for YouTube analysis, with **Claude Opus 5.5 through the existing Anthropic API** as the operational fallback. The five-way trial favoured Astra for source-grounded, practical actions; Opus 5.5 was close and often preserved more named details. Codex subscription use draws from its usage allowance and has no measured per-call API dollar cost. It is separate from OpenAI API billing.

## Method

- Recovered captions tied to the video IDs of the ten latest source-backed YouTube notes, #75–84. All ten were available. The source text ranged from 1,961 to 169,552 characters.
- Submitted the same seven-section, 400-word-limit instructions and each source to five currently reachable models. Anthropic models used the existing API key; GPT models used the signed-in Codex CLI, version 0.156.1, at medium reasoning effort in read-only, ephemeral runs.
- Checked all 50 outputs for completion, seven headings, original URL, four insights, three actions and 400-word limit. Spot-reviewed five sources for fidelity, important qualifications, clarity and whether the actions are worth doing.
- Private source texts, outputs, hashes and token receipts stay outside Git. `scripts/compare_models.py` and `scripts/score_model_comparison.py` reproduce the run with `MEGAMIND_EVAL_DIR` set to a private folder.

| Model | Reachable route | Outputs complete | Mean words | Mean seconds | Measured ten-call charge |
|---|---|---:|---:|---:|---:|
| GPT-6 Astra | Codex subscription | 10/10 | 332 | 24.3 | No API charge; subscription allowance used |
| Claude Opus 5.5 | Anthropic API | 10/10 | 359 | 15.4 | ~US$0.757 |
| GPT-6 Sol | Codex subscription | 10/10 | 264 | 21.8 | No API charge; subscription allowance used |
| Claude Sonnet 5 | Anthropic API | 10/10 | 290 | 10.8 | ~US$0.307 |
| GPT-6 Luna | Codex subscription | 10/10 | 240 | 17.3 | No API charge; subscription allowance used |

All 50 outputs included all seven headings, the original URL, exactly three checkbox actions and fewer than 400 words. Forty-nine had exactly four insights; Sonnet 5 returned five on one source. The measured Anthropic charges are calculated from API usage receipts and published input/output rates, not invoice figures. Codex runs did not expose comparable per-call token receipts, so their dollar cost is **not** represented as zero for an API deployment.

## What the spot review found

- **Astra:** Best at separating what the video actually said from what it proved. It kept practical caveats and proposed small tests with observable results. The long agent-course output retained the read-only-first tool guidance and called the productivity claims unverified.
- **Opus 5.5:** Close on quality, with more names and numbers. On the short promotional clip it explicitly asked to verify the repository and permissions before installing. The extra detail made some notes longer than needed.
- **Sol:** Clear and restrained. It often removed the names and specifics that would help a reader act later.
- **Sonnet 5:** Fast and good value, but more likely in the reviewed samples to carry a speaker's sweeping claim or recommend a broad tool connection without a small validation step.
- **Luna:** Consistently concise, but its actions were usually too general for MegaMind's main purpose.

The spot review covered five of ten sources, not a blinded human rating of every factual claim. The comparison also mixes Anthropic API and Codex CLI runtimes, so latency and cost are not controlled provider benchmarks. Quality conclusions are task-specific and should be revisited if the prompt or source mix changes.

## Current published rates and plan boundary

Published API rates per million input/output text tokens: [Astra US$10/50](https://developers.openai.com/api/docs/models/gpt-6-astra), [Sol US$2/10](https://developers.openai.com/api/docs/models/gpt-6-sol), [Luna US$0.10/0.50](https://developers.openai.com/api/docs/models/gpt-6-luna), [Opus 5.5 US$4/20](https://platform.claude.com/docs/en/models/opus-5-5/overview), [Sonnet 5 US$2/10](https://platform.claude.com/docs/en/models/sonnet-5/overview). [ChatGPT/Codex and API billing are separate](https://help.openai.com/en/articles/9039756-managing-billing-for-chatgpt-and-the-api-platform). Rates and model access can change.

## Operational change

`MODEL_PROVIDER=codex`, `CODEX_MODEL=gpt-6-astra` and the signed-in `CODEX_CLI` path select the primary. An Anthropic key plus `CLAUDE_MODEL=claude-opus-5-5` gives a fallback if Codex fails. Each new note records its analysis model. The shared `prompts/analysis-v2.md` keeps output short and asks the model to attribute unverified claims. Source snapshots are local and never published with the notes.
