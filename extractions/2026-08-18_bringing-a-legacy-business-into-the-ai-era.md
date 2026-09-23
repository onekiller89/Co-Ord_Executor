![banner](https://img.youtube.com/vi/ra9Tcadk824/maxresdefault.jpg)

# Bringing a Legacy Business into the AI Era

> **Source:** YouTube | **Extracted:** 2026-08-18 23:35 UTC | **Method:** youtube_transcript_api
> **URL:** https://www.youtube.com/watch?v=ra9Tcadk824

---

### Summary
Ido Seagal, a serial AI entrepreneur now leading Napster's AI-era revival, shares hard-won lessons from deploying AI (specifically Claude Code) across a ~200-person organisation. He documents a dramatic productivity transformation — 1 engineer doing the work of 20 after a week of intensive Claude Code adoption — and argues that the real AI ROI moment arrived at end of 2025/early 2026. The core message: the winning strategy is amplifying people to do exponentially more, not cutting headcount.

---

### Key Insights

- **The "orange pill" moment is now** — Ido argues Claude Code (Opus 4.6) represents a shift as significant as ChatGPT's launch, and that the real utility arrived at end-of-2025/early-2026. Previous AI adoption felt like "parlour tricks"; this is now genuinely transformative.
- **1 engineer = 20 engineers productivity** — After a hands-on week in India with 20 software engineers using Claude Code Max ($100/month/person), each engineer could produce what previously took the whole team a month. This is empirical, not marketing.
- **Lead AI transformation by example, not mandate** — Forcing tool adoption (e.g., Copilot 3-4 years ago) failed. What works is sitting with your team, demonstrating live results, and letting them experience the output personally. Flying to India for 10 days was the move.
- **Amplification > automation** — CEOs focused on cutting headcount with AI are entering a death spiral. If all competitors use the same commodity AI and you've fired everyone, you have no differentiation. The winning bet is doing exponentially *more* with your existing people.
- **The key muscle is "imagining you can ask for outrageous things"** — Most people self-limit. The primary skill isn't coding or prompting syntax — it's developing the mindset to ask AI for things that seem impossible. That's the actual bottleneck.
- **Synthetic chief of staff is viable today** — Ido's AI chief of staff "Jane" reads his email, Slack, and WhatsApp, prioritises relationships, and produced a 120-page CIA-style intelligence briefing for a trade show — all via conversational Claude Code, no code written manually.
- **AI will become a utility like electricity** — When Claude goes down, it will feel like AWS going down. Competitive, open markets for AI providers are therefore critical infrastructure concerns, not just business preferences.
- **Hire young, uncorrupted talent** — New hires who grew up with AI don't have legacy mental models to overcome. They treat AI like a refrigerator — obviously useful, not impressive — and that's an asset.

---

### Actions

- [ ] Sign up for Claude Max plan ($100/month) and run Claude Code for at least one full week before evaluating it
- [ ] Identify your 5-20 most technical team members and run an immersive, in-person AI adoption sprint — sit with them daily for a week, lead by example
- [ ] Download the Claude desktop app (not just the web version) and explore the Chat / Co-work / Code tabs to understand what's available beyond basic chat
- [ ] Install the Claude browser extension to enable Claude Code to control your browser for research and automation tasks
- [ ] Define ONE ambitious workflow (e.g., pre-meeting intelligence briefing, competitive analysis, onboarding docs) and attempt it entirely through conversational Claude Code — no manual coding
- [ ] Audit your current AI spend vs. productivity gains: are you paying ~$100/person/month? Calculate the ROI using actual output metrics, not sentiment surveys
- [ ] Read Ido's "orange pill" essay on LinkedIn (link via QR in the video or direct message to Ido Seagal on LinkedIn)
- [ ] For business functions (sales, marketing, CS): identify one repetitive, research-heavy task per team and pilot a Claude Code automation this quarter
- [ ] Evaluate whether your AI transformation is being led by demonstration or by decree — if the latter, change the approach

---

### Implementation Prompts

#### Prompt 1: Build a Pre-Meeting Intelligence Briefing (CIA-Style)
*Replicates Ido's trade show preparation workflow — turning a LinkedIn group photo or attendee list into a prioritised, actionable relationship dossier. Massive leverage for any sales, BD, or executive team.*

> You are acting as my chief of staff. I'm preparing for [EVENT NAME] on [DATE]. I have a list of attendees / a LinkedIn screenshot of key people I'll be meeting.
>
> Here is the attendee list / image: [PASTE LIST OR DROP IMAGE]
>
> For each person:
> 1. Research their LinkedIn profile (use browser tools if available)
> 2. Identify their role, company, key accounts they manage, and recent public activity
> 3. Rate their strategic importance to me on a scale of 1–10 with a one-sentence justification
> 4. Write a personalised draft follow-up email I can send after meeting them
> 5. Note one specific talking point or shared interest I can use to open conversation
>
> My company does: [2-3 sentence description of your company and what you're trying to achieve at this event]
>
> Output: A structured report — one page per person — sorted by strategic priority (highest first), plus a summary spreadsheet with columns: Name | Company | Role | Priority Score | Key Accounts | Talking Point | Follow-up Status.

---

#### Prompt 2: Set Up a Synthetic Chief of Staff (Jane-Style Agent)
*Creates a personalised AI chief of staff that understands your context, communication style, and priorities — so it can triage information and surface what matters.*

> I want to set up a persistent AI chief of staff to help me manage my communications and priorities. Help me build the context file and operating instructions for this agent.
>
> Ask me the following in sequence, then compile the answers into a structured CLAUDE.md or system prompt I can reuse:
> 1. What are my top 3 strategic priorities this quarter?
> 2. Who are the 10 most important people I communicate with and why?
> 3. What communication channels do I use (email, Slack, WhatsApp, etc.)?
> 4. What does a "high priority" item look like vs. a "low priority" one for me?
> 5. What are my recurring weekly commitments and deadlines?
> 6. What decisions do I always want to be flagged on immediately?
>
> Then produce:
> - A system prompt / CLAUDE.md file I can paste into Claude Projects or Claude Code
> - A daily briefing template the agent should fill in each morning
> - A triage rubric: Urgent + Important / Important / Delegate / Ignore

---

#### Prompt 3: Run a 1-Week AI Adoption Sprint Plan for an Engineering Team
*Structures the exact type of immersive, in-person week Ido ran in India — giving leaders a day-by-day agenda to coach their team from near-zero to genuine Claude Code proficiency.*

> I'm planning a 5-day intensive AI adoption sprint for a team of [NUMBER] software engineers. The goal is to get each engineer from minimal Claude Code usage to being able to independently run complex, multi-step agentic workflows by end of the week.
>
> Current team proficiency level: [beginner / some ChatGPT use / familiar with Copilot]
> Tech stack: [e.g., Python, React, Node, etc.]
> Key projects we're working on: [brief description]
>
> Create a detailed day-by-day agenda including:
> - Day 1: Setup, orientation, and first "wow moment" exercise
> - Day 2: Core workflow automation (real tasks from our codebase)
> - Day 3: Multi-step agentic tasks and browser automation
> - Day 4: Team-specific deep dives — each engineer picks their highest-leverage use case
> - Day 5: Showcase, retrospective, and ongoing habit-building plan
>
> Also provide:
> - A list of 5 "starter tasks" that reliably produce dramatic results for engineers new to Claude Code
> - A measurement framework: how do we track before/after productivity?
> - Common failure modes to avoid during the week

---

#### Prompt 4: Calculate and Present AI ROI to Leadership
*Turns empirical productivity observations into a CFO-ready business case — bridging the gap between "it feels faster" and budget approval for scaling AI tools.*

> Help me build a concrete AI ROI analysis to present to my leadership / CFO / board.
>
> Context:
> - Team size: [NUMBER] people in [FUNCTION, e.g., engineering / sales / support]
> - Current AI tool spend: $[AMOUNT] per month per person on [TOOLS]
> - Observed productivity improvement: [e.g., "tasks that took a week now take a day"]
> - Average fully-loaded employee cost: $[AMOUNT] per year
>
> Build me:
> 1. A simple ROI calculation: cost of AI tools vs. value of productivity gained (in $ equivalent)
> 2. A 12-month projection showing cumulative value if we scale from [X] to [Y] users
> 3. A risk-adjusted version (conservative / base / optimistic scenarios)
> 4. A one-page executive summary I can present in a 5-minute slot
> 5. Answers to the top 3 objections a skeptical CFO will raise
>
> Make all numbers transparent and auditable — show your assumptions clearly so I can adjust them.

---

#### Prompt 5: Design a "Claude Code Imagination Muscle" Training Exercise
*Addresses the core bottleneck Ido identifies — most people don't ask for ambitious enough tasks. This prompt generates exercises that specifically train the mindset shift.*

> The biggest barrier to AI adoption isn't technical skill — it's that people don't believe they can ask for ambitious things. I want to design a workshop exercise that specifically trains this "imagination muscle."
>
> My audience: [e.g., sales managers / marketing team / customer success / mixed business functions]
> Duration available: [e.g., 2 hours]
> Their current AI usage: [e.g., summarising emails, basic Q&A]
>
> Design a structured exercise that:
> 1. Starts with what they currently ask AI to do (baseline)
> 2. Uses a "10x ask" framework — for every task, challenge them to ask for something 10x more ambitious
> 3. Includes 5 specific example transformations: [timid ask] → [ambitious ask] relevant to their role
> 4. Has a live demo component where they attempt one ambitious task in real-time and see the result
> 5. Ends with each participant committing to one "outrageous ask" to try this week
>
> Also write the facilitator script for the key "permission-giving" moment where participants realise they've been self-limiting.

---

#### Prompt 6: Audit Your Current AI Adoption Strategy — Amplification vs. Automation
*Helps leaders identify whether their AI strategy is accidentally heading toward the "death spiral" Ido describes (headcount cuts + commodity AI = no differentiation).*

> I want to audit my company's current AI strategy to determine whether we're on an amplification path (doing more with our people) or an automation/replacement path (cutting costs by replacing people).
>
> Our company: [brief description, size, industry]
> Current AI initiatives: [list what you're doing with AI today]
> Recent decisions made citing AI: [e.g., headcount freezes, role eliminations, new hires, new products]
>
> Analyse our current trajectory and provide:
> 1. A diagnostic: are we amplification-first or automation-first? Evidence for your assessment.
> 2. The strategic risk of our current path (especially if we're automation-first)
> 3. Three specific pivots we could make in the next 90 days to shift toward amplification
> 4. New products, services, or capabilities we could unlock if each employee was 10x more productive
> 5. A one-paragraph "north star" AI strategy statement I can use to align the leadership team

---

### Links & Resources

- [Original Video — "Bringing a Legacy Business into the AI Era" (AI:ROI / Section)](https://www.youtube.com/watch?v=ra9Tcadk824)
- [Ido Seagal on LinkedIn](https://www.linkedin.com/in/idoseagal/) *(search for his "orange pill" essay)*
- [Claude Code (Anthropic)](https://claude.ai/code)
- [Claude Desktop App (Mac)](https://claude.ai/download)
- [Claude Max Plan — $100/month](https://claude.ai/upgrade)
- [Napster (AI-era version)](https://napster.com)
- [Section — AI:ROI Conversations](https://www.sectionschool.com)

---

### Tags
`#ai-adoption` `#ai-roi` `#claude-code` `#leadership` `#productivity` `#enterprise-ai`

---

### Category
AI Transformation Leadership

---

*Extracted by [Co-Ord Executor](https://github.com/onekiller89/Co-Ord_Executor)*
