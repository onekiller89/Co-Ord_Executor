![banner](https://img.youtube.com/vi/b4d32pBa3UY/maxresdefault.jpg)

# This AI System Will Make You So Smart It’s Almost Unfair

> **Source:** YouTube | **Extracted:** 2026-09-15 06:08 UTC | **Method:** youtube_transcript_api
> **URL:** https://www.youtube.com/watch?v=b4d32pBa3UY

---

### Summary
Dan Martell outlines a step-by-step system for building a personal "AI brain" using Obsidian as the knowledge vault, structured identity files, and automated nightly processing. The system combines a permanent knowledge base, consistent AI persona, organised folder architecture, and meeting transcription pipelines to create a self-improving AI assistant. The end goal is an autonomous agent with enough personal context to act on your behalf — drafting emails, recalling contacts, and making informed decisions.

---

### Key Insights

- **Paying for AI is table stakes** — free tiers use older, slower models; upgrading immediately puts you ahead of ~97% of users before you even customise anything.
- **AI has no persistent memory by default** — the only reliable fix is giving it a permanent external knowledge base (files it can always read), not relying on in-app memory features.
- **Three identity files define your AI persona**: `user.md` (who you are), `soul.md` (how the AI should behave/communicate), and `identity.md` (the AI's role and name). Together they transform a generic assistant into a digital clone.
- **Folder structure is the difference between signal and noise** — Martell went from 60% to 85% accuracy just by imposing folder organisation (People, Projects, Decisions, Companies, Meetings, Daily, Knowledge + MOC).
- **Maps of Content (MOC) files** act as index files that consolidate scattered notes across folders into a single reference, preventing topic sprawl as the vault grows.
- **Meeting transcription is the primary feed mechanism** — using Grainola with a custom extraction prompt (decisions, commitments, preferences, key insights → markdown output) automates daily brain-feeding.
- **Nightly automated processing mimics sleep consolidation** — a scheduled Claude task (cron job at 11pm) reads the day's additions, creates missing files, consolidates duplicates, updates MOCs, and flags strategic items for review.
- **Context density drives agent quality** — the more cross-linked a person/project/company is in the vault, the better the AI's answers. Link count is a proxy for contextual signal strength.

---

### Actions

- [ ] Upgrade to a paid AI subscription (ChatGPT Plus, Claude Pro, Gemini Advanced, etc.)
- [ ] Download and install [Obsidian](https://obsidian.md) and create a new vault called something like `AI-Brain`
- [ ] Create the seven core folders inside the vault: `People`, `Projects`, `Decisions`, `Companies`, `Meetings`, `Daily`, `Knowledge`
- [ ] Create a `MOC` folder and leave it empty for now — add index files when topics become messy
- [ ] Use an AI to interview you about your working style, values, and communication preferences, then generate `user.md`, `soul.md`, and `identity.md` files
- [ ] Save all three identity files into the root of your Obsidian vault
- [ ] Install [Grainola](https://www.grainola.ai) (or equivalent meeting transcription tool) and configure a custom extraction template using the four-point prompt (decisions, commitments, preferences, key insights)
- [ ] Configure Grainola to output markdown files to your `Meetings` folder with naming format `YYYY-MM-DD Meeting Name.md`
- [ ] Set up a nightly scheduled task in Claude (or a cron job / automation) to run the brain-consolidation prompt at 11pm
- [ ] Open Obsidian's Graph View each morning to visually monitor how your vault is growing and connecting

---

### Implementation Prompts

#### Prompt 1: Generate your three AI identity files
*Creates the foundational `user.md`, `soul.md`, and `identity.md` files that transform a generic AI into your personal digital clone. Without these, every AI session starts from zero.*

> I want to build a personal AI brain system using Obsidian. To set it up properly, I need you to interview me so you can create three identity files for my AI assistant. Please ask me a series of questions — one at a time — to gather the following information:
>
> 1. **For `user.md`**: My name, roles, titles, communication style preferences, key frameworks I operate by, things I care about most, how I like problems presented to me, and my operating principles.
> 2. **For `soul.md`**: How I want my AI to speak (tone, voice, energy level), what words or hedging phrases I want it to avoid (e.g., "try", "hope", "maybe"), and behavioural rules like "solve before asking" or "challenge me with love".
> 3. **For `identity.md`**: What I want to name my AI, what role(s) it should play (coach, chief of staff, accountability partner, etc.), and how it should introduce itself.
>
> After the interview, produce three complete markdown files — `user.md`, `soul.md`, and `identity.md` — formatted and ready to save into the root of my Obsidian vault. Make them specific, personal, and actionable — not generic templates.

---

#### Prompt 2: Scaffold your Obsidian vault folder structure
*Sets up the exact seven-folder architecture (plus MOC) that provides the structural skeleton your AI brain needs to avoid hallucination and maximise retrieval accuracy.*

> I'm setting up a personal AI brain in Obsidian. Please give me:
>
> 1. A complete folder structure to create inside my Obsidian vault, including these folders: `People`, `Projects`, `Decisions`, `Companies`, `Meetings`, `Daily`, `Knowledge`, and `MOC`.
> 2. For each folder, write a brief `_README.md` file I can place inside it explaining: what goes in this folder, the file naming convention to use (include date formats where relevant), and a one-line example filename.
> 3. A `VAULT_GUIDE.md` root file that gives any AI reading this vault a map of the structure so it understands where to find and store information.
>
> Format all output as markdown code blocks, ready to copy-paste. Use the naming convention `YYYY-MM-DD` for date-stamped files.

---

#### Prompt 3: Create your Grainola / meeting transcription extraction prompt
*Produces a reusable custom prompt template for any meeting transcription tool (Grainola, Otter.ai, Fireflies, etc.) that extracts only what matters — decisions, commitments, people context, and insights — straight into your vault format.*

> I need a meeting extraction prompt template for my AI brain system. I use a meeting transcription tool that lets me set a custom post-meeting processing prompt. The output should be a markdown file that goes into my `Meetings` folder in Obsidian.
>
> Create a prompt template that instructs the AI to extract:
> 1. **Decisions** — What was decided, by whom, and why
> 2. **Commitments** — Who promised what, by when
> 3. **People context** — How attendees communicate, their preferences, any personal details mentioned
> 4. **Key insights** — Strategic shifts, non-obvious observations, frameworks mentioned
> 5. **Action items** — Specific next steps with owners and deadlines
>
> Rules for the prompt: output as clean markdown, skip small talk and filler, use headers for each section, flag anything that should create or update a People/Companies/Projects file in my vault. Include a frontmatter block with date, meeting name, and attendees.
>
> Then write a second version of the same prompt, shortened to under 100 words, for tools with character limits.

---

#### Prompt 4: Build the nightly brain-consolidation prompt
*Replicates the "sleep consolidation" step — the automated nightly process that creates missing files, merges duplicates, updates MOCs, and flags strategic items. This is what turns a static note archive into a self-improving brain.*

> I want to set up a nightly automated prompt that runs against my Obsidian vault to consolidate and improve my AI brain. Write a complete, production-ready prompt I can use as a scheduled task (e.g., via Claude's scheduled tasks, a cron job, or an automation tool like Make or Zapier).
>
> The prompt should instruct the AI to:
> 1. Read everything added or modified in the vault today
> 2. Find "orphan notes" — mentions of people, projects, or companies that don't yet have their own files — and create stub files for them in the correct folders
> 3. Identify and consolidate duplicate or near-duplicate notes
> 4. Update all relevant MOC (Maps of Content) files with new links
> 5. Strengthen connections between related notes by adding cross-links
> 6. Flag 3-5 strategic items for me to review tomorrow morning, with a one-line explanation of why each matters
> 7. Output a short "Brain Report" summarising what changed tonight
>
> Format the prompt so it can be copy-pasted directly into a Claude scheduled task. Also provide a version formatted as a shell script comment block for use with a cron job.

---

#### Prompt 5: Create a People file template
*People files are the highest-leverage notes in your vault — they store contact details, communication preferences, relationship history, and commitments. A good template ensures consistency so the AI can reliably retrieve and update them.*

> Create a markdown template for a `People` file in my Obsidian AI brain vault. This template will be used for every person I interact with professionally or personally.
>
> The template should include sections for:
> - Full name, role/title, company
> - Contact details (email, phone, LinkedIn, etc.)
> - Communication style and preferences (how they like to be communicated with)
> - Relationship context (how we met, when, mutual connections)
> - Key decisions or commitments involving this person (with dates)
> - Notes from meetings (linked to the Meetings folder files)
> - Personal details worth remembering (interests, family, preferences)
> - Last contacted date and next planned touchpoint
> - Tags/links to related Projects and Companies files
>
> Use Obsidian markdown formatting including frontmatter (YAML), headers, and dataview-compatible fields where relevant. The filename format should be `Firstname Lastname.md`. Make it practical for an AI agent to read, update, and query.

---

#### Prompt 6: Generate a Daily note template with AI brain integration
*Daily notes are the primary input stream for your brain — a consistent template ensures each day's entry feeds the right structured data into the vault, making the nightly consolidation step more effective.*

> Create a Daily note template for my Obsidian AI brain vault. I write a short daily entry (3-5 lines minimum, up to a page) capturing what happened, what I decided, and what I'm thinking about.
>
> Design a template that:
> 1. Auto-populates today's date in the filename (`YYYY-MM-DD.md`) and as a header
> 2. Has sections for: Top 3 priorities for the day, Decisions made today (with brief rationale), People interacted with (linked to People files), Energy/mood snapshot (1 line), Key insight or learning, Tomorrow's open loops
> 3. Includes a section for free-form brain dump
> 4. Has frontmatter tags so the nightly consolidation AI can easily identify and parse daily notes
> 5. Ends with a "Feed to brain" checklist — checkboxes for items the AI should extract into other vault folders (e.g., "[ ] Create/update People file for [name]", "[ ] Log decision in Decisions folder")
>
> Format as a complete Obsidian markdown template, ready to use with the Templater plugin or as a default template.

---

#### Prompt 7: Audit and stress-test your AI brain setup
*Before relying on this system for real decisions, you need to verify it's working correctly — that the AI can retrieve the right information, the folder structure is consistent, and the identity files are producing the right tone and behaviour.*

> I've set up a personal AI brain in Obsidian with the following structure: folders for People, Projects, Decisions, Companies, Meetings, Daily, Knowledge, and MOC. I also have three identity files: `user.md`, `soul.md`, and `identity.md`.
>
> Help me run an audit of this system by giving me:
> 1. **10 test queries** I should ask my AI to verify it can correctly retrieve and synthesise information from my vault (e.g., "Who did I commit to follow up with this week?", "What decisions have I made about [topic]?")
> 2. **5 stress-test scenarios** that would expose weaknesses in the folder structure or file naming conventions
> 3. **A checklist of 10 things to verify** before I start relying on this brain for real decisions — covering file structure, identity file quality, MOC coverage, and nightly consolidation output
> 4. **Common failure modes** in personal AI brain setups and how to diagnose and fix each one
>
> Format as a practical QA checklist I can work through in one sitting.

---

### Links & Resources

- [Video: This AI System Will Make You So Smart It's Almost Unfair — Dan Martell](https://www.youtube.com/watch?v=b4d32pBa3UY)
- [Obsidian — Local markdown knowledge base](https://obsidian.md)
- [Notion — Cloud-based AI-native data store](https://www.notion.so)
- [Google Drive — Basic cloud file storage](https://drive.google.com)
- [Grainola — AI meeting transcription with custom templates](https://www.grainola.ai)
- [Claude by Anthropic — AI with scheduled tasks feature](https://claude.ai)
- [Dan Martell on Instagram — DM "YouTube OS" for the AI Company OS Playbook](https://www.instagram.com/danmartell)

---

### Tags
`#second-brain` `#pkm` `#ai-productivity` `#obsidian` `#automation` `#knowledge-management`

---

### Category
Personal Knowledge Management

---

*Extracted by [Co-Ord Executor](https://github.com/onekiller89/Co-Ord_Executor)*
