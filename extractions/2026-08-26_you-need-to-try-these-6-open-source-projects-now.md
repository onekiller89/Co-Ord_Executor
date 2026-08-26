![banner](https://img.youtube.com/vi/1RTq_EWv2Yo/maxresdefault.jpg)

# You NEED to try these 6 Open-Source Projects NOW

> **Source:** YouTube | **Extracted:** 2026-08-26 00:40 UTC | **Method:** youtube_transcript_api
> **URL:** https://www.youtube.com/watch?v=1RTq_EWv2Yo

---

### Summary
Matthew Berman showcases six open-source projects worth exploring immediately: Unsloth (local LLM fine-tuning and inference), Diagram Design (agent-friendly diagram generation), Obsidian Skills (agent access to Obsidian notes), Buzz (agent-native Slack alternative from Block/Jack Dorsey), Ego Light (fast browser automation for AI agents), and Modely (image-to-3D mesh generation). Each project is free, self-hostable, and designed to either enhance local AI workflows or integrate seamlessly with existing AI coding agents like Claude Code and Codex.

---

### Key Insights

- **Unsloth has evolved far beyond fine-tuning** — it now includes a full ChatGPT-like agent UI with web search, MCP support, memory, tools, and remote access, all running locally with no coding required.
- **Diagram Design fills a real gap in agent output quality** — agents notoriously produce broken, overlapping diagrams; this tool can be installed as a plugin/skill in Claude Code, Codex, Cursor, and Hermes to produce clean, professional diagrams.
- **Obsidian Skills bridges personal knowledge management and AI agents** — agents can read/write your Obsidian vault, making it a local-first knowledge base or "brain" for your agent workflows.
- **Buzz is positioning itself as the team collaboration layer for human+agent teams** — agents are first-class citizens alongside human users, with a Nostr-based audit trail ensuring every action (human or automated) is logged identically.
- **Ego Light solves a key browser automation pain point** — it shares your already-logged-in browser state with agents like Claude Code or Codex, eliminating auth headaches with zero configuration cost.
- **Modely democratises 3D asset creation** — local, GPU-friendly image-to-3D mesh conversion opens up game asset creation and 3D printing workflows without cloud dependencies.
- **The agent-native pattern is emerging as a design philosophy** — multiple projects here (Buzz, Ego Light, Diagram Design) are explicitly built with AI agents as first-class users, not afterthoughts.

---

### Actions

- [ ] Install Unsloth and explore its agent UI for local model inference before committing to fine-tuning
- [ ] Install the Diagram Design MCP plugin into Claude Code and test it with an architecture diagram prompt
- [ ] Set up Obsidian if not already using it, then install Obsidian Skills to give Claude Code access to your vault
- [ ] Star and self-host Buzz to evaluate it as a human+agent collaboration hub for a small project or team
- [ ] Install Ego Light and test browser automation via `/ego browser` in Claude Code or Codex
- [ ] Try Modely with a reference image to generate a 3D mesh for printing or game asset use
- [ ] Check Matthew Berman's linked follow-up video for additional open-source project recommendations

---

### Implementation Prompts

#### Prompt 1: Install and configure the Diagram Design MCP plugin in Claude Code
*Adds clean, professional diagram generation to Claude Code so agents produce readable architecture and flow diagrams instead of broken ASCII art.*

> I want to install the Diagram Design open-source project as an MCP plugin in Claude Code. Please help me:
> 1. Find the correct GitHub repository for "Diagram Design" (the diagram generation tool for AI agents mentioned alongside Claude Code, Codex, and Cursor)
> 2. Write the exact MCP server configuration block to add to my Claude Code `mcp_servers` config (or `CLAUDE.md` if applicable)
> 3. Provide a test prompt I can use immediately after setup to generate a system architecture diagram
> 4. List the diagram types it supports (flowchart, state machine, timeline, etc.) with example prompts for each
> Output the config as a ready-to-paste JSON block and include any required install commands (npm/pip/etc.).

---

#### Prompt 2: Set up Obsidian Skills for Claude Code agent access
*Enables Claude Code to read and write your Obsidian vault, turning it into a persistent local knowledge base your agent can use across sessions.*

> I want to connect my Obsidian vault to Claude Code using the "Obsidian Skills" open-source project. Help me:
> 1. Identify the correct GitHub repo for Obsidian Skills (agent skill specification compatible, works with Claude Code)
> 2. Write step-by-step install instructions for macOS/Linux
> 3. Configure the skill so Claude Code can: (a) read notes by title or tag, (b) create new notes, (c) search across the vault
> 4. Suggest a `CLAUDE.md` entry that tells Claude Code when and how to use the Obsidian skill automatically
> 5. Provide 3 example prompts that demonstrate useful agent+Obsidian workflows (e.g., saving research findings, building a project wiki, storing agent memory)
> My vault is located at `~/Documents/ObsidianVault`. Use that path in all config examples.

---

#### Prompt 3: Integrate Ego Light browser automation with Claude Code
*Gives Claude Code the ability to control your already-authenticated browser sessions, enabling web tasks without re-logging in or complex setup.*

> I want to set up Ego Light (the open-source "fastest browser for AI agents") with Claude Code. Please:
> 1. Provide the GitHub repo URL and installation steps for Ego Light on macOS
> 2. Explain how to invoke it inside Claude Code using the `/ego browser` slash command pattern
> 3. Write a Claude Code hook or script that launches the Ego Light browser context before any web automation task
> 4. Give 5 practical example prompts I can use with Claude Code + Ego Light for real tasks (e.g., scraping a logged-in dashboard, filling a form, extracting data from a behind-login page)
> 5. Explain how Ego Light shares existing browser login state — what browser profiles does it support (Chrome, Firefox, etc.)?
> Make all commands copy-paste ready for a Mac with Apple Silicon.

---

#### Prompt 4: Set up Unsloth for local LLM fine-tuning (no-code approach)
*Gets Unsloth running with its point-and-click interface so you can fine-tune or run inference on open-source models locally without writing any code.*

> Help me install and configure Unsloth for local LLM fine-tuning and inference on my machine. I want the no-code UI experience. Please provide:
> 1. Installation commands for macOS with Apple Silicon (M-series GPU) — if not supported, provide Linux/CUDA instructions as fallback
> 2. How to launch the ChatGPT-like agent UI locally and access it in a browser
> 3. Step-by-step instructions to run inference on a small model (e.g., Gemma or Qwen) immediately after install to verify it works
> 4. How to set up MCP tool support within Unsloth's UI
> 5. How to configure remote access so I can control the Unsloth instance from another device
> 6. A recommended beginner fine-tuning workflow using the point-and-click interface (what dataset format, what settings to start with)
> Include all pip/conda/brew commands needed and flag any common setup errors to watch for.

---

#### Prompt 5: Self-host Buzz (agent-native Slack alternative)
*Gets a privacy-first, self-hosted team chat running where AI agents are first-class members alongside human teammates.*

> I want to self-host Buzz, the open-source agent-native Slack alternative from Block (Jack Dorsey's company). Please provide:
> 1. The GitHub repository URL and a Docker Compose setup for self-hosting on a Linux VPS or local machine
> 2. How to create both human user accounts and AI agent accounts within Buzz
> 3. How to connect an AI agent (e.g., a Claude-powered agent via API) as a first-class Buzz user that participates in channels
> 4. How to set up a simple workflow/automation inside Buzz (e.g., agent auto-responds to a trigger phrase in a channel)
> 5. How the Nostr relay audit trail works and how to query the event log
> 6. Minimum server specs required for a small team (5 humans + 3 agents)
> Output a complete `docker-compose.yml` and `.env` template I can use immediately.

---

#### Prompt 6: Use Modely for image-to-3D mesh generation locally
*Converts any reference image into a 3D-printable or game-ready mesh file entirely on your local GPU, no cloud required.*

> I want to set up Modely, the open-source local image-to-3D mesh generation tool. Help me:
> 1. Find the GitHub repo and install it on a Mac with Apple Silicon (or provide CUDA/Linux instructions if Metal is unsupported)
> 2. Run a test conversion using a sample image to produce a `.obj` or `.stl` mesh file
> 3. Explain the quality settings and trade-offs (speed vs. mesh resolution)
> 4. Describe how to prepare input images for best results (background removal, lighting, angle recommendations)
> 5. Show how to convert the output mesh to a 3D-print-ready `.stl` file and what slicer software works best with it
> 6. Write a simple Python wrapper script that accepts an image path as an argument and outputs a `.stl` file to a specified directory
> Make all commands copy-paste ready and include expected processing time on a consumer GPU.

---

#### Prompt 7: Create a unified CLAUDE.md config that wires all these tools together
*Produces a single CLAUDE.md file that tells Claude Code when and how to use Diagram Design, Obsidian Skills, and Ego Light automatically during relevant tasks.*

> I've installed three tools alongside Claude Code: Diagram Design (MCP plugin for diagrams), Obsidian Skills (vault access), and Ego Light (browser automation). Write a comprehensive `CLAUDE.md` file that:
> 1. Documents all three tools with their trigger conditions (when Claude should automatically use each one)
> 2. Sets behavioural rules: e.g., "always use Diagram Design when asked for architecture or flow diagrams", "save important findings to Obsidian automatically", "use Ego Light for any task requiring web login"
> 3. Includes example slash commands or shorthand phrases for invoking each tool
> 4. Adds a "Tools Available" section Claude can reference when deciding which capability to use
> 5. Includes a brief project context section I can customise with my own project details
> Format as a complete, ready-to-use `CLAUDE.md` file I can place at my project root. Use proper markdown with clear headings and bullet lists.

---

### Links & Resources

- [Unsloth - Local LLM Fine-tuning & Inference](https://unsloth.ai) *(search GitHub: unslothai/unsloth)*
- [Diagram Design - Agent Diagram Generation](https://github.com) *(search: "Diagram Design" agent diagrams open source)*
- [Obsidian - Markdown Note-Taking App](https://obsidian.md)
- [Obsidian Skills - Agent Skill for Obsidian](https://github.com) *(search: "Obsidian Skills" agent skill specification)*
- [Buzz - Open-Source Agent-Native Slack Alternative by Block](https://github.com) *(search: "Buzz" Block Jack Dorsey open source chat)*
- [Ego Light - Fastest Browser for AI Agents](https://github.com) *(search: "Ego Light" browser AI agents open source)*
- [Modely - Image to 3D Mesh Generation](https://github.com) *(search: "Modely" image to 3D open source)*
- [Matthew Berman YouTube Channel](https://www.youtube.com/@matthew_berman)
- [Original Video](https://www.youtube.com/watch?v=1RTq_EWv2Yo)
- [Hostinger - Cloud Hosting (sponsor)](https://hostinger.com) *(use code MatthewB for 10% off)*
- [Nostr Protocol](https://nostr.com) *(used by Buzz for audit logging)*

> **Note:** Exact GitHub URLs were not provided in the video. The links above include search guidance — check the video description for direct links as promised by Matthew Berman.

---

### Tags
`#open-source` `#ai-agents` `#local-ai` `#automation` `#llm-tools`

---

### Category
AI Agents

---

*Extracted by [Co-Ord Executor](https://github.com/onekiller89/Co-Ord_Executor)*
