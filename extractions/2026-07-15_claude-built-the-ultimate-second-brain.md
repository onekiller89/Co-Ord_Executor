![banner](https://img.youtube.com/vi/cwf2vEAigKA/maxresdefault.jpg)

# Claude Built the Ultimate Second Brain

> **Source:** YouTube | **Extracted:** 2026-07-15 23:23 UTC | **Method:** youtube_transcript_api
> **URL:** https://www.youtube.com/watch?v=cwf2vEAigKA

---

### Summary
Wes Roth demonstrates how to build an AI-powered "Second Brain" using Obsidian (local markdown-based note-taking) and Claude Code as the AI engine. The system automatically ingests, organises, cross-links, and summarises knowledge — from YouTube analytics to sponsor deadlines — creating a living, compounding knowledge graph. Inspired by Andrej Karpathy's "LLM Wiki" concept, this system runs 24/7 on a cheap mini-PC, costs under $100 to bootstrap, and gets smarter over time as both data and AI models improve.

---

### Key Insights

- **Flat folder structure is critical**: Avoid deep nested subfolders — they become nightmares for LLMs to navigate. Use 3 core folders (inbox, raw, wiki) and let cross-links handle topic organisation instead of subdirectories.
- **The three-layer architecture**: Raw data flows in → Wiki organises and cross-links → Doctrine produces actionable insights. Each layer has a distinct role and shouldn't be conflated.
- **Markdown is the durable format**: Because everything is stored as plain `.md` files on your local machine, you're never locked into any app, model, or vendor. The data survives everything.
- **CLAUDE.md is the employee handbook**: Claude reads this rulebook every session and follows it automatically — define your ingestion rules, folder purposes, and naming conventions here.
- **The OODA loop makes it compound**: Observe (data collection) → Orient (wiki/summaries) → Decide (doctrine/strategy) → Act (execution) → feed results back in. The longer it runs, the more valuable it becomes.
- **A $200 always-on mini-PC is the war room**: A cheap always-on device runs cron jobs, ingests new data nightly, and keeps the second brain updated without touching your main machine.
- **LLMs are the missing piece from an 80-year-old idea**: Vannevar Bush's 1945 "Memex" concept was always the dream — LLMs finally make it practical by acting as the tireless librarian.
- **The system improves automatically as models improve**: Unlike traditional databases, this second brain gets smarter every time a better model is released — it's future-proof by design.

---

### Actions

- [ ] Download and install [Obsidian](https://obsidian.md) (free, no sign-up required)
- [ ] Install [Claude Code Desktop](https://claude.ai/code) and log in
- [ ] Create a new Obsidian vault called `second-brain` with three root folders: `inbox/`, `raw/`, `wiki/`
- [ ] Inside `wiki/`, create subfolders: `concepts/`, `entities/`, `summaries/` plus two empty notes: `index.md` and `log.md`
- [ ] Write (or have Claude generate) a `CLAUDE.md` rulebook defining folder purposes, ingestion rules, and naming conventions
- [ ] Enable the **Dataview** and **Kanban** community plugins in Obsidian settings
- [ ] Tell Claude Code to scaffold the entire vault structure and write the CLAUDE.md for you
- [ ] Start ingesting: paste one URL per day into Claude Code and say `ingest [URL]`
- [ ] Set up at least one automated cron job to pull data you care about (RSS feeds, YouTube stats, X analytics, etc.)
- [ ] Set up a $200 mini-PC (or repurpose an old machine) to run ingestion agents 24/7
- [ ] Download the PDF template from the video description and hand it to Claude Code to auto-build the system

---

### Implementation Prompts

#### Prompt 1: Scaffold the entire Second Brain vault structure
*Automates the tedious setup of folders, starter files, and a working CLAUDE.md so you can skip directly to ingesting content.*

> I want to build an AI-powered Second Brain using Obsidian and Claude Code. Please scaffold the following directory structure inside a folder called `second-brain/`:
>
> ```
> second-brain/
> ├── inbox/          # Quick captures waiting to be processed
> ├── raw/            # Immutable source documents (never edit these)
> ├── wiki/
> │   ├── concepts/   # Abstract ideas, frameworks, mental models
> │   ├── entities/   # People, companies, products, tools
> │   ├── summaries/  # LLM-generated summaries of raw content
> │   ├── index.md    # Master index of all wiki pages
> │   └── log.md      # Daily activity log
> ├── doctrine/       # Actionable insights and strategies derived from wiki
> └── CLAUDE.md       # Rulebook for the AI librarian
> ```
>
> Then generate a comprehensive `CLAUDE.md` file that:
> 1. Defines the purpose of each folder
> 2. Specifies that raw/ files are immutable — never edit them, only read
> 3. Instructs Claude to always cross-link related pages using `[[double brackets]]`
> 4. Keeps folder structure flat — no deep nesting, topics live in links not folders
> 5. Defines the ingestion workflow: raw → summarise → wiki → cross-link → update index.md and log.md
> 6. Instructs Claude to update existing entity/concept pages when new related content arrives ("ripple updates")
> 7. Specifies markdown formatting standards (H2 for sections, bullet lists for facts, frontmatter with date and tags)
>
> Create a sample `wiki/entities/example-entity.md` and `wiki/concepts/example-concept.md` showing the expected format.

---

#### Prompt 2: Build a universal content ingestion command
*Creates a reusable ingestion workflow so pasting any URL or text triggers a full parse, summarise, and cross-link pipeline.*

> I have an Obsidian second-brain vault at `~/second-brain/` with folders: inbox/, raw/, wiki/concepts/, wiki/entities/, wiki/summaries/. 
>
> Create a bash script called `ingest.sh` that accepts a URL or file path as an argument. When run, it should:
> 1. Fetch the content (use `curl` for URLs, read directly for files)
> 2. Save the raw content as-is to `raw/YYYY-MM-DD-[slug].md` with a frontmatter header containing source URL, date, and type
> 3. Print a structured prompt to stdout that I can paste into Claude Code to: (a) generate a 200-word summary saved to `wiki/summaries/`, (b) extract all entities (people, companies, tools, papers) and create/update their pages in `wiki/entities/`, (c) extract key concepts and create/update pages in `wiki/concepts/`, (d) add cross-links using [[double brackets]] throughout, (e) append an entry to `wiki/index.md` and `wiki/log.md`
>
> Also write the Claude Code prompt I should use after running the script, instructing Claude to perform steps (a)–(e) above, referencing the raw file path. The prompt should end with: "After completing all updates, list every file you created or modified."
>
> Target: macOS/Linux bash, no external dependencies beyond curl.

---

#### Prompt 3: Generate a CLAUDE.md rulebook for your specific use case
*Customises the AI librarian's behaviour for your personal or professional domain so ingestion and insights are relevant to you.*

> I'm building a personal Second Brain in Obsidian. My focus areas are: [REPLACE WITH YOUR TOPICS, e.g., "AI research, content creation, YouTube analytics, sponsor management"].
>
> Generate a detailed `CLAUDE.md` file for my vault that acts as Claude's standing instructions. Include these sections:
>
> **1. Identity & Mission** — Claude is my AI librarian. Its job is to maintain the wiki, never lose data, and surface insights.
>
> **2. Folder Rules** — Define inbox/ (unprocessed captures), raw/ (immutable sources), wiki/ (living knowledge base), doctrine/ (actionable strategies).
>
> **3. Ingestion Protocol** — Step-by-step: receive input → save raw → summarise → extract entities/concepts → cross-link → ripple-update related pages → update log.
>
> **4. Cross-linking Rules** — Always use [[Page Name]] syntax. Create the page if it doesn't exist. Never use bare topic mentions without linking.
>
> **5. Naming Conventions** — Files use kebab-case. Dates in frontmatter use ISO 8601. Entity pages start with a one-line description.
>
> **6. Flat Structure Rule** — Maximum 2 levels of nesting. Topics are expressed as links, not folders.
>
> **7. Doctrine Generation** — When asked, analyse wiki/ contents and produce a doctrine/ document with actionable insights, each claim traced to a source file.
>
> **8. What Claude Must Never Do** — Never delete raw/ files. Never rename files without logging the change. Never hallucinate sources.
>
> Make the tone direct and operational, as if writing instructions for a new employee.

---

#### Prompt 4: Build a Kanban sponsor/project tracker in Obsidian
*Replicates Wes's sponsor workflow board so deadlines and project stages are visible and manageable without leaving Obsidian.*

> I use Obsidian with the Kanban community plugin installed. Create a Kanban board file at `second-brain/wiki/sponsor-tracker.md` using Obsidian Kanban plugin syntax.
>
> The board should have these columns: **Incoming** | **Script Draft** | **Awaiting Approval** | **Recording** | **Editing** | **Published**
>
> Each card should support these metadata fields in the card body:
> - Sponsor name (linked as [[Sponsor Name]] to their entity page)
> - Due date
> - Deliverable type (video integration / dedicated / social post)
> - Notes
> - Asset links
>
> Also create a template file at `second-brain/wiki/templates/sponsor-card-template.md` that I can copy for each new sponsor.
>
> Finally, write a Claude Code prompt I can use to: (1) add a new sponsor card by just telling Claude the sponsor name and due date, (2) move a card to a new column by name, (3) generate a weekly summary of what's due in the next 7 days across all active columns.
>
> Use valid Obsidian Kanban plugin markdown syntax throughout.

---

#### Prompt 5: Set up automated daily ingestion cron jobs
*Automates the "war room" — pulling fresh data into your second brain every day without manual effort.*

> I want to automate daily data ingestion into my Obsidian second-brain vault at `~/second-brain/`. 
>
> Help me set up cron jobs (macOS launchd or Linux cron) that run daily at 7am to ingest the following sources:
> 1. **RSS feeds** — given a list of feed URLs I'll provide, fetch new items from the last 24 hours and save each as a raw/ file
> 2. **YouTube channel stats** — using the YouTube Data API v3, fetch my latest video performance metrics and append to `wiki/entities/my-youtube-channel.md`
> 3. **A custom URL list** — read from `second-brain/inbox/watch-list.md` (one URL per line) and attempt to fetch/archive each
>
> For each source, create:
> - A standalone Python script (Python 3.10+) that performs the fetch and writes output as markdown to `raw/YYYY-MM-DD-[source]-[slug].md`
> - A frontmatter block with: source, date, type, url
> - A requirements.txt with all dependencies
>
> Then provide the exact crontab entries (or launchd plist for macOS) to schedule each script at 7am daily.
>
> Also create a `second-brain/wiki/routines.md` file listing all active automations, their schedule, what they collect, and the script path — so I can audit the system at a glance.

---

#### Prompt 6: Build a "What topics haven't I covered?" query system
*Replicates the killer demo from the video — letting Claude analyse your content archive and surface content gaps against trending topics.*

> I have an Obsidian second-brain vault at `~/second-brain/` containing markdown files about YouTube videos I've published (in `wiki/entities/`), AI topics I've covered (in `wiki/concepts/`), and summaries of AI news/papers (in `wiki/summaries/`).
>
> Write a Python script called `content-gap-analysis.py` that:
> 1. Reads all files in `wiki/entities/` that represent YouTube videos (identify them by frontmatter `type: youtube-video`)
> 2. Extracts all topics/tags mentioned across those files
> 3. Reads all files in `wiki/summaries/` and `wiki/concepts/` to build a list of topics that exist in the knowledge base but have NOT been covered in a video
> 4. Outputs a ranked markdown report saved to `doctrine/content-gaps-YYYY-MM-DD.md` listing: uncovered topics, how many source documents reference them, and suggested video angle
>
> Also write the Claude Code prompt to run this analysis conversationally — where I can just ask: "What topics haven't I covered that are trending in my second brain?" and Claude will read the vault files, cross-reference them, and produce the gap analysis without running an external script.
>
> Include instructions for how to structure video entity files (frontmatter fields: title, published-date, topics, views, type) so future ingestion is compatible with this analysis.

---

#### Prompt 7: Create a voice-capture inbox pipeline
*Sets up a frictionless way to dump ideas into the second brain from your phone or desktop using voice, so nothing is lost.*

> I want to add voice capture to my Obsidian second-brain at `~/second-brain/inbox/`. When I record a voice note (as an .m4a or .mp3 file dropped into a watched folder), it should automatically: transcribe the audio, save the transcript as a new inbox markdown file with today's date, and queue it for Claude to process into the wiki.
>
> Build this pipeline:
> 1. A Python script `voice-watcher.py` that watches `~/second-brain/inbox/audio/` for new audio files using the `watchdog` library
> 2. On new file detection: transcribe using OpenAI Whisper API (model: whisper-1) or local `whisper` CLI if API key not set
> 3. Save transcript to `~/second-brain/inbox/YYYY-MM-DD-voice-[slug].md` with frontmatter: source: voice, date, original-file path, status: unprocessed
> 4. Append the filename to `~/second-brain/wiki/log.md`
>
> Then write the Claude Code slash-command style prompt I can run each morning: "Process all unprocessed items in inbox/ — summarise each, extract entities and concepts, add to wiki, update their frontmatter status to 'processed'."
>
> Include a `requirements.txt` and setup instructions. Target Python 3.10+, macOS/Linux compatible.

---

### Links & Resources

- [Obsidian](https://obsidian.md) — Free local-first markdown note-taking app
- [Claude Code Desktop](https://claude.ai/code) — Claude's desktop coding/agent interface
- [Wes Roth YouTube Channel](https://www.youtube.com/@WesRoth) — Source channel
- [Original Video](https://www.youtube.com/watch?v=cwf2vEAigKA) — "Claude Built the Ultimate Second Brain"
- [Andrej Karpathy's LLM Wiki concept](https://twitter.com/karpathy) — The inspiration behind the system
- [Obsidian Dataview Plugin](https://github.com/blacksmithgu/obsidian-dataview) — Enables dynamic tables and queries inside Obsidian
- [Obsidian Kanban Plugin](https://github.com/mgmeyers/obsidian-kanban) — Enables drag-and-drop Kanban boards in Obsidian
- [Vannevar Bush — "As We May Think" (1945)](https://www.theatlantic.com/magazine/archive/1945/07/as-we-may-think/303881/) — Original Memex concept article
- [Getting Things Done (GTD)](https://gettingthingsdone.com) — David Allen's productivity system, a predecessor concept
- [Fireship YouTube Channel](https://www.youtube.com/@Fireship) — Referenced in the video

---

### Tags
`#second-brain` `#obsidian` `#knowledge-management` `#claude-code` `#automation` `#pkm`

---

### Category
Knowledge Management

---

*Extracted by [Co-Ord Executor](https://github.com/onekiller89/Co-Ord_Executor)*
