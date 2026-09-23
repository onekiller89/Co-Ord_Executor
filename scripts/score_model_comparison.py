"""Summarise measured properties of the private ten-source model comparison.

This checks structure, brevity, receipts and source URL only. Human review is
still required for factual accuracy and whether the actions are worthwhile.
"""

import json
import os
import re
from pathlib import Path

OUT = Path(os.environ.get("MEGAMIND_EVAL_DIR", Path.home() / ".local/share/megamind/model-eval"))
MODELS = ("claude-opus-5-5", "claude-sonnet-5", "gpt-6-astra", "gpt-6-sol", "gpt-6-luna")
HEADINGS = ("Summary", "Key Insights", "Actions", "Implementation Prompts", "Links & Resources", "Tags", "Category")


def main():
    sources = json.loads((OUT / "manifest.json").read_text(encoding="utf-8"))
    result = []
    for model in MODELS:
        rows = []
        for source in sources:
            if source["status"] != "ready":
                continue
            num = source["index_number"]
            body = (OUT / f"output-{num}-{model}.md").read_text(encoding="utf-8")
            receipt = json.loads((OUT / f"receipt-{num}-{model}.json").read_text(encoding="utf-8"))
            parts = dict(re.findall(r"^### ([^\n]+)\n(.*?)(?=^### |\Z)", body, re.M | re.S))
            insights = re.findall(r"^-\s+\S", parts.get("Key Insights", ""), re.M)
            actions = re.findall(r"^- \[ \] \S", parts.get("Actions", ""), re.M)
            rows.append({"words": len(body.split()),
                         "headings_ok": tuple(parts) == HEADINGS,
                         "four_insights": len(insights) == 4,
                         "three_actions": len(actions) == 3,
                         "under_400_words": len(body.split()) <= 400,
                         "original_url_present": source["url"] in parts.get("Links & Resources", ""),
                         "seconds": receipt["seconds"],
                         "estimated_usd": receipt.get("estimated_usd"),
                         "success": receipt.get("returncode", 0) == 0 and receipt.get("stop_reason", "end_turn") == "end_turn"})
        result.append({"model": model, "sources": len(rows),
                       "avg_words": round(sum(r["words"] for r in rows) / len(rows)),
                       "range_words": [min(r["words"] for r in rows), max(r["words"] for r in rows)],
                       "avg_seconds": round(sum(r["seconds"] for r in rows) / len(rows), 1),
                       "estimated_api_usd": round(sum(r["estimated_usd"] or 0 for r in rows), 4) if model.startswith("claude") else None,
                       "checks": {key: sum(r[key] for r in rows) for key in
                                  ("success", "headings_ok", "four_insights", "three_actions", "under_400_words", "original_url_present")}})
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
