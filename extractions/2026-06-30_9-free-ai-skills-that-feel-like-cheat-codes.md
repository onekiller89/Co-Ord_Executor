![banner](https://img.youtube.com/vi/STH929HARLo/maxresdefault.jpg)

# 9 Free AI Skills That Feel Like Cheat Codes

> **Source:** YouTube | **Extracted:** 2026-07-01 10:32 UTC | **Method:** youtube_transcript_api
> **URL:** https://www.youtube.com/watch?v=STH929HARLo

---

### Summary
Matt Wolfe walks through 9 free AI skills and plugins that can be installed into any agent harness (Claude Code, OpenAI Codex, Cursor, Open Claw, VS Code Copilot, etc.) via a simple GitHub URL install command. Skills are reusable `.md` prompt files that give agents consistent, repeatable behaviours; plugins bundle skills with MCPs, hooks, and agents. The video covers tools spanning code review, writing cleanup, knowledge graphing, real-time research, frontend design, and programmatic animation generation.

### Key Insights
- **Skills vs Plugins**: A skill is a single dialled-in prompt file (`.md`) that gives the model a repeatable behaviour. A plugin is a bundle of skills + agents + MCPs + hooks — installed the same way but delivers more.
- **Universal install method**: Simply paste the GitHub URL into your agent harness chat and say "install this for me" — works across Claude Code, Codex, Cursor, Open Claw, Hermes, VS Code, and Copilot.
- **G-Stack (Garry Tan / YC)**: 23 specialist roles + 8 slash-command power tools that turn your agent into a virtual engineering team (CEO, EM, designer, reviewer, QA lead, security auditor, release engineer).
- **Graphify**: Converts codebases, docs, or second-brain notes into a queryable JSON knowledge graph + visual HTML — acts as a memory layer that dramatically reduces token usage on repeated queries.
- **Understand Anything**: Similar to Graphify but optimised for human + agent onboarding — produces interactive flowchart-style visuals showing how code components connect.
- **Last 30 Days**: Synthesises current internet sentiment across Reddit, X, YouTube, Hacker News, Polymarket, and GitHub into a structured report with an exportable HTML file.
- **Animation skills (Remotion + Hyperframes)**: Generate After Effects-style MP4 animations (logo reveals, stock charts, iPhone text conversations) from a single prompt — Hyperframes (by HeyGen) tended to produce slightly more polished output.
- **Design skills (Anthropic Frontend Design + Taste)**: Two complementary skills that push the model toward less generic, more aesthetically intentional UI — useful to run solo or combined for multiple design variations.
- **Stop Slop**: Lightweight skill that removes AI writing "tells" from any paragraph — useful for blog posts, scripts, or any AI-assisted writing.

### Actions
- [ ] Bookmark the `skills.sh` website to browse and discover new community skills
- [ ] Install **G-Stack** (`github.com/garytan/gstack`) and run `/gstack office-hours` on your next project idea to stress-test it before building
- [ ] Install **Stop Slop** and run it on any AI-generated copy before publishing
- [ ] Install **Graphify** and run `/graphify .` on an existing codebase or notes folder to generate a knowledge graph memory layer
- [ ] Install **Understand Anything** on a codebase you're onboarding to — share the HTML output with collaborators
- [ ] Install **Last 30 Days** and use it to research competitor tools or trending topics before creating content or building features
- [ ] Install both **Anthropic Frontend Design** and **Taste** skills, then generate 3 design variants of your next UI before committing to one
- [ ] Install **Remotion** and **Hyperframes** and test both on the same animation prompt to compare output quality
- [ ] For any new skill install: paste the raw GitHub URL into your agent chat with the message "install this for me please" — no manual file copying needed
- [ ] After installing G-Stack, follow Garry's recommended starter sequence: office hours → plan/CEO review → review → QA

### Implementation Prompts

#### Prompt 1: Install G-Stack and run an office hours stress test
*Installs the full G-Stack plugin bundle and immediately puts it to work validating a product idea — the fastest way to pressure-test a concept before writing a single line of code.*
> I want to install and use the G-Stack plugin by Garry Tan (Y Combinator). First, install it from this GitHub repo: https://github.com/garytan/gstack — follow whatever install process is appropriate for this environment (copy skill files to `.claude/skills/` or equivalent). Once installed, run the `/gstack office-hours` skill with the following brief: "I want to build [DESCRIBE YOUR APP IDEA IN 1-2 SENTENCES]. Help me pressure test this idea before I build it — challenge my assumptions, identify risks, and ask me the hard questions a YC partner would ask." Keep asking follow-up questions until you've written a concise product brief as a markdown file called `idea-brief.md`.

#### Prompt 2: Install Stop Slop and clean up AI-generated copy
*Removes generic AI "tells" from any written content — essential for blog posts, scripts, product descriptions, or any public-facing copy drafted with AI assistance.*
> Install the Stop Slop skill from this GitHub repo: https://github.com/cgbur/stop-slop — place the skill file in the appropriate skills directory for this environment. Once installed, apply the Stop Slop skill to the following paragraph and rewrite it to sound like a specific, confident human voice — remove filler phrases, hedging language, em-dash overuse, and any phrasing that pattern-matches to generic AI output. Return only the rewritten paragraph with a brief note on what was changed: [PASTE YOUR AI-GENERATED PARAGRAPH HERE]

#### Prompt 3: Run Graphify on a codebase or notes folder to build a knowledge graph
*Creates a queryable JSON knowledge graph + interactive HTML visualisation of any codebase or markdown notes folder — dramatically reduces token costs on repeated queries by using the graph as a memory layer instead of re-reading all files.*
> Install the Graphify skill from: https://github.com/helrabelo/graphify — place skill files in the correct skills directory. Then run `/graphify .` on the current project folder. After the graph is generated: 1) Open the resulting `graph.html` file and confirm the visualisation renders. 2) Query the graph (without re-reading source files) to answer: "What are the 5 biggest recurring themes or architectural patterns in this project?" 3) Query again: "What are 3 things that look underconnected or isolated that might be worth investigating?" Save all findings to `graphify-insights.md`.

#### Prompt 4: Run Understand Anything for developer onboarding documentation
*Generates an interactive flowchart-style knowledge map of a codebase — ideal for onboarding new developers or getting a high-level architectural overview without reading every file.*
> Install the Understand Anything skill from: https://github.com/the-horizon-team/understand-anything — place it in the correct skills directory for this environment. Then run `/understand .` on the current project. Once complete: 1) Describe the top-level architecture in plain English as if explaining to a new hire. 2) Identify the 3 most critical entry points a new developer should study first. 3) Flag any areas of the codebase that appear overly complex or poorly connected. Save the output as `onboarding-guide.md` alongside the generated HTML visualisation.

#### Prompt 5: Use Last 30 Days to research internet sentiment on a topic
*Synthesises current Reddit, YouTube, Hacker News, GitHub, X, and Polymarket content into a structured sentiment report — useful for competitive research, content planning, or validating market interest before building.*
> Install the Last 30 Days skill from: https://github.com/mcp-mirror/last30days (check the skills.sh site or Matt Wolfe's video description for the exact URL). Once installed, run the skill with this query: "Research [YOUR TOPIC — e.g. a tool name, trend, or competitor]. Find: 1) What people are most excited about, 2) What they're confused or frustrated by, 3) What they're speculating will happen next. Pull from Reddit, YouTube, Hacker News, GitHub, and X. Cite sources." After the research completes, generate a shareable HTML export file called `research-[topic]-[date].html` using the skill's built-in HTML export functionality.

#### Prompt 6: Generate frontend design variants using Anthropic Design + Taste skills
*Produces multiple aesthetically distinct UI redesigns of the same component by running two complementary design skills — gives you real options to choose from instead of accepting the first AI-generated design.*
> Install the Anthropic Frontend Design skill and the Taste (design taste frontend) skill. Anthropic's skill is available via the Claude skills directory; Taste is at: https://github.com/leoxa/taste (verify URL from skills.sh). Then, for the HTML/component file at [FILE PATH], generate THREE design variants: 1) Using only the Anthropic Frontend Design skill, 2) Using only the Taste skill, 3) Using both skills combined. Save each as a separate HTML file (`design-v1-anthropic.html`, `design-v2-taste.html`, `design-v3-combined.html`). For each variant, write 2 sentences explaining the design choices made.

#### Prompt 7: Create an animation using Remotion and Hyperframes for comparison
*Generates the same animation using two different skills so you can compare output quality — useful for logo reveals, data visualisations, explainer graphics, or social media content.*
> Install the Remotion best practices skill and the Hyperframes skill (by HeyGen). Remotion: https://github.com/remotion-dev/remotion-claude-skill — Hyperframes: check skills.sh or HeyGen's GitHub. Then create the following animation TWICE — once with each skill: "Create an animated bar chart showing [YOUR DATA — e.g. monthly revenue, user growth, or a fun dataset] over [TIME PERIOD]. The bars should animate in sequentially, include labelled axes, a title, and smooth easing. Export as MP4." Save outputs as `animation-remotion.mp4` and `animation-hyperframes.mp4`. Note which skill produced cleaner output and why.

#### Prompt 8: Run G-Stack code review on an existing branch
*Performs a senior-engineer-level code review using G-Stack's review specialist — catches bugs, edge cases, security issues, and UX problems that the base model alone often misses.*
> The G-Stack plugin should already be installed (if not, install from https://github.com/garytan/gstack). Run the `/gstack review` skill on the current working directory or the files changed in the current branch. Instruction: "Review the current changes like a senior engineer. Look for: 1) Bugs and logic errors, 2) Missed edge cases, 3) Security vulnerabilities (run OWASP and STRIDE checks where applicable), 4) UX problems visible from the code, 5) Technical debt or architectural concerns. For each issue found, provide: the file and line number, a description of the problem, severity (critical/high/medium/low), and a recommended fix." Output the full review as `code-review-[date].md`.

### Links & Resources
- [G-Stack by Garry Tan (YC)](https://github.com/garytan/gstack)
- [Stop Slop](https://github.com/cgbur/stop-slop) *(verify exact URL from video description)*
- [Graphify](https://github.com/helrabelo/graphify) *(verify exact URL from video description)*
- [Understand Anything](https://github.com/the-horizon-team/understand-anything) *(verify exact URL)*
- [Last 30 Days skill](https://github.com/) *(exact URL in Matt Wolfe's video description)*
- [Anthropic Frontend Design skill](https://skills.sh) *(#2 most popular on skills.sh)*
- [Taste (Design Taste Frontend) by Leon XLNX — ~50k GitHub stars](https://github.com/leoxa/taste) *(verify exact URL)*
- [Remotion](https://github.com/remotion-dev/remotion)
- [Hyperframes by HeyGen](https://github.com/HeyGen-Official/hyperframes) *(verify exact URL)*
- [skills.sh — skills discovery and organisation site](https://skills.sh)
- [Future Tools Newsletter](https://futuretools.io/newsletter)
- [Original YouTube Video](https://www.youtube.com/watch?v=STH929HARLo)

> ⚠️ **Note**: Several GitHub URLs above are best-guess inferences. The video states all links are in the description — verify exact URLs from [the video description](https://www.youtube.com/watch?v=STH929HARLo) before installing.

### Tags
`#ai-skills` `#claude-code` `#codex` `#agent-plugins` `#developer-tools` `#productivity`

### Category
Claude Code

---

*Extracted by [Co-Ord Executor](https://github.com/onekiller89/Co-Ord_Executor)*
