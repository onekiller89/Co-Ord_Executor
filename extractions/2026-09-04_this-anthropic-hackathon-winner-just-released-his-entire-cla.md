![banner](https://img.youtube.com/vi/g3Mh8Hws-jo/maxresdefault.jpg)

# This Anthropic Hackathon Winner Just Released His Entire Claude Code Setup for Free - ECC

> **Source:** YouTube | **Extracted:** 2026-09-04 12:28 UTC | **Method:** youtube_transcript_api
> **URL:** https://www.youtube.com/watch?v=g3Mh8Hws-jo

---

### Summary
Afan Mustafa, winner of the Anthropic x Forum Ventures Hackathon in New York, has open-sourced his entire Claude Code setup called "Everything Claude Code" (ECC). Built while creating a full AI product (Zenith Chat) in just 8 hours, ECC provides a plug-and-play development environment featuring 64 specialised AI agents, 262 skills, 84 slash commands, hooks, and pre-configured MCP integrations for popular platforms. It also includes a continuous learning system that adapts to your personal coding patterns over time.

### Key Insights
- **64 specialised agents out of the box** — each scoped to a specific task (feature planning, architecture, security review, build error fixing, Go code review, Playwright E2E testing), eliminating the need to prompt-engineer general-purpose Claude for every task.
- **Continuous learning via Git history** — ECC reads your repository history, identifies your coding patterns, and converts them into reusable skills automatically — the system compounds in usefulness the longer you use it.
- **262 skills + 84 slash commands** — a large library of pre-built capabilities that can be invoked immediately, covering a wide range of development workflows without custom setup.
- **Pre-configured MCP integrations** — GitHub, Supabase, Vercel, and Railway are wired up from day one, removing the usual friction of connecting Claude Code to your toolchain.
- **Trigger-based hooks** — automation that fires on specific events, enabling autonomous workflows beyond simple chat interactions.
- **Cross-platform, single-plugin install** — works on Windows, Mac, and Linux with auto-detection of your package manager, making adoption nearly frictionless.
- **Battle-tested, not theoretical** — this is the exact configuration that produced a working AI product in 8 hours at a competitive hackathon, giving it credibility beyond typical starter templates.

### Actions
- [ ] Search GitHub for "Everything Claude Code" by Afan Mustafa and star/fork the repository
- [ ] Read the repo's README to understand installation requirements and prerequisites
- [ ] Install ECC as a Claude Code plugin following the single-command install instructions
- [ ] Browse the 64 agents directory and identify which agents are most relevant to your current projects
- [ ] Explore the 84 slash commands and create a personal cheat sheet of the ones you'll use most
- [ ] Connect the pre-built MCP configurations for the platforms you use (GitHub, Supabase, Vercel, Railway)
- [ ] Run ECC on an existing project to let it analyse your Git history and begin generating personalised skills
- [ ] Review the trigger-based hooks and enable those that match your development workflow (e.g., on commit, on build failure)

### Implementation Prompts

#### Prompt 1: Discover and audit the ECC repository structure
*Get a clear map of everything ECC provides before installing, so you can prioritise what to use first.*
> I'm evaluating the "Everything Claude Code" (ECC) repository by Afan Mustafa (search GitHub for "everything-claude-code"). Please help me audit its structure. Explore the repository and produce: (1) a directory tree of the top 2 levels, (2) a categorised list of all 64 agents with a one-line description of each, (3) a grouped summary of the 84 slash commands, (4) an explanation of how the continuous learning / skills system works based on the source code or documentation, and (5) a list of all MCP integrations included and how they are configured. Output this as a structured markdown document I can use as a reference guide.

#### Prompt 2: Install ECC and verify the setup
*Ensure ECC is correctly installed as a Claude Code plugin with all dependencies resolved.*
> I want to install the "Everything Claude Code" (ECC) plugin for Claude Code on my [Mac/Windows/Linux] machine. I use [npm/yarn/pnpm/bun] as my package manager. Walk me through the exact installation steps from the ECC GitHub repository. After installation, provide a verification checklist: commands I can run to confirm (1) the plugin is loaded by Claude Code, (2) all 84 slash commands are available, (3) the MCP servers for GitHub, Supabase, Vercel, and Railway are reachable, and (4) the agent system is functional. Flag any common setup errors and how to fix them.

#### Prompt 3: Configure MCP integrations for my stack
*Wire up the pre-built MCP servers so Claude Code can interact directly with your existing services.*
> I'm setting up the MCP integrations included in the Everything Claude Code (ECC) repository. I use the following services: GitHub (for version control), Supabase (for database/auth), and Vercel (for deployments). Using the ECC configuration files as a base, help me: (1) locate the correct config files for each MCP server, (2) populate them with my credentials and project-specific values (show me exactly which environment variables or config keys to set), (3) test each connection from within Claude Code using a slash command or agent call, and (4) troubleshoot any authentication or network errors. Provide the final `.mcp.json` or equivalent config I should have in place.

#### Prompt 4: Activate the continuous learning system on an existing project
*Let ECC analyse your Git history and generate personalised skills from your real coding patterns.*
> I want to use the continuous learning feature in Everything Claude Code (ECC) on my existing project at [/path/to/project]. This project uses [language/framework, e.g., TypeScript + Next.js]. Using the ECC skills/learning system: (1) trigger the Git history analysis on my repo, (2) show me what coding patterns it detects (naming conventions, file structure preferences, error handling style, etc.), (3) display the reusable skills it generates from those patterns, (4) explain how to review and approve generated skills before they are saved, and (5) show me how to manually create a custom skill if the auto-generated ones miss something important. Output the final skills as YAML or whatever format ECC uses.

#### Prompt 5: Build a custom specialised agent using the ECC framework
*Extend ECC with a new agent tailored to a gap in your workflow not covered by the 64 defaults.*
> Using the Everything Claude Code (ECC) agent framework as a template, help me create a new specialised agent for [describe your use case, e.g., "reviewing database migration files for safety and reversibility"]. Reference the structure of an existing ECC agent (e.g., the security review agent) as a model. The new agent should include: (1) a clear system prompt scoped to this single responsibility, (2) a defined input format (what context/files it receives), (3) a structured output format (what it returns), (4) a corresponding slash command to invoke it (e.g., `/review-migration`), and (5) an optional trigger hook (e.g., fires when a file matching `migrations/*.sql` is staged). Produce the complete agent definition file ready to drop into the ECC agents directory.

#### Prompt 6: Create a personal ECC slash command cheat sheet
*Quickly internalise the 84 available slash commands so you can use them without hunting through docs.*
> I have Everything Claude Code (ECC) installed and want to build a personal reference for all 84 slash commands. Please: (1) list every available slash command with a one-line description of what it does, (2) group them into logical categories (e.g., Planning, Code Review, Testing, Deployment, Learning), (3) highlight the 10 most impactful commands for day-to-day development, (4) for each highlighted command, provide a worked example showing the exact input and expected output, and (5) export the full list as a markdown table I can save to `COMMANDS.md` in my project root for quick reference inside Claude Code.

#### Prompt 7: Reproduce the Zenith Chat hackathon workflow
*Understand the exact ECC-powered process Afan used to ship a full product in 8 hours — then apply it to your own project.*
> Afan Mustafa used the Everything Claude Code (ECC) setup to build "Zenith Chat" — a full AI product — in 8 hours at the Anthropic x Forum Ventures Hackathon. Using ECC, help me recreate the likely development workflow he followed. Specifically: (1) which ECC agents would be activated first for a greenfield AI chat product (planning, architecture), (2) what slash commands drive the initial scaffolding, (3) how the build-error-fixing agent integrates into the dev loop, (4) how the security review and Playwright E2E testing agents are triggered before submission, and (5) produce a reusable 8-hour sprint template (as a markdown checklist with ECC commands) I can follow for my own hackathon or rapid-prototype project.

### Links & Resources
- [Everything Claude Code (ECC) — GitHub Repository](https://github.com/search?q=everything-claude-code+afan+mustafa&type=repositories) *(search GitHub for exact repo by Afan Mustafa)*
- [Original YouTube Video — InsiderForce](https://www.youtube.com/watch?v=g3Mh8Hws-jo)
- [Claude Code — Anthropic Official](https://claude.ai/code)
- [Anthropic x Forum Ventures Hackathon](https://www.anthropic.com) *(event context)*
- [Model Context Protocol (MCP) — Anthropic](https://modelcontextprotocol.io)
- [Supabase](https://supabase.com)
- [Vercel](https://vercel.com)
- [Railway](https://railway.app)
- [Playwright (E2E Testing)](https://playwright.dev)

### Tags
`#claude-code` `#ai-agents` `#developer-tools` `#mcp` `#open-source` `#productivity`

### Category
Claude Code

---

*Extracted by [Co-Ord Executor](https://github.com/onekiller89/Co-Ord_Executor)*
