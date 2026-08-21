![banner](https://img.youtube.com/vi/z4AbijUCoKU/maxresdefault.jpg)

# Give Me 15 Minutes. I'll Teach You  80% of Obsidian

> **Source:** YouTube | **Extracted:** 2026-08-21 00:20 UTC | **Method:** youtube_transcript_api
> **URL:** https://www.youtube.com/watch?v=z4AbijUCoKU

---

### Summary
This video by Nick Milo (Linking Your Thinking) delivers a fast-paced practical introduction to Obsidian, covering its core value proposition: local-first markdown notes you own, bidirectional linking, and flexible organisation. The tutorial walks through vault setup, essential hotkeys, folder structure (the ACE framework), graph view, plugins to avoid early on, and AI integration options — giving beginners a solid 80% foundation in under 15 minutes.

---

### Key Insights

- **You own your data** — Obsidian notes are plain `.md` files in a folder on your computer, readable in any markdown-compatible app (VS Code, iA Writer, Ulysses, etc.), making you vendor-independent forever.
- **Links are the superpower** — Use `[[double brackets]]` to create and connect notes simultaneously; unresolved links still appear in search and graph view, encouraging fearless linking before writing.
- **Enable "automatically update internal links"** in Settings → Files & Links immediately — without this, renaming a note silently breaks all links pointing to it.
- **The ACE folder structure** (Atlas, Calendar, Efforts) provides a minimal but scalable organisational skeleton: timeless ideas, time-based notes (journal/daily), and active projects respectively.
- **Avoid plugin overload on day one** — resist Dataview, Kanban, and Advanced Tables early; master linking first, then layer complexity only as genuine need arises.
- **Maps of Content (MOCs) beat tags** for organising knowledge — a MOC is a note that links and curates other notes by theme, creating strong hubs in the graph view rather than flat tag lists.
- **AI integration is opt-in and self-directed** — Obsidian has no native AI; you choose tools like Claude for querying notes, keeping a clear boundary between your original thinking and AI-generated content.
- **Hotkeys are non-negotiable for speed** — `Cmd+O` (quick switcher), `Cmd+P` (command palette), `Cmd+[[` (link), and navigation shortcuts (`Cmd+Opt+←/→`) dramatically reduce friction once learned.

---

### Actions

- [ ] Download and install Obsidian from obsidian.md, create your first vault in a dedicated folder on your desktop
- [ ] Go to **Settings → Files & Links** → enable "Automatically update internal links"
- [ ] Set a dedicated **Attachments folder** in Settings → Files & Links to prevent image clutter in the sidebar
- [ ] Install the **Anuppuchin** theme (Settings → Appearance → Manage → search "Anuppuchin") as a base
- [ ] Create the ACE folder structure: `Atlas/`, `Calendar/`, `Efforts/` as your three top-level folders
- [ ] Create your first 3 notes and practice linking them with `[[double brackets]]` — observe them appear in graph view
- [ ] Enable the **Templates** core plugin and create at least one reusable note template
- [ ] Enable the **Audio Recorder** core plugin for quick voice memos
- [ ] Practice the essential hotkeys: `Cmd+B`, `Cmd+I`, `Cmd+O`, `Cmd+P`, `Cmd+T`, `Cmd+W`, `Cmd+F`, `Cmd+;`
- [ ] Download Nick Milo's free **Ideverse** template vault to get a pre-built foundation
- [ ] Create your first **Map of Content** note that links to 5+ related notes on a topic you care about
- [ ] Set up a **Daily Note** in the `Calendar/` folder and use it for one week of capture

---

### Implementation Prompts

#### Prompt 1: Generate a personalised Obsidian vault starter structure
*Creates a ready-to-use folder and file scaffold matching the ACE framework, so you can start with clean organisation instead of an empty vault.*

> Create a complete Obsidian vault starter structure using the ACE framework (Atlas, Calendar, Efforts). Output the following as individual markdown file contents I can paste directly into Obsidian:
> 
> 1. A `README.md` at the vault root explaining the ACE structure and how to use it
> 2. An `Atlas/Atlas MOC.md` — a Map of Content template with sections for: Concepts, People, Books, Topics (each with placeholder `[[links]]`)
> 3. A `Calendar/Daily Note Template.md` — a daily note template with: date property (using YAML frontmatter), sections for "Today's Focus", "Thoughts & Captures", "Links to Explore", and "Gratitude"
> 4. An `Efforts/Efforts MOC.md` — a project hub template with sections for Active, Paused, and Completed efforts, each with placeholder links
> 5. A `Meta/Hotkeys Reference.md` note listing all essential Obsidian hotkeys (bold, italic, link, quick switcher, command palette, new tab, close tab, navigate back/forward, add property, find on page)
> 
> Use proper markdown formatting. Include YAML frontmatter with `created`, `tags`, and `type` properties on each file. Make all placeholder links use `[[double bracket]]` syntax.

---

#### Prompt 2: Build a Map of Content (MOC) for any topic
*Generates a structured MOC note for a topic of your choice, giving you a ready-made knowledge hub to drop into your Atlas folder.*

> I'm building a Map of Content (MOC) note in Obsidian for the topic: **[INSERT YOUR TOPIC HERE]**. 
> 
> Create a complete markdown MOC note I can paste directly into Obsidian. It should include:
> - YAML frontmatter with `type: MOC`, `tags`, and `created` fields
> - An introductory paragraph summarising what this MOC covers and why it matters
> - 4–6 thematic sections, each with a brief explanation and 3–5 placeholder `[[Note Title]]` links representing subtopics, questions, or related ideas I should explore
> - A "Questions I'm Exploring" section with 3 open-ended questions formatted as `[[links]]` I can turn into notes
> - A "Related MOCs" section linking to 2–3 adjacent topics
> 
> Make the note titles in `[[brackets]]` specific and meaningful (not generic), as if they were real evergreen notes in a personal knowledge base. Format using proper Obsidian markdown.

---

#### Prompt 3: Create an Obsidian daily note template with AI-assisted reflection prompts
*Produces a rich daily note template optimised for capture, linking, and end-of-day reflection — ready to use with Obsidian's Templates core plugin.*

> Create an Obsidian daily note template for use with the Templates core plugin. The file should be saved as `Calendar/Templates/Daily Note.md`.
> 
> Requirements:
> - YAML frontmatter with: `date`, `day-of-week`, `week-number`, `mood` (dropdown options: energised, focused, neutral, tired, stressed), `type: daily`
> - **Morning section**: "Today's Intentions" (3 bullet checkboxes), "Most Important Task" (single line), "What I'm Grateful For" (2–3 bullets)
> - **Capture section**: "Thoughts & Ideas" (freeform, with reminder to use `[[links]]`), "Things I Learned", "Interesting Quotes or References"
> - **Evening reflection section**: "What Went Well", "What I'd Do Differently", "One Insight Worth Keeping" (with prompt to turn this into a permanent note using `[[link]]`)
> - **Connections section**: "Notes This Links To" (placeholder `[[links]]`), "Projects/Efforts Touched Today" (placeholder `[[links]]`)
> - A footer reminder: "Remember: capture fast, link freely, refine later."
> 
> Use clean markdown formatting with H2 section headers and emoji for visual scanning. Make it copy-paste ready.

---

#### Prompt 4: Generate an evergreen note from a raw idea or quote
*Takes any rough idea, quote, or thought and transforms it into a properly formatted Obsidian evergreen note with connections — ideal for building your Atlas.*

> Transform the following raw idea/quote/thought into a properly structured Obsidian evergreen note:
> 
> **Raw input:** [PASTE YOUR IDEA, QUOTE, OR ROUGH THOUGHT HERE]
> 
> Produce a complete markdown note with:
> - YAML frontmatter: `type: concept`, `created`, `tags` (suggest 2–3 relevant tags), `status: seedling`
> - A single declarative title (the note filename should be a clear statement, e.g. "Constraints breed creativity")
> - An opening paragraph of 3–5 sentences that expands the idea in my own voice (write as if I'm the author)
> - A "Why This Matters" section (2–3 sentences on practical relevance)
> - A "Connections" section with 4–6 `[[suggested note titles]]` I should either find or create in my vault — make these specific and meaningful
> - A "Questions This Raises" section with 2–3 open questions formatted as potential future note titles in `[[brackets]]`
> - A "Sources & References" section (leave as placeholder bullets)
> 
> Keep the tone intellectual but conversational. The note should feel like something I wrote, not a Wikipedia article.

---

#### Prompt 5: Design a personal plugin adoption roadmap for Obsidian
*Creates a phased, week-by-week plan for adding Obsidian plugins and features without overwhelming yourself — following Nick Milo's "master linking first" philosophy.*

> Create a phased Obsidian plugin and feature adoption roadmap for a new user who has just set up their vault. The plan should follow the principle: master the basics before adding complexity.
> 
> Format this as a markdown note I can save in Obsidian as `Meta/Obsidian Learning Roadmap.md`.
> 
> Structure it as:
> - **Week 1 — Foundation**: Core habits to build (linking, daily notes, basic hotkeys). Zero plugins beyond Obsidian defaults. Specific daily practice suggestions.
> - **Week 2–3 — Core Plugins**: Which built-in Obsidian core plugins to enable and why (e.g., Templates, Audio Recorder, Backlinks, Graph View). One practice exercise per plugin.
> - **Month 2 — First Community Plugins**: Recommend 3–4 community plugins suitable at this stage (with brief reason for each and install instructions as a checklist). Suggested: focus on ones that enhance linking and navigation, not databases.
> - **Month 3+ — Power Features**: When and why to consider Dataview, Bases, Canvas, and AI integrations. Include a warning checklist of signs you're adding complexity too early.
> - A "Plugins to Avoid Until Month 3+" section listing common temptations and why to wait.
> 
> Include YAML frontmatter and format with clear H2/H3 headers, checkboxes, and callout blocks (using Obsidian `> [!tip]` syntax).

---

#### Prompt 6: Create a hotkey mastery practice plan
*Generates a structured 7-day drill plan to internalise Obsidian's essential keyboard shortcuts, turning them into muscle memory through deliberate daily practice.*

> Create a 7-day Obsidian hotkey mastery plan I can save as `Meta/Hotkey Practice Plan.md` in my vault.
> 
> For each day, provide:
> - The 2–3 hotkeys to focus on that day (Mac version + Windows equivalent)
> - A brief explanation of what each hotkey does and when to use it
> - A specific 5-minute practice drill I can do inside Obsidian (e.g., "Create 5 notes using only Cmd+O and Cmd+T, link them all without touching the mouse")
> - A "mastery check" — a simple test to know I've got it
> 
> Day topics should follow this sequence:
> - Day 1: Navigation (Cmd+O, Cmd+P, Cmd+T, Cmd+W)
> - Day 2: Text formatting (Cmd+B, Cmd+I, headings with #)
> - Day 3: Linking (`[[`, Cmd+Opt+←/→ for back/forward)
> - Day 4: Search and find (Cmd+F, Cmd+Shift+F for global search)
> - Day 5: Note management (Cmd+;, rename, move to folder)
> - Day 6: Embed and reference (! prefix for embeds, external links)
> - Day 7: Full workflow run-through combining all hotkeys in a timed note-making session
> 
> Format as a clean markdown document with checkboxes for each drill step. Add a motivational note at the top about why hotkey fluency matters for thinking speed.

---

### Links & Resources

- [Obsidian Official Site](https://obsidian.md)
- [Linking Your Thinking with Nick Milo — YouTube Channel](https://www.youtube.com/@linkingyourthinking)
- [Source Video: Give Me 15 Minutes. I'll Teach You 80% of Obsidian](https://www.youtube.com/watch?v=z4AbijUCoKU)
- [Ideverse Free Template Vault (referenced, scan QR in video)](https://www.linkingyourthinking.com) *(check Nick Milo's site for direct link)*
- [Anuppuchin Theme — Obsidian Community Themes](https://github.com/AnubisNekhet/AnuPpuccin)
- [Obsidian Sync (paid official sync)](https://obsidian.md/sync)
- [Obsidian Bases Feature](https://obsidian.md/bases) *(referenced in video)*
- [Claude AI](https://claude.ai) *(recommended by Nick for AI integration with Obsidian)*

---

### Tags
`#obsidian` `#note-taking` `#personal-knowledge-management` `#productivity` `#markdown`

---

### Category
Personal Knowledge Management

---

*Extracted by [Co-Ord Executor](https://github.com/onekiller89/Co-Ord_Executor)*
