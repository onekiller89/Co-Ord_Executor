"""AI-powered content processor using Claude API for insight extraction."""

import anthropic

import config
from extractors.base import ExtractionResult


SYSTEM_PROMPT = """\
You are Co-Ord Executor — an AI assistant that transforms raw content extractions into \
structured, actionable knowledge documents.

Your job is to analyse the extracted content and produce a structured output with these \
exact sections. Be thorough but concise. Focus on what is genuinely valuable and actionable.

## Output format (follow exactly):

### Summary
2-4 sentences capturing the core value of this content.

### Key Insights
Bullet list of the most important takeaways. Each insight should be self-contained and \
useful on its own. Aim for 3-8 insights.

### Actions
A checklist of concrete, specific things the reader can do to implement or benefit from \
this content. Each action should be a clear next step, not vague advice. \
Use "- [ ]" checkbox format.

### Implementation Prompts
Ready-to-use prompts that can be pasted directly into an AI assistant (like Claude Code) \
to implement the actions above. Each prompt should be specific, self-contained, and \
produce a useful result. Format each as a blockquote.

### Links & Resources
All URLs, tools, libraries, repos, and resources mentioned or referenced. \
Format as markdown links. Include the original source URL.

### Tags
Suggest 3-6 lowercase tags for categorisation. Format as: `#tag1` `#tag2` `#tag3`

### Category
Suggest ONE primary category from: AI/ML, Development, DevOps, Productivity, \
Claude Code, Security, Design, Career, Business, Open Source, Other.

## Context-awareness rules:
- If the content relates to Claude, Claude Code, Anthropic, MCP, or similar: \
  tailor the Implementation Prompts specifically for Claude Code CLI usage. \
  Reference Claude Code features like slash commands, MCP servers, CLAUDE.md, hooks, etc.
- If the content relates to AI coding assistants generally (Cursor, Copilot, Windsurf, \
  Cline, Aider, OpenClaw, etc.): note how concepts can be adapted for Claude Code.
- If the content is about a specific tool/framework: make the Actions about setting it up \
  and trying it, and the prompts about implementing it.
- If the content is educational/conceptual: make the Actions about applying the knowledge \
  and the prompts about building something with it.

Be practical. The reader will pick this up later on their desktop to implement. \
Make everything as copy-paste-ready as possible."""


def process_extraction(result: ExtractionResult) -> str:
    """Process an extraction result through Claude to generate structured output.

    Returns the AI-generated structured content as a string.
    """
    if not config.ANTHROPIC_API_KEY:
        return _fallback_processing(result)

    client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)

    user_message = f"""\
Source type: {result.source_type}
URL: {result.url}
Title: {result.title}

--- Extracted content ---
{result.raw_content}
--- End of content ---

Analyse this content and produce the structured output as specified."""

    response = client.messages.create(
        model=config.CLAUDE_MODEL,
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )

    return response.content[0].text


def _fallback_processing(result: ExtractionResult) -> str:
    """Basic processing when no AI API key is available."""
    lines = result.raw_content.split("\n")
    # Extract any URLs from content
    links = []
    for line in lines:
        if "http://" in line or "https://" in line:
            links.append(line.strip())

    return f"""\
### Summary
Content extracted from {result.source_type}: {result.title}

> **Note:** No Anthropic API key configured. This is a raw extraction without AI processing.
> Set ANTHROPIC_API_KEY in your .env file for full insight extraction.

### Key Insights
- Review the raw content below for insights.

### Actions
- [ ] Review this extraction and manually identify action items
- [ ] Set up ANTHROPIC_API_KEY for automatic AI processing

### Implementation Prompts
> No AI processing available. Configure your API key to enable this feature.

### Links & Resources
- [Original source]({result.url})
{chr(10).join(f"- {link}" for link in links[:10])}

### Tags
`#{result.source_type.lower().replace("/", "-")}` `#needs-review`

### Category
Other

---

### Raw Content
{result.raw_content[:5000]}"""
