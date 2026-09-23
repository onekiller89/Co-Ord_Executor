![banner](https://img.youtube.com/vi/Y8vAQ1FgNbM/maxresdefault.jpg)

# Paste This Into Claude, Never Hit a Token Limit Again

> **Source:** YouTube | **Extracted:** 2026-07-31 06:00 UTC | **Method:** youtube_transcript_api
> **URL:** https://www.youtube.com/watch?v=Y8vAQ1FgNbM

---

### Summary
This video explains why AI tools like Claude and Codex hit token limits so quickly: every message in a conversation resends the entire conversation history, meaning reused input can account for 96%+ of total token usage. The creator shares 15 rules across three levels — manual habits, an installable "Token Saver" skill, and a local multi-agent intermediary called Ringer — to dramatically reduce token consumption without changing how you work.

---

### Key Insights

- **Reused input is the real cost driver**: On a single working day, 96% of 3.77 billion tokens were reused input from prior conversation turns — not new content. Every retry compounds this.
- **Each new message carries the entire conversation history**: LLMs have no real memory; they simulate it by resending the full conversation every turn. By message 30, your new text is a rounding error.
- **Starting a new chat when the task changes is the single biggest win**: Long conversations carry hundreds of millions of tokens of "old work" that's irrelevant to your current question.
- **Output tokens cost you twice (or more)**: Output becomes input on the next turn, and every subsequent turn — so verbose answers compound into future costs.
- **Tools/MCP servers burn tokens before you type anything**: A typical multi-tool setup (GitHub + Slack + Sentry + Grafana) consumes ~55,000 tokens in tool definitions before Claude does any actual work.
- **Carry the artifact, not the argument**: Between multi-step workflows, pass only the final result (e.g. the research report) into the next stage — not the entire research conversation that produced it.
- **The "dumbest model that gets the job done" is the right model**: Use the least capable model that still solves the task; a skill can help suggest this if you're unsure.
- **A local intermediary (like Ringer) can intercept requests before they're sent**, enabling hard token limits, cached answer retrieval, passage selection, and even skipping model calls entirely.

---

### Actions

- [ ] **Edit messages instead of correcting in a follow-up** — use the edit button to fix unclear prompts before sending, not a new reply saying "that was wrong"
- [ ] **Batch related questions into one prompt** and specify the output format (e.g. "5 bullets", "50 words", "JSON") upfront
- [ ] **Start a fresh conversation whenever the task changes** — don't continue a debugging thread for a new, unrelated question
- [ ] **Strip context between workflow stages** — when moving from research to writing, paste only the final research output, not the entire research conversation
- [ ] **Request minimal output explicitly** — ask for a paragraph, 5 bullets, or JSON instead of letting the model write at length
- [ ] **Pre-search files yourself and paste relevant snippets** — don't ask the model to search a large file when you can extract the relevant section first
- [ ] **Convert PDFs and images to plain text/markdown** before pasting — don't send rich files when only the words matter
- [ ] **Build a retrievable knowledge base** (e.g. OpenBrain or similar) for recurring facts/answers so the model can fetch rather than recalculate
- [ ] **Audit which MCP/tool servers are connected** and disconnect any that aren't needed for the current task
- [ ] **Install the Token Saver skill** into Claude Code or Codex to automate most of the above habits
- [ ] **Explore the Ringer multi-agent framework** for a local proxy that enforces hard token limits and intercepts redundant calls before they're sent

---

### Implementation Prompts

#### Prompt 1: Audit your current Claude Code token usage patterns
*Understand where your tokens are actually going before optimising. This gives you a baseline so you can measure improvement.*

> I want to audit my Claude Code usage for token efficiency. Review my current CLAUDE.md and any active MCP server configurations in this project. For each MCP server connected, list: (1) the approximate token cost of its tool definitions, (2) whether it's likely needed for my most common tasks, and (3) whether it could be conditionally loaded. Then suggest a revised CLAUDE.md that adds a section called "Token Hygiene Rules" incorporating these practices: start new threads when tasks change, request minimal output formats by default, strip old context between workflow stages, and pre-search files before asking the model to search. Output the full revised CLAUDE.md ready to paste.

---

#### Prompt 2: Create a Token Saver slash command for Claude Code
*Build a reusable `/token-saver` slash command that enforces the key token-saving habits automatically at the start of any task.*

> Create a Claude Code slash command file at `.claude/commands/token-saver.md` that implements the following token-saving protocol when invoked. The command should: (1) ask the user to state the single specific task and desired output format before proceeding, (2) remind the user to paste only the relevant file excerpts rather than whole files, (3) check if this task is a continuation of a previous thread and suggest starting fresh if the context is large, (4) recommend the minimum output length needed (bullets, JSON, paragraph, etc.), and (5) confirm whether all currently connected MCP tools are needed for this specific task or if some can be skipped. Format the command as a proper Claude Code slash command with a clear description and step-by-step instructions the model will follow.

---

#### Prompt 3: Build a workflow stage separator prompt template
*Enforce the "carry the artifact, not the argument" rule by creating a reusable template for handing off between multi-step AI workflows.*

> Create a markdown template file called `workflow-handoff-template.md` that I can use when transitioning between stages of a multi-step AI workflow (e.g. research → writing → editing). The template should: (1) have a section to paste ONLY the final output/artifact from the previous stage, (2) have a section to clearly state the next stage's goal and desired output format, (3) include an explicit instruction line telling the model to ignore anything not included in this prompt, (4) include a word/token budget field where I specify the maximum output length, and (5) have a checklist reminding me to: strip prior conversation history, convert any file sources to plain text, and confirm only necessary tools are loaded. Make it clean, copy-paste ready, and usable directly as a Claude prompt.

---

#### Prompt 4: Generate a CLAUDE.md section for MCP tool hygiene
*Reduce the ~55,000 token overhead from always-on tool definitions by creating rules that load tools conditionally based on task type.*

> I want to reduce token overhead from MCP tool definitions in my Claude Code setup. My currently connected MCP servers are: [LIST YOUR MCP SERVERS HERE — e.g. filesystem, GitHub, Slack, Brave Search]. Generate a CLAUDE.md section called "## Tool Loading Policy" that: (1) categorises each tool by task type (e.g. "only needed for git operations", "only needed for web research"), (2) provides an explicit instruction to Claude to flag when it's about to use a tool that seems unrelated to the current task, (3) includes a default policy of "use the minimum tools required", and (4) adds a reminder that tool definitions cost tokens before any work begins. Format it ready to paste into an existing CLAUDE.md.

---

#### Prompt 5: Create a personal token-efficient prompting cheat sheet
*Turn the 15 rules from the video into a scannable personal reference you can paste into any AI tool or keep in your notes.*

> Create a concise, scannable cheat sheet called "Token-Efficient AI Prompting — 15 Rules" based on these principles: (1) edit messages instead of correcting in follow-ups, (2) batch related questions with explicit output format, (3) start fresh when the task changes, (4) carry only the final artifact between workflow stages, (5) request only the output length you need, (6) pre-search files yourself and paste snippets, (7) convert PDFs/images to plain text before pasting, (8) keep a retrievable knowledge base for recurring answers, (9) only load tools the current task actually needs, (10) use compaction/context editing for long-running threads, (11) monitor context window size and anticipate hitting limits, (12) use the dumbest model that can still do the job, (13) use prompt caching for repeated API work, (14) enforce hard token limits via an intermediary if possible, (15) intercept and filter requests before they reach the model. Format as a two-column table: Rule | One-line action. Keep each action under 15 words.

---

#### Prompt 6: Design a "clean task" startup ritual for Claude Code
*Create a CLAUDE.md hook or startup instruction that automatically prompts you to assess context size and task scope at the beginning of each session.*

> Write a Claude Code session startup ritual to add to my CLAUDE.md under a section called "## Session Start Protocol". When a new Claude Code session begins, Claude should: (1) ask me to state the single task for this session in one sentence, (2) estimate roughly how large the current project context is and flag if it's likely to cause token pressure, (3) ask whether this is a continuation of a prior task or a new one (and suggest a fresh thread if it's new), (4) confirm the desired output format and length before starting any work, and (5) list which MCP tools it plans to use and ask for confirmation. Keep the protocol concise — it should take under 60 seconds to complete. Output the full CLAUDE.md section ready to paste.

