"""API usage and budget tracking for MegaMind.

Tracks token usage, estimated costs, and provides budget summaries.
Data is persisted to a JSON file for cross-session tracking.
"""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

import config

log = logging.getLogger("megamind.budget")

BUDGET_FILE = config.PROJECT_ROOT / "api_budget.json"

# Pricing (USD per 1M tokens); verify against provider rates when models change.
# https://platform.claude.com/docs/en/about-claude/pricing
PRICING = {
    "claude-opus-5-5":         {"input": 4.00, "output": 20.00},
    "claude-sonnet-5":        {"input": 2.00, "output": 10.00},
    "claude-sonnet-4-6":       {"input": 3.00, "output": 15.00},
    "claude-opus-4-6":         {"input": 15.00, "output": 75.00},
    "claude-haiku-4-5":        {"input": 0.80, "output": 4.00},
    # Grok (xAI) — approximate, varies
    "grok-3-latest":           {"input": 3.00, "output": 15.00},
    "grok-3":                  {"input": 3.00, "output": 15.00},
}

# Fallback pricing if model not in table
DEFAULT_PRICING = {"input": 3.00, "output": 15.00}


def _load() -> dict:
    """Load budget data from disk."""
    if BUDGET_FILE.exists():
        try:
            return json.loads(BUDGET_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, IOError):
            log.warning("Corrupt budget file — starting fresh")
    return {
        "total_input_tokens": 0,
        "total_output_tokens": 0,
        "total_cost": 0.0,
        "extraction_count": 0,
        "subscription_runs": 0,
        "history": [],  # recent entries for breakdown
    }


def _save(data: dict):
    """Persist budget data to disk."""
    BUDGET_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")


def _estimate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """Estimate cost in USD for a given API call."""
    prices = PRICING.get(model, DEFAULT_PRICING)
    cost = (input_tokens * prices["input"] + output_tokens * prices["output"]) / 1_000_000
    return round(cost, 6)


def record_usage(
    model: str,
    input_tokens: int,
    output_tokens: int,
    api: str = "anthropic",
    title: str = "",
) -> dict:
    """Record an API call's token usage and return the updated budget summary.

    Args:
        model: Model name (e.g. "claude-sonnet-4-6")
        input_tokens: Number of input tokens used
        output_tokens: Number of output tokens used
        api: Which API ("anthropic" or "grok")
        title: Optional extraction title for the history log

    Returns:
        Updated budget summary dict.
    """
    data = _load()
    cost = _estimate_cost(model, input_tokens, output_tokens)

    data["total_input_tokens"] += input_tokens
    data["total_output_tokens"] += output_tokens
    data["total_cost"] += cost
    data["extraction_count"] += 1

    # Keep last 100 entries in history
    entry = {
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"),
        "api": api,
        "model": model,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cost": cost,
        "title": title[:60] if title else "",
    }
    data["history"].append(entry)
    if len(data["history"]) > 100:
        data["history"] = data["history"][-100:]

    data["total_cost"] = round(data["total_cost"], 6)
    _save(data)

    log.info(
        f"Budget: +${cost:.4f} ({input_tokens}in/{output_tokens}out) "
        f"| Total: ${data['total_cost']:.4f} ({data['extraction_count']} extractions)"
    )
    return data


def record_subscription_run(model: str, title: str = "") -> dict:
    """Count Codex subscription analyses without inventing an API charge."""
    data = _load()
    data["subscription_runs"] = data.get("subscription_runs", 0) + 1
    data["history"].append({
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"),
        "api": "codex_subscription", "model": model, "title": title[:60],
        "cost": None,
    })
    data["history"] = data["history"][-100:]
    _save(data)
    return data


def get_summary() -> dict:
    """Return the current budget summary."""
    return _load()


def format_budget_embed_text() -> str:
    """Return a formatted string for Discord display."""
    data = _load()
    lines = [f"**Codex subscription analyses:** {data.get('subscription_runs', 0)}"]
    if data["extraction_count"]:
        avg_cost = data["total_cost"] / data["extraction_count"]
        lines.extend([
            f"**Tracked API spend:** ${data['total_cost']:.4f}",
            f"**API calls:** {data['extraction_count']}",
            f"**Avg API cost/call:** ${avg_cost:.4f}",
            f"**API tokens:** {data['total_input_tokens']:,} in / {data['total_output_tokens']:,} out",
        ])
    elif not data.get("subscription_runs"):
        return "No model usage recorded yet."

    # Last 5 entries
    recent = data["history"][-5:]
    if recent:
        lines.append("\n**Recent:**")
        for entry in reversed(recent):
            title = entry.get("title", "")
            charge = "subscription" if entry.get("cost") is None else f"${entry['cost']:.4f}"
            lines.append(f"  `{charge}` {entry['api']}/{entry['model'][:20]}: {title or 'untitled'} ({entry['date']})")

    return "\n".join(lines)
