![banner](https://img.youtube.com/vi/5p-sq8v3OXw/maxresdefault.jpg)

# AI Agents: The Most Valuable Skill You Can Learn in 2026 (Full Course)

> **Source:** YouTube | **Extracted:** 2026-08-06 16:38 UTC | **Method:** youtube_transcript_api
> **URL:** https://www.youtube.com/watch?v=5p-sq8v3OXw

---

### Summary
This is a comprehensive full-course episode featuring Remy, a self-taught AI practitioner, explaining how to build and use AI agents for business productivity. The core thesis is that we've moved from "chat" (question → answer) to "agents" (goal → result), and anyone who masters the three pillars — **context, tools, and skills** — can become a 100x more productive operator. The episode covers the agent loop, folder structure, MCP connectors, markdown context files, and how to build reusable SOPs (skills) that compound over time.

---

### Key Insights

- **Chat vs. Agents**: Chat models give you answers you still have to act on. Agents take a goal, plan, execute, and hand you a finished result. The productivity delta is 5–10x in favour of agents.
- **The Agent Loop**: Every agent runs on three steps — Observe, Think, Act — cycling until the task is done. Understanding this loop demystifies all agent platforms (Claude Code, Codex, Manus, etc.).
- **The Four Tuning Levers**: Observe → Context + Skills; Think → LLM model choice; Act → Tools. You don't build a new agent loop — you *tune* these four levers inside existing harnesses.
- **Context = Markdown files you own**: The `CLAUDE.md` (or `agents.md`) auto-loads into every session as the "north star." Supplementary files (about.md, brand voice, ICP, offer catalog) live in a `/context` folder and are pointed to from `CLAUDE.md`. You own these assets — unlike ChatGPT's opaque memory.
- **MCP = the connector layer**: Model Context Protocol lets agents connect to third-party tools (Gmail, Slack, ClickUp, Stripe, etc.) without custom dev. Choosing vendors that *have* an MCP is now a purchasing criterion.
- **Skills = SOPs in markdown**: Skills are reusable, versioned process documents (like VA SOPs). They use progressive disclosure — only name/description loads by default; full content loads when the task requires it. Skills compound: orchestrator skills chain other skills in sequence.
- **Global vs. Project structure**: A holding-company OS folder contains global `CLAUDE.md` and skills; sub-project folders (marketing, health, newsletter) have their own `CLAUDE.md` that stacks on top. One unified OS folder beats many siloed agent folders.
- **Bottom-up AI adoption wins**: Training employees to build their own personal OS and automate their own tasks is more effective than top-down AI specialist deployments. Skills built by the people who do the work are far more nuanced and valuable.

---

### Actions

- [ ] Create an `OS` folder on your desktop as your agent's "holding company" workspace
- [ ] Open a fresh Claude/ChatGPT chat and ask it to interview you to build these markdown context files: `about.md`, `brand_voice.md`, `ideal_customer_profile.md`, `offer_catalog.md`, `business_info.md`
- [ ] Create a `CLAUDE.md` (or `agents.md`) in your OS folder that references the `/context` subfolder and sets your north-star instructions
- [ ] Create a `memory.md` file and add a rule to `CLAUDE.md` telling the agent to check and update it with learned preferences before every task
- [ ] Connect your core tools via MCP in Claude Desktop: start with ClickUp/Notion, Gmail, and Slack
- [ ] Sign up for Composio and connect all your tools there as a single unified MCP bridge, so your setup is portable across harnesses
- [ ] Install and connect Apify MCP for internet scraping and Firecrawl MCP for full-page website reading
- [ ] Run `/context` in Claude Code to check your context window usage and trim any bloated markdown files
- [ ] Complete one full workday from inside Claude Code — use `@folder` tagging to scope tasks to the right sub-project
- [ ] After completing any repeatable process with the agent, immediately say "save this as a skill" to let Claude build the SOP for you
- [ ] Build an email inbox triage skill and schedule it to run 3x per day
- [ ] Create sub-project folders for each business pillar (e.g., `open_residency/`, `marketing/`, `health/`) each with their own `CLAUDE.md`

---

### Implementation Prompts

#### Prompt 1: Bootstrap your CLAUDE.md north-star file
*Creates the foundational context file that auto-loads into every Claude Code session, giving the agent immediate awareness of who you are and how you work.*

> I want to build a `CLAUDE.md` file that will serve as my agent's north-star context file in Claude Code. It should auto-load at the start of every session. Please interview me with one question at a time to extract the following sections: (1) Who I am — background, role, what I'm building; (2) My business — what it does, the core offer, pricing; (3) Brand voice — tone, style, what to avoid; (4) Ideal customer profile — who I serve, their pain points, goals; (5) Offer catalog — all products/services and how they connect; (6) My values and working preferences — how I like tasks structured, what I hate; (7) A pointer to a `/context` subfolder where extended markdown files live. After the interview, format everything as clean markdown with H2 headings per section. End the file with: "Load relevant files from /context before starting any task. Assumptions are the enemy. If the answer isn't there, ask me." Save the output as `CLAUDE.md`.

---

#### Prompt 2: Build your full context folder from an interview
*Generates all your core business context files in one session — these become permanent assets you own and can port to any agent harness.*

> I want to build a `/context` folder of markdown files for my AI agent. Please interview me — one question at a time — to create the following separate `.md` files: `about.md` (my personal story, background, expertise), `business_info.md` (what the business does, mission, history), `brand_voice.md` (tone, writing style, examples of good/bad copy, vocabulary to use/avoid), `ideal_customer_profile.md` (demographics, psychographics, pain points, goals, objections), `offer_catalog.md` (all products/services, prices, upsells, downsells, how they connect). For each file: ask me 5–8 targeted questions, then generate the file in clean markdown with H2/H3 headings and bullet points. Keep each file lean and information-dense — no filler. Flag any answers that are vague or subjective so I can tighten them before saving.

---

#### Prompt 3: Set up a self-updating memory system
*Implements the memory.md preference-learning loop so the agent continuously improves and remembers your corrections across sessions.*

> I want to add a self-updating memory system to my Claude Code project. Please do the following: (1) Create a file called `memory.md` in my current project folder with this structure: a header "Memory & Learned Rules", a subheader "Lessons I've been taught — I check these before every task", and 3 starter rules I'll dictate. (2) Update my `CLAUDE.md` to include a section called "Memory System" with these instructions: "Your memory lives in `memory.md`. Before every task, read it. When I correct you or state a preference (e.g. 'always use dark mode', 'sign off emails with Cheers, [name]'), immediately append it as a new bullet under the Learned Rules section. Use the `@memory.md` tag for fast access. Never ask me the same preference twice." (3) Use the `@` symbol to reference `memory.md` directly in the CLAUDE.md so it's symlinked in. Confirm when done and show me the final structure of both files.

---

#### Prompt 4: Connect Composio as your universal MCP bridge
*Sets up Composio as the single MCP that contains all your tool connections, making your agent setup portable across Claude Code, Codex, and any other harness.*

> I want to set up Composio as a universal MCP bridge in Claude Code so all my tool connections are portable across different agent harnesses. Walk me through the complete setup process step by step: (1) How to create a Composio account and find my API key; (2) How to add Composio as a custom MCP connector in Claude Desktop (the exact URL format and where to paste it in Settings → Connectors → Add Custom); (3) How to connect my first 5 tools inside Composio — Gmail, Google Calendar, Slack, Notion, and one project management tool (ClickUp or Linear); (4) How to verify the connection works by running a simple test task (e.g., "list my 5 most recent emails"); (5) How to also connect Apify and Firecrawl through Composio so I have web scraping and page reading available everywhere. Give me the exact steps, URLs, and any gotchas to watch out for. If you hit an error, I'll screenshot it and paste it back.

---

#### Prompt 5: Build a skill from a process you just completed
*Converts any completed agent workflow into a reusable, versioned SOP that triggers automatically in future sessions — the core compounding mechanism of the system.*

> I just completed a multi-step process with you (I'll describe it below). I want you to package this into a reusable skill using the Claude skill format. Here's what we just did: [PASTE YOUR PROCESS DESCRIPTION HERE]. Please: (1) Create a folder called `[skill-name]` inside `.claude/skills/`; (2) Inside it, create `skill.md` with this exact structure — Name: [skill name], Description: [one sentence on what it does + trigger phrases like "use when user says X"], then a horizontal rule, then Contents: a numbered step-by-step SOP that another agent could follow without any additional context, referencing specific tools (Apify, Firecrawl, etc.) where needed, with expected outputs at each step; (3) Include an "Output Format" section specifying exactly how to present the final result; (4) Save any reference examples or templates into the same folder. After saving, confirm the skill is accessible via `/[skill-name]` slash command and show me the full `skill.md` content.

---

#### Prompt 6: Build a competitive ads analysis skill with Firecrawl + Apify
*Replicates the "ads analyst" skill shown in the video — scrapes competitor ads, downloads creatives, and generates a strategic analysis report automatically.*

> Build me a complete "ads-analyst" skill for Claude Code that does the following when I provide a Meta Ads Library URL: Step 1 — Use the Firecrawl MCP to scrape all active ads from the URL, extracting: ad creative type (video/image), headline, body copy, CTA, estimated run duration, and link to landing page. Step 2 — Use Apify to download all ad creative assets (images/videos) into a local folder named `ad-research/[brand-name]/assets/`. Step 3 — Use Firecrawl to scrape each unique landing page the ads point to, capturing: headline, subheadline, CTA placement, offer structure, and social proof elements. Step 4 — Analyse all collected data and produce: (a) a `master-report.md` with top patterns, longest-running ads, creative format breakdown, and 5 "things to steal or beat"; (b) an `ads-report.html` visual summary with embedded thumbnails and sortable table. Step 5 — Save everything to `active/ad-research/[brand-name]/`. Format this as a proper `skill.md` file saved to `.claude/skills/ads-analyst/skill.md`, ready to trigger with `/ads-analyst`.

---

#### Prompt 7: Create an orchestrator skill that chains multiple skills in sequence
*Builds a master workflow skill (like the YouTube Publish Workflow shown in the video) that calls other skills in sequence — enabling fully automated multi-step pipelines.*

> I want to build an orchestrator skill in Claude Code that chains multiple sub-skills in a specific sequence. Here is the workflow I want to automate: [DESCRIBE YOUR WORKFLOW — e.g., "Weekly newsletter creation: 1. Pull top-performing subject lines from Beehive, 2. Draft newsletter body in my brand voice using the latest content from Notion, 3. Generate 3 subject line options, 4. Create a header image using Heygen/Higgsfield, 5. Stage the full email in Beehive as a draft"]. Please: (1) Create `.claude/skills/[workflow-name]/skill.md` as an orchestrator skill; (2) In the contents, explicitly state "This is an orchestrator skill" and list each sub-skill it calls in order, with the input each sub-skill needs from the previous step's output; (3) For any sub-skills that don't exist yet, create a placeholder `skill.md` with a TODO marker; (4) Add error handling instructions: "If any step fails, stop and report which step failed and why before proceeding"; (5) Add a final step: "Confirm all outputs are saved and present a summary checklist of what was completed." Show me the complete file structure when done.

---

#### Prompt 8: Design your OS folder structure for a multi-pillar business
*Scaffolds your entire personal AI operating system folder structure with global and project-level CLAUDE.md files, context, memory, and skills — ready to start working from day one.*

> I want to set up my complete AI Operating System (OS) folder structure on my computer, following the global vs. project-level architecture. My business pillars are: [LIST YOUR PILLARS — e.g., "main business, content/newsletter, personal health, client work"]. Please: (1) Design the full folder tree showing OS/ as the root, with subfolders for each pillar, an `active/` folder for one-off projects, and hidden `.claude/` folders for settings; (2) Create the global `CLAUDE.md` at the OS root level with a section explaining the folder structure and how to use `@folder` tagging to scope tasks; (3) Create a starter `CLAUDE.md` for each pillar folder with a one-paragraph description of what that workspace is for; (4) Create the global `.claude/skills/` directory with a placeholder `README.md` explaining the skills system; (5) Create a global `context/` folder with empty placeholder files for: `about.md`, `brand_voice.md`, `ideal_customer_profile.md`, `offer_catalog.md`, `memory.md`; (6) Output the complete folder tree as ASCII art, then create all the files. Use `mkdir -p` and file creation commands I can run in terminal, or create them directly if you have file system access.

---

### Links & Resources

- [Video: AI Agents Full Course — Open Residency](https://www.youtube.com/watch?v=5p-sq8v3OXw)
- [Apify — Web Scraping Marketplace](https://apify.com)
- [Firecrawl — Full-page Web Scraping for AI](https://firecrawl.dev)
- [Composio — Universal MCP Bridge for AI Agents](https://composio.dev)
- [Higgsfield AI — Image & Video Generation MCP](https://higgsfield.ai)
- [Beehive — Newsletter Platform with MCP](https://beehive.com)
- [Claude Code — Anthropic's Agent Harness](https://claude.ai/code)
- [WhisperFlow — Voice-to-Text for Mac](https://whisperflow.app)
- [Playwright — Browser Automation MCP](https://playwright.dev)
- [Chrome DevTools MCP — Browser Control for Agents](https://developer.chrome.com/docs/devtools)
- [OpenClaw — Advanced Agent Framework](https://openclaw.ai)
- [Hermes — Autonomous Agent Framework](https://hermes-agent.ai)
- [Obsidian — Markdown-based Second Brain](https://obsidian.md)
- [Composio — Connect apps reference (mentioned for Gmail multi-account)](https://composio.dev)
- [Ask Cat GPT — AI Content Creator (mentioned as inspiration)](https://twitter.com/AskCatGPT)
- [My First Million Podcast](https://www.mfmpod.com)
- [The Alchemist — Paulo Coelho](https://www.goodreads.com/book/show/865.The_Alchemist)

---

### Tags
`#ai-agents` `#claude-code` `#productivity` `#automation` `#mcp` `#personal-os`

---

### Category
AI Agents

---

*Extracted by [Co-Ord Executor](https://github.com/onekiller89/Co-Ord_Executor)*