---

#### Prompt 7: Write a token usage self-audit prompt
*A periodic self-audit prompt to identify your personal token waste patterns and get specific recommendations to fix them.*

> I want to audit my AI token usage habits. Based on the following description of how I typically use Claude Code [DESCRIBE YOUR TYPICAL WORKFLOW HERE — e.g. "I usually keep one long conversation going all day, paste full PDFs, ask multiple follow-up questions when something is wrong, and have 6 MCP servers always connected"], identify my top 3 token waste patterns ranked by likely impact. For each pattern: (1) explain exactly why it wastes tokens with a rough order-of-magnitude estimate of the waste, (2) give me a specific one-sentence rule to fix it, and (3) provide a concrete example showing the wasteful approach vs. the efficient approach side by side. Then give me a single "Token Budget Pledge" — a 3-bullet personal commitment I can paste into my CLAUDE.md as a permanent reminder.

---

### Links & Resources

- [Original Video — Paste This Into Claude, Never Hit a Token Limit Again](https://www.youtube.com/watch?v=Y8vAQ1FgNbM)
- [Nate B Jones — AI News & Strategy Daily (YouTube Channel)](https://www.youtube.com/@NateBJones)
- Token Saver Skill — available on Nate's Substack (linked in video description)
- Ringer Multi-Agent Framework — available via video description / Substack
- [OpenBrain](https://www.youtube.com/@NateBJones) — Nate's knowledge retrieval tool referenced in the video (check channel for dedicated videos)
- [Anthropic Tool Definition Research](https://www.anthropic.com) — referenced re: ~55,000 token overhead from multi-tool setups
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)

---

### Tags
`#token-optimization` `#claude-code` `#prompt-engineering` `#context-management` `#ai-productivity`

---

### Category
Claude Code

---

*Extracted by [Co-Ord Executor](https://github.com/onekiller89/Co-Ord_Executor)*
