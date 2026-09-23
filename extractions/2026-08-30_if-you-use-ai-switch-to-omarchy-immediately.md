![banner](https://img.youtube.com/vi/KO2T0oET9go/maxresdefault.jpg)

# If you use AI, switch to Omarchy immediately

> **Source:** YouTube | **Extracted:** 2026-08-30 11:10 UTC | **Method:** youtube_transcript_api
> **URL:** https://www.youtube.com/watch?v=KO2T0oET9go

---

### Summary
Omarchy (stylised "Omachi" in the transcript) is a free, open-source, AI-native Linux operating system built by DHH (creator of Ruby on Rails and Basecamp). It combines a keyboard-first tiling window manager with deep AI integration, allowing users to modify any part of the OS using AI agents. The presenter argues it surpasses macOS and Windows in speed, aesthetics, and personalisation — particularly because its open-source nature enables AI-assisted customisation of the OS itself.

---

### Key Insights

- **AI-native OS customisation is the real breakthrough**: Because Omarchy is open-source, you can point an AI agent at the codebase and say "change this behaviour" — and it does. This is fundamentally impossible on macOS or Windows.
- **Keyboard-first tiling WM eliminates window chaos**: No floating windows — everything is a tile. This forces focus, reduces tab/window accumulation, and dramatically speeds up navigation via keybinds (Super + arrow, Super + 1-5, etc.).
- **Runs on virtually any hardware**: Even machines with 2GB RAM. Old laptops, closet computers, 15-year-old hardware — all viable targets. DHH recommends Dell XPS; the presenter bought a Framework laptop.
- **All major AI tools work out of the box**: Claude, ChatGPT, Grok, Hermes agent — all pre-integrated. Token usage tracking is built directly into the OS UI.
- **Tiling layout enforces productive constraints**: Continuously splitting screens create natural friction against accumulating hundreds of open windows, which is a common productivity killer on traditional OSes.
- **The open-source stack vision**: Local LLM + open-source agent harness + open-source OS = a fully customisable intelligence and compute stack that adapts entirely to your needs.
- **Installation is beginner-accessible via AI assistance**: Flash to USB, ask an AI agent to walk you through it step by step — no prior Linux experience required.

---

### Actions

- [ ] Watch the video and identify an old/spare computer (laptop or desktop) to test Omarchy on without risk
- [ ] Download the Omarchy ISO from the official repository (omarchy.org or GitHub)
- [ ] Get a USB drive (8GB+) and ask Claude/ChatGPT to walk you through flashing Omarchy onto it using Balena Etcher or `dd`
- [ ] Install Omarchy on your spare machine and spend one focused work session using only keybinds (no mouse)
- [ ] Learn the core keybinds: Super+Arrow (focus), Super+1-5 (desktops), Super+Enter (terminal), Super+Shift+Enter (browser), Super+Space (app launcher)
- [ ] Identify one thing you dislike about the default setup and ask an AI agent to modify it (notifications, window layout, keybind, theme)
- [ ] Set up a dedicated "OS dev" AI agent (Grok team or Claude project) specifically for Omarchy customisation tasks
- [ ] Explore themes via Super+Space → search "theme" and pick one that suits your workflow aesthetic
- [ ] Try adding a custom keybind (e.g., Super+A for to-do capture) by asking your AI agent to edit the relevant config file

---

### Implementation Prompts

#### Prompt 1: Flash Omarchy to USB and Install
*Gets you from zero to a running Omarchy install. Covers the full setup process for someone with no prior Linux experience.*

> I want to install Omarchy (the AI-native Linux OS by DHH) on a spare computer. I have a USB drive and I'm currently on [macOS/Windows]. Please give me step-by-step instructions to: 1) Download the latest Omarchy ISO (check omarchy.org or the official GitHub), 2) Flash it to my USB drive using Balena Etcher or the command line, 3) Boot my target machine from USB, 4) Walk through the installation process. My target machine specs are: [insert RAM, CPU, storage]. Flag any potential compatibility issues and tell me what to back up before starting.

---

#### Prompt 2: Learn Core Omarchy Keybinds Fast
*Generates a quick-reference cheat sheet so you can become keyboard-native in your first session.*

> Create a concise, printable keybind cheat sheet for Omarchy (the tiling window manager Linux OS by DHH). Include: window focus navigation (Super+Arrow), desktop switching (Super+1-5), opening terminal, opening browser, app launcher, tiling layout controls, and any common system shortcuts. Format it as a clean markdown table with columns: Keybind | Action | Notes. Also include 3–5 tips for someone switching from macOS who is used to mouse-driven workflows.

---

#### Prompt 3: Customise the OS with an AI Agent
*Replicates the "edit your OS with AI" workflow from the video — the core value proposition of Omarchy.*

> I'm using Omarchy (open-source Linux OS based on a tiling WM). I want to make a customisation using an AI agent. The change I want is: [describe your change, e.g., "make all open windows equal size when I press a keybind" or "add a close button to all notifications including critical ones"]. Please: 1) Identify which Omarchy config file or script controls this behaviour, 2) Show me the exact code change needed, 3) Tell me the command to apply it without rebooting, 4) Suggest a keybind that doesn't conflict with defaults. Assume I have access to the terminal and basic file editing tools.

---

#### Prompt 4: Add a Custom To-Do Capture Keybind
*Recreates the Super+A to-do list feature from the video — a practical example of OS-level personalisation.*

> I'm running Omarchy Linux and want to add a quick to-do capture feature: when I press Super+A, a small popup terminal or dialog appears where I can type a task, hit Enter, and it saves to a plain text file at ~/todos.txt. Please provide: 1) The script to create this capture popup (using rofi, zenity, or a terminal command — whichever works best on Omarchy), 2) The exact lines to add to my Omarchy keybind config to bind this to Super+A, 3) How to reload the config without rebooting. Also show me a simple command to view my saved tasks from the terminal.

---

#### Prompt 5: Set Up a Dedicated Omarchy Dev AI Agent
*Creates a reusable AI agent context for ongoing OS customisation — the "Omachi dev" Grok agent mentioned in the video.*

> I want to create a dedicated AI agent (as a Claude Project or custom GPT) specifically for customising my Omarchy Linux OS. Help me write the system prompt / project instructions for this agent. It should: know Omarchy is based on [tiling WM — likely i3/Hyprland/Sway — check the actual Omarchy repo], understand the file structure and config locations, always provide terminal-ready commands, ask clarifying questions before making changes that could break the desktop, and suggest safe ways to test changes before committing. Also include a list of the 10 most common customisation tasks I should tell it I might ask about.

---

#### Prompt 6: Compare Omarchy to Your Current Setup
*Helps you make an informed decision before committing, by mapping your current workflows to Omarchy equivalents.*

> I currently use [macOS/Windows] and my daily workflow includes: [list your main apps and tasks, e.g., browser, code editor, video calls, Notion, Spotify, etc.]. I'm considering switching to or dual-booting Omarchy Linux. Please: 1) Tell me which of my apps have native Linux versions or good alternatives, 2) Flag anything that might not work well on Linux, 3) Explain how a tiling WM workflow would change my daily habits, 4) Suggest the lowest-risk way to try Omarchy (spare machine, dual boot, or VM) given my setup. Be honest about trade-offs — don't just sell me on Linux.

---

#### Prompt 7: Build a Context-Switching OS Mode
*Implements the "future vision" from the video — an OS that morphs based on what you're doing.*

> I'm running Omarchy Linux and want to create two "work modes" that I can switch between with a keybind: 1) CODE MODE: switches to a dark minimal theme, opens my terminal and code editor side by side, closes all notifications, sets do-not-disturb. 2) FOCUS/WRITING MODE: opens a single full-width window with my writing app, plays lo-fi music via the CLI player, dims other desktops. Please write the shell scripts for each mode and the keybind config entries to trigger them (e.g., Super+Shift+C for code, Super+Shift+W for writing). Include how to detect and use Omarchy's theme-switching command inside the scripts.

---

### Links & Resources

- [Omarchy Official Site / Repo](https://omarchy.org) *(check for current URL — may be omarchy.org or GitHub)*
- [DHH on GitHub](https://github.com/dhh)
- [Ruby on Rails](https://rubyonrails.org) — DHH's prior major open-source project
- [Basecamp](https://basecamp.com) — DHH's company
- [Framework Laptop](https://frame.work) — recommended Linux-compatible laptop mentioned in video
- [Balena Etcher](https://etcher.balena.io) — tool for flashing OS images to USB
- [Hermes Agent](https://github.com) *(search "Hermes AI agent" for current repo)*
- [Original Video](https://www.youtube.com/watch?v=KO2T0oET9go) — Alex Finn, "If you use AI, switch to Omarchy immediately"

---

### Tags
`#omarchy` `#linux` `#open-source` `#ai-native` `#productivity`

---

### Category
Open Source

---

*Extracted by [Co-Ord Executor](https://github.com/onekiller89/Co-Ord_Executor)*
