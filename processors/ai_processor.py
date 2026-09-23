"""AI-powered content processor using Claude API for insight extraction."""

import time
import re
import logging
import subprocess
import tempfile
from pathlib import Path

import anthropic

import config
from extractors.base import ExtractionResult

log = logging.getLogger("megamind.processor")


SYSTEM_PROMPT = (Path(__file__).resolve().parents[1] / "prompts" / "analysis-v2.md").read_text(encoding="utf-8").strip()


REQUIRED_SECTIONS = (
    "Summary",
    "Key Insights",
    "Actions",
    "Implementation Prompts",
    "Links & Resources",
    "Tags",
    "Category",
)


def process_extraction(result: ExtractionResult) -> str:
    """Use the selected model, falling back to Anthropic when Codex is unavailable."""
    if config.MODEL_PROVIDER == "codex":
        try:
            content = _process_codex(result)
            missing = _missing_required_sections(content)
            if missing:
                raise RuntimeError("Codex output missed required sections")
            result.metadata["analysis_model"] = config.CODEX_MODEL
            try:
                from budget import record_subscription_run
                record_subscription_run(config.CODEX_MODEL, result.title)
            except Exception:
                log.warning("Codex usage counter could not be saved")
            return content
        except (OSError, subprocess.SubprocessError, RuntimeError) as exc:
            log.warning("Codex analysis failed (%s); trying Anthropic fallback", type(exc).__name__)
            if not config.ANTHROPIC_API_KEY:
                raise
    elif config.MODEL_PROVIDER != "anthropic":
        raise ValueError(f"Unknown model provider: {config.MODEL_PROVIDER}")
    content = _process_anthropic(result)
    if config.ANTHROPIC_API_KEY:
        result.metadata["analysis_model"] = config.CLAUDE_MODEL
    return content


def _process_codex(result: ExtractionResult) -> str:
    """Run the already signed-in Codex CLI in an empty, read-only workspace."""
    prompt = (f"{SYSTEM_PROMPT}\n\nSource URL: {result.url}\nTitle: {result.title}\n"
              f"SOURCE CONTENT\n{result.raw_content}\nEND SOURCE\n\n"
              "Return only the seven Markdown sections. Do not use tools or inspect files; "
              "the complete source is above.")
    with tempfile.TemporaryDirectory(prefix="megamind-codex-") as workspace:
        output = Path(workspace) / "answer.md"
        completed = subprocess.run(
            [config.CODEX_CLI, "exec", "--ephemeral", "--ignore-user-config",
             "--skip-git-repo-check", "--sandbox", "read-only",
             "-c", "model_reasoning_effort=medium", "-m", config.CODEX_MODEL,
             "-o", str(output), "-"],
            input=prompt, text=True, cwd=workspace, capture_output=True, timeout=300,
        )
        if completed.returncode or not output.is_file():
            raise RuntimeError(f"Codex exited with code {completed.returncode}")
        return output.read_text(encoding="utf-8").strip()


def _process_anthropic(result: ExtractionResult) -> str:
    """Process an extraction through the Anthropic API, tracking its API cost."""
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

    max_retries = 4
    for attempt in range(max_retries + 1):
        try:
            response = client.messages.create(
                model=config.CLAUDE_MODEL,
                max_tokens=3200,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_message}],
            )
            break
        except anthropic.APIStatusError as e:
            if e.status_code == 529 and attempt < max_retries:
                wait = 2 ** (attempt + 1)  # 2s, 4s, 8s, 16s
                time.sleep(wait)
                continue
            raise

    calls = [response]
    processed_text = "\n".join(block.text for block in response.content if block.type == "text").strip()
    missing_sections = _missing_required_sections(processed_text)
    # Long extractions occasionally reach the response limit after producing all of
    # the substantive analysis but before the final taxonomy fields.  Complete
    # only those fields rather than discarding an otherwise useful extraction.
    if missing_sections and set(missing_sections).issubset({"Tags", "Category"}):
        completion_prompt = f"""The following MegaMind extraction is complete except for the required section(s): {', '.join(missing_sections)}.

Return ONLY the missing Markdown section(s), using these exact headings:
{chr(10).join(f'### {section}' for section in missing_sections)}

For Tags, suggest 3-6 lowercase hashtag tags. For Category, give one precise category name.

Extraction to classify:
---
{processed_text}
---"""
        completion = client.messages.create(
            model=config.CLAUDE_MODEL,
            max_tokens=500,
            messages=[{"role": "user", "content": completion_prompt}],
        )
        calls.append(completion)
        repair_text = "\n".join(block.text for block in completion.content if block.type == "text").strip()
        processed_text = f"{processed_text.rstrip()}\n\n{repair_text}"
        missing_sections = _missing_required_sections(processed_text)
    # Track token usage for budget
    try:
        from budget import record_usage
        for index, call in enumerate(calls):
            record_usage(
                model=config.CLAUDE_MODEL,
                input_tokens=call.usage.input_tokens,
                output_tokens=call.usage.output_tokens,
                api="anthropic",
                title=result.title + (" (section repair)" if index else ""),
            )
    except Exception:
        pass  # Don't let budget tracking break extraction

    if missing_sections:
        raise RuntimeError(
            "AI processing response missing required section(s): "
            + ", ".join(missing_sections)
        )

    return processed_text


def _missing_required_sections(text: str) -> list[str]:
    """Return required MegaMind sections missing from AI output."""
    missing = []
    for section in REQUIRED_SECTIONS:
        pattern = rf"^###\s+{re.escape(section)}\s*$"
        if not re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE):
            missing.append(section)
    return missing


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
#### Prompt 1: Configure API Key
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
