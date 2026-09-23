![banner](https://img.youtube.com/vi/BNjzXcEXmg4/maxresdefault.jpg)

# This NEW Claude Prompting Technique is blowing people's minds (gauntlet-loop)

> **Source:** YouTube | **Extracted:** 2026-08-10 23:49 UTC | **Method:** youtube_transcript_api
> **URL:** https://www.youtube.com/watch?v=BNjzXcEXmg4

---

### Summary
The "gauntlet loop" is a three-part prompting technique for Claude that orchestrates a fleet of sub-agents to build complex outputs (games, 3D environments, websites) with built-in critic agents that loop until quality meets a defined bar. Originating from Matt Schumer's viral demo of Claude Opus 5 one-shotting a full FPS game, the pattern is simple but powerful: define a task, specify a sub-agent fan-out build method, and set a quality bar that prevents early stopping. The technique is most effective when applied to a solid MVP foundation rather than used as a starting prompt from scratch.

---

### Key Insights

- **Three-part structure is the core pattern**: Task → Build Method (fan out sub-agents, each with a critic partner) → Bar to Hit (quality standard that must be met before stopping). The actual wording matters less than this structure.
- **Critic/evaluator agents consistently improve output quality** — Anthropic's own "Building Effective Agents" research confirms that having a separate model evaluate output is better than self-evaluation, because models tend to convince themselves their output is already good enough.
- **The gauntlet loop is not new — it's an extreme application of existing loops**: Agent loops and critic patterns have existed since at least late 2024; the gauntlet loop scales this to parallel sub-agent fleets, each with their own evaluator.
- **Don't start from zero with this technique**: Running it on an undefined brief will produce polished but off-brand/off-brief results. Use it as a "warp drive" to sharpen an existing MVP or design system.
- **Token and time costs are significant**: Runs of 1–2+ hours are normal. Set expectations accordingly and only trigger the loop once direction is locked in.
- **No extra tooling required**: Claude Code handles the orchestration natively — a well-structured prompt is all you need to trigger multi-agent fan-out.
- **Broad applicability beyond games**: Architecture walkthroughs, real estate visualisations, product websites, and any domain requiring high-fidelity iterative output can benefit from this pattern.

---

### Actions

- [ ] Read Matt Schumer's original article on the gauntlet loop to understand the exact prompt wording and intent
- [ ] Copy the three-part gauntlet loop prompt structure (Task / Build Method / Bar to Hit) into a personal prompt library or CLAUDE.md
- [ ] Download or create the `/gauntlet-loop` slash skill mentioned in the video (linked in YouTube description)
- [ ] Run a small test gauntlet loop prompt in Claude Code on a contained task (e.g., a single-page UI component) before attempting a large build
- [ ] Read Anthropic's "Building Effective Agents" article to understand the theoretical foundation of evaluator/critic agent patterns
- [ ] Before running a gauntlet loop on a real project, build an MVP or design system first to give the loop a strong foundation and direction
- [ ] Experiment with adjusting the "bar to hit" wording — more extreme standards (e.g., "utterly wowed compared to [reference product]") drive more iteration cycles and higher quality
- [ ] Track token usage and time on your first gauntlet loop run to calibrate expectations for future use

---

### Implementation Prompts

#### Prompt 1: Generate a Gauntlet Loop Prompt for Any Task
*Bootstraps the gauntlet loop pattern for any goal so you can immediately use it without writing the prompt from scratch.*

> You are an expert at writing Claude agentic prompts using the "gauntlet loop" technique. I will give you a task and you will generate a complete, ready-to-use gauntlet loop prompt following this exact three-part structure:
>
> 1. **Task**: A clear, specific description of what needs to be built or created.
> 2. **Build Method**: Instruct the main agent to break the goal into the smallest logical pieces, fan out a dedicated sub-agent for each piece, and assign a separate "blind critic" sub-agent to each worker that visually/functionally evaluates the output against the target bar before passing it forward.
> 3. **Bar to Hit**: A high, specific quality standard the critic agents must confirm before the loop terminates — reference a real-world benchmark or named product for comparison.
>
> My task: **[INSERT YOUR TASK HERE — e.g., "Build a fully interactive product landing page for a coffee subscription brand called Roast & Co, dark aesthetic, with scroll animations and a pricing section"]**
>
> Output only the final gauntlet loop prompt, ready to paste into Claude Code or Claude desktop. Do not include explanations — just the prompt itself.

---

#### Prompt 2: Set Up a /gauntlet-loop Slash Command in Claude Code
*Creates a reusable Claude Code slash command so you can trigger gauntlet loop prompt generation from any project with a single command.*

> Create a Claude Code slash command file called `gauntlet-loop.md` to be placed in the `.claude/commands/` directory of my project. When invoked with `/gauntlet-loop [task description]`, it should:
>
> 1. Accept the user's task description as input
> 2. Automatically generate a complete gauntlet loop prompt using this three-part structure:
>    - **Task**: Restate the goal clearly and specifically
>    - **Build Method**: Instruct Claude to decompose the goal into atomic sub-tasks, spawn a dedicated sub-agent per task, and pair each with a blind critic sub-agent that evaluates quality before reporting back
>    - **Bar to Hit**: Set an extremely high quality bar referencing a named world-class benchmark relevant to the task type
> 3. Output the final prompt ready to run immediately
>
> Format the `.md` file correctly for Claude Code's slash command system, with a clear description, input variable handling, and the prompt template. Show me the complete file content.

---

#### Prompt 3: Add Gauntlet Loop Pattern to CLAUDE.md
*Embeds the gauntlet loop pattern permanently into your project's Claude instructions so it's available as a building pattern across all sessions.*

> Update my project's `CLAUDE.md` file to include a documented section on the Gauntlet Loop prompting pattern. The section should include:
>
> - **What it is**: A three-part agentic prompting structure (Task / Build Method / Bar to Hit) that orchestrates a fleet of worker sub-agents each paired with a blind critic sub-agent that loops until a defined quality bar is met
> - **When to use it**: After an MVP or design foundation is established — not as a first prompt from scratch. Best for polish/quality amplification passes.
> - **When NOT to use it**: On undefined briefs, early ideation, or when token budget is limited (expect 1–2+ hour runs)
> - **Template**: A fill-in-the-blank three-part prompt template
> - **Example**: One short concrete example showing all three parts filled in
>
> Append this section cleanly to my existing CLAUDE.md without modifying anything else. Show me the exact markdown to add.

---

#### Prompt 4: Build a Critic-Loop Agent Pattern from Scratch
*Implements the core worker + critic loop pattern as a standalone Claude Code workflow you can adapt for any domain.*

> Using Claude Code, create a minimal but complete implementation of the worker-critic loop pattern. Structure it as follows:
>
> **Setup**: A main orchestrator prompt that:
> 1. Receives a task definition and quality bar
> 2. Decomposes the task into N sub-tasks
> 3. For each sub-task, runs a "worker" prompt to generate output
> 4. For each worker output, runs a "critic" prompt that scores it against the quality bar (pass/fail + specific feedback)
> 5. If critic returns fail, feeds the feedback back to the worker and retries (max 5 iterations per sub-task)
> 6. Only when all critics pass does it assemble the final output
>
> Implement this using Claude Code's native bash/file tooling — no external libraries needed. Create:
> - `orchestrator.md` — the main prompt file
> - `worker_template.md` — the worker sub-agent prompt template  
> - `critic_template.md` — the critic sub-agent prompt template
> - `run.sh` — a shell script to kick off the loop with a task argument
>
> Show complete file contents for all four files.

---

#### Prompt 5: Apply Gauntlet Loop to Polish an Existing MVP
*The recommended workflow — use gauntlet loop as a quality amplifier on something already built, not from scratch.*

> I have an existing [web app / UI component / document / codebase — SPECIFY] that needs a quality polish pass. I want to apply the gauntlet loop prompting technique to improve it significantly without changing its core direction or brand.
>
> Here is my existing MVP: **[PASTE CODE, DESIGN DESCRIPTION, OR FILE PATH]**
>
> Here is my quality bar reference: **[e.g., "should look and feel as polished as Stripe's marketing site" or "should match the attached brand guidelines"]**
>
> Generate a complete gauntlet loop prompt I can paste into Claude Code that:
> 1. Takes my existing MVP as the starting point (not blank slate)
> 2. Fans out sub-agents to improve specific quality dimensions (visual polish, accessibility, copy, animations, performance — adapt as relevant)
> 3. Has each sub-agent paired with a critic that compares the improved output against my quality bar reference
> 4. Loops until all critics confirm the bar is met
>
> Output only the ready-to-run prompt.

---

#### Prompt 6: Diagnose Why a Gauntlet Loop Run Went Off-Brief
*Helps you debug and fix gauntlet loop outputs that look polished but missed the actual goal — a common failure mode.*

> I ran a gauntlet loop prompt in Claude and the output looks visually impressive but is off-brief — it doesn't match my brand/requirements. Help me diagnose what went wrong and fix it.
>
> Here is the gauntlet loop prompt I used: **[PASTE YOUR PROMPT]**
>
> Here is what I got back: **[DESCRIBE OR PASTE OUTPUT]**
>
> Here is what I actually wanted: **[DESCRIBE INTENDED RESULT, BRAND GUIDELINES, OR ATTACH REFERENCE]**
>
> Please:
> 1. Identify which part of the three-part gauntlet loop structure (Task / Build Method / Bar to Hit) was too vague or misdirected
> 2. Suggest specific rewrites for each problematic section
> 3. Recommend what MVP foundation or reference material I should provide upfront before re-running
> 4. Output a corrected, complete gauntlet loop prompt ready to run again

---

### Links & Resources

- [Original video — Jay E | RoboNuggets](https://www.youtube.com/watch?v=BNjzXcEXmg4)
- [Matt Schumer on X (original demo, 4.8M views)](https://x.com/mattshumer_) *(search for gauntlet loop post)*
- [Matt Schumer's "Something Big is Happening" article](https://x.com/mattshumer_) *(87M views — search on Medium/Substack)*
- [Anthropic — Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Andrej Karpathy's post on LLM capabilities](https://x.com/karpathy) *(referenced in video — search his timeline)*
- [RoboNuggets Community / Claude Masterclass](https://www.youtube.com/@RoboNuggets) *(pin comment on video for link)*
- `/gauntlet-loop` slash skill — available in the video's YouTube description

---

### Tags
`#prompting` `#claude` `#ai-agents` `#multi-agent` `#claude-code`

### Category
Claude Code

---

*Extracted by [Co-Ord Executor](https://github.com/onekiller89/Co-Ord_Executor)*
