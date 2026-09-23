![banner](https://img.youtube.com/vi/5p-sq8v3OXw/maxresdefault.jpg)

# AI Agents: The Most Valuable Skill You Can Learn in 2026 (Full Course)

> **Source:** YouTube | **Extracted:** 2026-09-23 02:55 UTC | **Method:** youtube_transcript_api
> **URL:** https://www.youtube.com/watch?v=5p-sq8v3OXw

---

### Summary
This is a comprehensive "full course" episode featuring Remy, a self-taught non-technical founder who runs an AI agent team for a major ecom brand. He breaks down the shift from AI chat (question → answer) to AI agents (goal → result), explaining the observe-think-act loop that powers agents, and walks through his exact system for tuning agents using three pillars: context, tools, and skills. The episode includes live screen-share demos building real agent setups in Claude Code, covering folder structure, markdown files, MCP integrations, and skill creation.

---

### Key Insights

- **Chat vs. Agents is the productivity divide**: Chat gives answers, agents deliver finished work. People using agents are 5–10x more productive; the gap is widening fast between those who've made the shift and those who haven't.
- **The observe-think-act loop is all an agent is**: Every agent just cycles through "look at situation → decide next step → do it" until the goal is met. Understanding this demystifies 90% of the hype around "AI agents."
- **Agents are tuned, not built**: No one is "building agents" — they're tuning the four levers: context (observe), skills (observe), LLM model (think), and tools (act). The harness (Claude Code, Codex, Manus) is just the car; you need to know how to drive.
- **Context = markdown files you own**: Your CLAUDE.md is the northstar file loaded into every session automatically. Supporting context files (about.md, ICP, brand voice, offer catalog) live in a context folder. This is YOUR data, not a black box like ChatGPT memory.
- **Skills = SOPs for AI**: Skills are markdown files with a name, description, and step-by-step process. The agent reads the "spine of the book" (name + description) for all skills at session start, then pulls the full content only when needed (progressive disclosure). Build them process-first by doing a task once, then telling Claude to save it as a skill.
- **MCP is how your agent gets tools**: Model Context Protocol is just a translator between Claude and third-party apps (Gmail, Notion, Slack, etc.). Composio acts as a single MCP hub aggregating hundreds of tools — critical for portability across agent harnesses.
- **The OS folder is your holding company**: One OS folder contains sub-folders for each business/life pillar. A global CLAUDE.md applies everywhere; project-level CLAUDE.mds stack on top. This replaces having separate "agents" per function.
- **Skills compound as business assets**: V1 of a skill is never perfect — most good skills are on V5–V10. Skills built by employees are IP assets, and the question of who *owns* those skills when someone leaves a company is a live, unresolved problem in the space.

---

### Actions

- [ ] Create a root folder called `OS` on your desktop — this is your AI operating system holding company
- [ ] Open Claude (chat mode) and run: *"Interview me to build the following markdown context files: about_me.md, ideal_customer_profile.md, brand_voice.md, offer_catalog.md"* — answer verbally using Whisper Flow if available
- [ ] Create a `CLAUDE.md` (or `agents.md`) in your OS folder pointing to your context subfolder, and paste in a summary of who you are and what you do
- [ ] Create a `memory.md` file and instruct Claude to: *"Check this file before every task and write new learned rules here when I correct you"*
- [ ] Connect your top 3 tools as MCP connectors in Claude Desktop (Settings → Connectors → Browse)
- [ ] Set up Composio as a single MCP hub so all your tool connections are portable across harnesses (Claude Code, Codex, etc.)
- [ ] Install and configure: Apify (web scraping), Firecrawl (page scraping/reading), Chrome DevTools or Playwright (browser control), and Hailuo/Higgsfield (image/video generation) as MCPs
- [ ] Complete one full workday entirely from inside Claude Code — notice where the friction points are and build your first skill from that
- [ ] After any repeatable task, tell Claude: *"Save this process as a skill in my .claude/skills folder"*
- [ ] Run `/context` in Claude Code periodically to check how much of your context window your markdown files are consuming — trim if over ~10–15% before any work begins
- [ ] Set up an email inbox triage skill and schedule it to run 3x per day
- [ ] Create project-level `CLAUDE.md` files for each major pillar folder (e.g., `OS/open_residency/CLAUDE.md`) with context specific to that domain

---

### Implementation Prompts

#### Prompt 1: Build your complete context file suite via interview
*Sets up the foundational markdown files that give your agent persistent memory of who you are — the most important first step in the entire system.*

> You are helping me build my AI agent's context files. I want to create the following markdown files: `about_me.md`, `ideal_customer_profile.md`, `brand_voice.md`, `offer_catalog.md`, and `values.md`. 
>
> Please interview me one file at a time to extract the information needed. Start with `about_me.md`. Ask me specific, targeted questions to pull out: my background and story, what I do professionally, my current projects and roles, my content/media presence if any, my goals for the next 12 months, and any relevant personal context. 
>
> After I answer, synthesize my responses into a clean, well-structured markdown file with clear headings (H2/H3), bullet points, and bold key terms. Keep it factual and objective — avoid vague or subjective language. Once I approve it, move to the next file. Do NOT use placeholder text. Everything must be real, based on my answers.

---

#### Prompt 2: Create your master CLAUDE.md northstar file
*The CLAUDE.md file is automatically loaded into every Claude Code session — it's the single most important file in your entire OS folder, acting as the agent's onboarding doc.*

> Create a `CLAUDE.md` file for my AI agent operating system. This file will be automatically loaded at the start of every Claude Code session. Structure it as follows:
>
> 1. **Who I am** — a 3–5 sentence summary of me, my role, and my business context
> 2. **My context folder** — instruct the agent: "Before starting any task, read all files in the `/context` folder. Load the relevant files. Assumptions are the enemy — if information isn't there, ask me."
> 3. **My memory system** — instruct the agent: "Your memory lives in `/context/memory.md`. Check it before every task. When I correct you or state a preference, add a new rule to that file immediately."
> 4. **My skills** — instruct the agent: "Your skills live in `.claude/skills/`. Read the name and description of each skill at session start. When a task matches a skill, load and follow it exactly."
> 5. **How I like to work** — [I will fill this in, but include a placeholder section for: communication style, output format preferences, tools I prefer]
> 6. **Core principle** — include: "The marginal cost of completeness is near zero. Don't give me 80% — finish the job."
>
> Format the entire file in clean markdown. Keep it under 400 words total so it doesn't bloat my context window.

---

#### Prompt 3: Build a skill from a process you just completed
*Use this immediately after completing any multi-step task you'll want to repeat — this is the "process-first" skill creation method that turns one-time work into permanent reusable SOPs.*

> We just completed a multi-step task together. Now I want you to package that entire process into a reusable skill file so I never have to explain it again.
>
> Please do the following:
> 1. Review our full conversation history for this session and identify every step we took to complete the task
> 2. Create a new folder inside `.claude/skills/` named after the task (use snake_case, e.g., `email_inbox_triage/`)
> 3. Inside that folder, create a `skill.md` file with this exact structure:
>    - **Name**: [short skill name]
>    - **Description**: [1–2 sentences describing what this skill does and when to use it — this is the "spine of the book" I'll see in slash commands]
>    - ---
>    - **Contents**: Step-by-step instructions formatted like an SOP for a VA. Include: exact tools to use (Apify, Firecrawl, etc.), what to look for, how to handle edge cases we encountered, the exact output format I approved, and any corrections I made during the process.
> 4. Also save any output templates or reference examples as separate files in the same skill folder
>
> The skill should be detailed enough that a future version of you — with no memory of this session — could execute it perfectly on the first try.

---

#### Prompt 4: Set up Composio as your universal MCP hub
*Composio aggregates all your tool connections into a single MCP endpoint, making your entire toolset portable across Claude Code, Codex, Manus, or any other agent harness.*

> I want to set up Composio as my universal MCP hub so all my tool connections are portable across different AI agent harnesses (Claude Code, Codex, Manus, etc.).
>
> Please walk me through this step by step:
> 1. How to create a Composio account and find my API key / MCP server URL
> 2. How to add Composio as a custom connector in Claude Desktop (Settings → Connectors → Add Custom)
> 3. How to connect my top priority tools inside Composio — I want to connect: Gmail (all accounts), Google Calendar, Slack, Notion, and one project management tool (ClickUp or Linear)
> 4. How to verify the connection is working by running a simple test task in Claude Code
> 5. How to also connect Apify and Firecrawl through Composio so they're available in the same hub
>
> For each step, assume I am non-technical and give me exact clicks, URLs, and what to copy-paste. If I hit an error, tell me to screenshot it and paste it back to you.

---

#### Prompt 5: Build a competitive ad intelligence skill using Firecrawl + Apify
*Automates the process of scraping competitor ads from Meta Ad Library, analyzing them, and generating a structured report — replicating the live demo from the video.*

> Build me a complete ad intelligence skill that I can run whenever I want a competitor analysis. Save it to `.claude/skills/ad_intelligence/skill.md`.
>
> The skill should do the following when triggered with a Meta Ad Library URL:
> 1. Use **Firecrawl** to scrape the Ad Library page and extract all active ads (creative assets, copy, headlines, CTAs, run duration)
> 2. Use **Apify** (Instagram/Facebook scraper actor) to supplement with any missing ad data
> 3. Download all video and image creative assets into a local folder named `ad_research/[competitor_name]/assets/`
> 4. Scrape all destination landing pages linked from the ads using Firecrawl — capture layout, headline, CTA placement, offer structure
> 5. Generate three output files:
>    - `master_report.md` — ranked ad breakdown with: hook type, format, offer, estimated run duration, landing page summary
>    - `strategic_insights.html` — visual HTML report with: top patterns, things to steal, things to beat, creative angles not yet tested
>    - `raw_data.csv` — all ads in tabular format for sorting/filtering
>
> Structure the skill.md with name, description separator, then numbered steps referencing specific tools. Include error handling instructions (e.g., if Firecrawl is blocked, fall back to Apify web scraper actor).

---

#### Prompt 6: Create an orchestrator skill that chains multiple skills in sequence
*Orchestrator skills let you chain multiple individual skills into a single workflow — the equivalent of a multi-step agency process running on autopilot.*

> I want to create an orchestrator skill that chains multiple existing skills together into one end-to-end workflow. 
>
> Here's my use case: I want a **Content Publishing Workflow** that runs every time I'm ready to publish a new piece of content. Build the skill at `.claude/skills/content_publish_workflow/skill.md`.
>
> The orchestrator should call these skills in sequence:
> 1. `youtube_titles` skill — generate 10 title options for the video topic
> 2. `hook_writer` skill — write 3 hook variations for the script opening
> 3. `subject_line_writer` skill — write 10 newsletter subject lines tied to this content
> 4. `social_captions` skill — write platform-specific captions for Instagram, LinkedIn, and X
> 5. Then compile all outputs into a single `content_brief_[date].md` file saved to my `/content/active/` folder
>
> In the skill.md, clearly label it as an "ORCHESTRATOR SKILL" at the top. For each step, specify: which skill to call, what input to pass from the previous step's output, and what the expected output artifact is. Add a final step that asks me: "All assets are ready. Would you like me to schedule distribution?" before taking any publishing actions.
>
> If any of the referenced sub-skills don't exist yet, flag them with [SKILL NOT FOUND — CREATE FIRST] so I know what to build.

---

#### Prompt 7: Set up a memory system with automatic self-improvement
*Implements the memory.md system shown in the video so your agent learns your preferences over time and never repeats the same mistake twice.*

> I want to implement a persistent memory and self-improvement system for my Claude Code agent. Do the following:
>
> 1. Create `/context/memory.md` with this structure:
>    ```
>    # Agent Memory — Learned Rules & Preferences
>    ## How to use this file
>    Check this file before starting ANY task. When [my name] corrects you or states a preference, immediately append a new rule under the relevant section.
>    
>    ## Communication & Output Style
>    ## Writing & Copy Preferences  
>    ## Technical Preferences
>    ## Tool Usage Rules
>    ## Things I Never Want
>    ## Workflow Preferences
>    ```
>
> 2. Update my `CLAUDE.md` to include these exact instructions:
>    *"MEMORY SYSTEM: Before every task, read @/context/memory.md. When I correct you mid-task or express a preference, pause and add it as a new rule to the relevant section of memory.md before continuing. Use the @ symbol to reference the file so it loads instantly without using an extra loop."*
>
> 3. Test the system by doing this: I'll tell you one preference right now — [INSERT YOUR PREFERENCE, e.g., "Never use bullet points when writing email copy — always write in flowing paragraphs"]. Add that as the first rule to memory.md, confirm you've written it, then show me the updated file.
>
> 4. Also add a monthly maintenance instruction to CLAUDE.md: *"If memory.md exceeds 50 rules, flag it for a spring clean audit to remove contradictions."*

---

### Links & Resources

- [Video Source — AI Agents Full Course (Open Residency)](https://www.youtube.com/watch?v=5p-sq8v3OXw)
- [Claude Code](https://claude.ai/code) — Primary agent harness used throughout
- [Anthropic Claude](https://claude.ai) — Underlying model and desktop app
- [Composio](https://composio.dev) — Universal MCP aggregator hub
- [Apify](https://apify.com) — Web scraping marketplace (thousands of scrapers)
- [Firecrawl](https://firecrawl.dev) — Full page scraping and reading for agents
- [Higgsfield AI](https://higgsfield.ai) — Image and video generation MCP (aggregates multiple image models)
- [Beehive](https://beehive.io) — Newsletter platform with native MCP support
- [Whisper Flow](https://whisperflow.app) — Voice-to-text tool for hands-free prompting
- [OpenClaw](https://openclaw.ai) — Advanced autonomous agent framework
- [Hermes](https://herm.es) — Agent framework for running on dedicated hardware (Mac Mini)
- [Playwright MCP](https://github.com/microsoft/playwright-mcp) — Browser automation for agents
- [Chrome DevTools MCP](https://github.com/ModelContextProtocol/servers) — Google Chrome browser control
- [Perplexity Computer](https://perplexity.ai) — Alternative agent harness
- [Manus AI](https://manus.im) — Alternative agent harness
- [OpenAI Codex](https://openai.com/codex) — Alternative agent harness
- [Obsidian](https://obsidian.md

### Tags
#ai-agents #claude-code #mcp #prompt-engineering #workflow-automation #non-technical-founders

### Category
AI Agent Systems & Automation

---

*Extracted by [MegaMind](https://github.com/onekiller89/MegaMind)*
