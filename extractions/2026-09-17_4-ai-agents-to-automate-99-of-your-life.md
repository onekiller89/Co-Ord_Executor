![banner](https://img.youtube.com/vi/TL8V41Ea6oM/maxresdefault.jpg)

# 4 AI Agents To Automate 99% Of Your Life

> **Source:** YouTube | **Extracted:** 2026-09-17 11:08 UTC | **Method:** youtube_transcript_api
> **URL:** https://www.youtube.com/watch?v=TL8V41Ea6oM

---

### Summary
This video presents a practical framework for building four AI agents using the "Four C's" system: Coordination, Creativity, Clarity, and Coaching. The author — a 20-year CEO/investor — walks through step-by-step agent builds using Claude (with Gmail/Calendar integration), focusing on a key philosophy: make work visible first, then efficient, then automatic. No coding is required; plain English prompts are sufficient.

---

### Key Insights

- **The Five-Part Prompt Skeleton works universally**: Every effective agent prompt contains: (1) the job, (2) the tool, (3) the categories, (4) the output, and (5) the boundary. This structure works across Claude, ChatGPT, and Gemini.
- **Delegate incrementally, not immediately**: The golden rule is make work *visible* → make it *efficient* → make it *automatic* → *then* delegate. Skipping steps leads to misplaced trust in agent outputs.
- **Agents run on ReAct loops**: Under the hood, every agent follows Reason → Act → Observe → Reason again. Understanding this helps you write better prompts and debug bad outputs.
- **Telescope vs. Microscope for document analysis**: Use "telescope" mode to aggregate scattered intel across the web, emails, and files. Use "microscope" mode to dissect a single dense document — extracting obligations, risks, jargon, and hidden liabilities into a structured table.
- **Voice mode transforms the coaching agent**: Speaking your rehearsal answers out loud (via Claude/ChatGPT/Gemini voice mode) is more valuable than typing — it replicates real-world pressure and reveals where you fumble.
- **Cross-verify AI outputs across engines**: Use Claude, Gemini, and ChatGPT as an "advisory board" — run research through one, then verify with another. Disagreement between them is a signal to dig deeper.
- **Skills = reusable agent capabilities**: Claude's built-in skills (PowerPoint, Word, Excel, PDF) produce real editable files. You can encode your brand template as a custom skill so every output matches your style automatically.
- **"If you come in confused, AI multiplies the confusion"**: Clarity of input determines quality of output. Experimentation and iteration are how you build the intuition to get what you want.

---

### Actions

- [ ] Sign up for Claude and switch to "Co-work" (task) mode to begin building agents
- [ ] Connect Gmail via the plus menu → Connectors → Add Connectors → Gmail
- [ ] Write your first email agent prompt using the five-part skeleton: job, tool, categories, output, boundary — with explicit "don't send without approval" boundary
- [ ] After trusting email output for a few days, add Google Calendar and write the combined coordination prompt
- [ ] Schedule the coordination agent to run every morning automatically using the Schedule tab
- [ ] Build the creativity agent by pointing it to a local folder of rough notes and specifying the output format, audience, length, and voice
- [ ] Upload a brand deck and ask Claude to convert it into a reusable style skill
- [ ] Build a clarity agent for an upcoming contract: use the 5-column table prompt (what it says / plain English / why it matters / risk level / questions to ask)
- [ ] Set up a coaching agent with your resume, job description, and a specific hiring manager persona — then use voice mode on your phone to practice out loud
- [ ] After coaching session, explicitly break character and ask for a debrief: weaknesses, fumbles, better answers, a one-page prep card
- [ ] Cross-verify any important AI research output by running it through a second AI engine (Claude → Gemini, or vice versa)

---

### Implementation Prompts

#### Prompt 1: Email Coordination Agent
*Builds the core daily inbox triage agent. Saves time by surfacing urgent items and drafting context-aware replies — without auto-sending anything.*

> You are my email coordination assistant with access to my Gmail inbox. Review all unread emails from the last 24 hours. Sort them into three buckets:
> 1. **Urgent** – requires my action or response today
> 2. **Informational** – good to know but no action needed
> 3. **Ignore** – newsletters, promotions, automated notifications
>
> For each Urgent email: draft a reply that sounds like me — professional but direct, no fluff. Include the recipient name and subject in your draft header.
>
> Output format: a numbered list per bucket, with sender, subject, one-sentence summary, and (for Urgent) the draft reply below it.
>
> **Boundary**: Do NOT send any emails. Present all drafts for my approval first.

---

#### Prompt 2: Email + Calendar Coordination Sync
*Combines inbox urgency with your calendar to surface conflicts, prep requirements, and scheduling gaps — your morning briefing in one run.*

> You have access to my Gmail and Google Calendar. Do the following:
>
> 1. Pull all urgent emails from the last 24 hours (use your email triage results if already run).
> 2. Pull today's and tomorrow's calendar events.
> 3. Cross-reference them and tell me:
>    - **Conflicts**: any email requiring action that clashes with a meeting block
>    - **Prep needed**: meetings that require documents, context, or decisions based on recent emails
>    - **Can wait**: items with no time pressure in the next 48 hours
>
> Output as three clearly labelled sections. Be concise. Flag anything that needs my decision today.
>
> **Boundary**: Do not reschedule, decline, or modify any calendar events. Show me the analysis only.

---

#### Prompt 3: Creativity Agent — Pitch Deck Builder
*Turns messy notes into a structured, editable PowerPoint file. The agent asks clarifying questions before building, so the output is actually useful.*

> I'm going to give you my rough notes on an idea I want to pitch. Your job is to turn them into a presentation deck.
>
> **My notes**: [paste your notes here]
>
> **Target audience**: [e.g., CFO, investors, board members]
> **Deck length**: 8–10 slides
> **Presentation time**: 15 minutes
> **Tone**: [e.g., confident, data-driven, conversational]
>
> Before you build anything: ask me up to 5 clarifying questions if you see gaps in the notes. Once I answer, build the full deck as a PowerPoint (.pptx) file saved to my folder.
>
> Structure suggestion: Problem → Insight → Solution → Evidence → Ask → Next Steps.
> Make the opening slide punchy. Keep bullets to 3 per slide max.

---

#### Prompt 4: Brand Style Skill Setup
*Encodes your visual brand into a reusable agent skill so every future document or deck automatically matches your colours, fonts, and layout.*

> I'm uploading a sample presentation that represents my brand style. Analyse it carefully and extract the following:
>
> - Primary and secondary colours (with hex codes if possible)
> - Font names and sizes used for headings, body, and captions
> - Slide layout patterns (e.g., title left, image right; full-bleed header, etc.)
> - Spacing and padding conventions
> - Any recurring design elements (icons, dividers, logo placement)
>
> Then create a **Brand Style Skill document** I can reference in future prompts. Format it as a reusable instruction block I can paste at the top of any creativity agent prompt to ensure consistent styling across all future decks and documents.

---

#### Prompt 5: Clarity Agent — Contract Microscope
*Breaks open a complex legal or financial document into plain English, surfacing obligations, risks, and the questions you should be asking before signing.*

> I'm uploading a document (contract / policy / report). Read it carefully and completely — do not skim or summarise at a high level.
>
> Extract and analyse the following key elements: fee structure, obligations, deadlines, exclusivity clauses, termination conditions, liability terms, and anything that seems unusual or one-sided.
>
> Present your findings as a **table with 5 columns**:
> | What the document says | Plain English meaning | Why it matters | Risk level (Low/Med/High) | Questions I should ask |
>
> After the table, give me:
> - Your top 3 red flags
> - The single most important clause I should negotiate or clarify before signing
>
> **Boundary**: Do not give legal advice. Flag issues for my lawyer's review.

---

#### Prompt 6: Telescope Research Agent — Company Deep Dive
*Aggregates web, email, news, and document intelligence on a counterparty before a deal, meeting, or negotiation — so you walk in informed.*

> I'm about to [sign a deal with / meet with / negotiate with] **[Company Name]**. I need a full intelligence picture before I proceed.
>
> Do the following in order:
> 1. Search the web for who they are — founding story, business model, leadership team, recent news, funding, controversies
> 2. Search my connected emails for any past correspondence with them — summarise the relationship history and any commitments made
> 3. Research their core product and competitive positioning from reliable sources
> 4. Flag anything that seems like a risk, a red flag, or a mismatch with what they've told me
>
> Output: one consolidated briefing document saved to my folder, with sources cited for all web claims.
> Include a section called **"Things to verify"** for anything uncertain.
> Be concise. Use headers. No fluff.

---

#### Prompt 7: Coaching Agent — Interview Rehearsal Setup
*Creates a realistic, adaptive interview simulation with a specific hiring manager persona, tracks your responses, and delivers a structured debrief at the end.*

> I'm preparing for a job interview. Here is my context:
>
> - **Company**: [Company Name + 2-sentence description]
> - **Role**: [Job title + key responsibilities]
> - **Job description**: [paste or upload]
> - **My resume**: [paste or upload]
> - **My cover letter / position statement**: [paste or summarise]
>
> You are the hiring manager for this role. You are [sharp / sceptical / data-driven — pick one or describe]. You've read my resume. Begin the interview now.
>
> **Rules**:
> - Ask one question at a time
> - Push back on weak or vague answers like a real interviewer would
> - Do not break character until I say "Interview complete"
> - Track the full conversation so we can review it after
>
> When I say "Interview complete", switch to **coach mode**: tell me where I was weak, where I fumbled, what I should have said differently, where I rambled, and give me 3 improved versions of my weakest answer. Then produce a one-page prep card I can review before the real interview.

---

#### Prompt 8: Cross-Verification Advisory Board Check
*Sends a key research output or claim to a second AI engine for independent verification — your "advisory board" safety net for high-stakes decisions.*

> I've received the following research/analysis from another AI:
>
> [paste the output here]
>
> Your job is to act as an independent reviewer. Do the following:
> 1. Identify any claims that are **unverified, overstated, or potentially outdated**
> 2. Flag any **gaps** — important angles or data points that were missed
> 3. Note anywhere the original analysis seems **biased or one-sided**
> 4. Add any **new information** you have that changes or nuances the picture
> 5. Give me a **confidence rating** (High / Medium / Low) on the overall reliability of the original output
>
> Be direct. I'm using this to make a real decision.

---

### Links & Resources

- [Video: 4 AI Agents To Automate 99% Of Your Life](https://www.youtube.com/watch?v=TL8V41Ea6oM)
- [Claude by Anthropic](https://claude.ai) — primary tool used in the walkthrough
- [Claude Co-work / Tasks mode](https://claude.ai) — agent-building interface (vs. standard chat)
- [ChatGPT](https://chat.openai.com) — alternative agent platform
- [Google Gemini](https://gemini.google.com) — alternative agent platform
- [ReAct framework (Reason + Act)](https://arxiv.org/abs/2210.03629) — the underlying loop powering AI agents
- [Charlie Chaplin — Modern Times (1936)](https://en.wikipedia.org/wiki/Modern_Times_(film)) — referenced in closing analogy
- Sandeep Swadia's newsletter — linked below the video (check YouTube description)

---

### Tags
`#ai-agents` `#productivity` `#automation` `#prompt-engineering` `#no-code`

### Category
AI Agents

---

*Extracted by [MegaMind](https://github.com/onekiller89/MegaMind)*
