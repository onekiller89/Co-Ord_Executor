"""Bounded, local-only comparison of MegaMind analysis models.

Raw YouTube captions and model outputs stay outside the public Git repository.
Run from the repository root with CI=true so missing captions fail closed.
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(os.environ.get("MEGAMIND_EVAL_DIR", Path.home() / ".local/share/megamind/model-eval"))
MODELS = ("claude-opus-5-5", "claude-sonnet-5", "gpt-6-astra", "gpt-6-sol", "gpt-6-luna")
PRICES = {
    "claude-opus-5-5": (4.0, 20.0),
    "claude-sonnet-5": (2.0, 10.0),
}

SYSTEM = (ROOT / "prompts" / "analysis-v2.md").read_text(encoding="utf-8").strip()


def _ensure_out() -> None:
    OUT.mkdir(mode=0o700, parents=True, exist_ok=True)
    OUT.chmod(0o700)


def _manifest() -> list[dict]:
    return json.loads((OUT / "manifest.json").read_text(encoding="utf-8"))


def prepare() -> None:
    """Recover captions for the latest ten source-backed extractions."""
    os.environ["CI"] = "true"
    import sys
    sys.path.insert(0, str(ROOT))
    from extractors.youtube import YouTubeExtractor

    _ensure_out()
    rows = []
    index = (ROOT / "extractions" / "INDEX.md").read_text(encoding="utf-8")
    for line in index.splitlines():
        if not re.match(r"^\| \d+ \|", line):
            continue
        cells = [cell.strip() for cell in line.split("|")]
        if len(cells) < 10 or cells[4] == "Unverified" or cells[3] != "YouTube":
            continue
        link = re.search(r"\]\(\./(.+?)\)", cells[8])
        if not link:
            continue
        historical = ROOT / "extractions" / link.group(1)
        if not historical.exists():
            continue
        old = historical.read_text(encoding="utf-8")
        url = re.search(r"^> \*\*URL:\*\* (https?://\S+)", old, re.M)
        if not url:
            continue
        rows.append((int(cells[1]), historical, url.group(1), old))

    selected = rows[-10:]
    if len(selected) != 10:
        raise RuntimeError(f"Expected ten recent sources, found {len(selected)}")
    manifest = []
    for number, historical, url, old in selected:
        item = {"index_number": number, "url": url,
                "historical_file": str(historical.relative_to(ROOT)),
                "historical_sha256": hashlib.sha256(old.encode()).hexdigest()}
        try:
            result = YouTubeExtractor().extract(url)
            if result.metadata.get("extraction_method") not in {"youtube_transcript_api", "yt_dlp_subtitles"}:
                raise RuntimeError("Source is not verified captions")
            raw = result.raw_content
            path = OUT / f"source-{number}.txt"
            path.write_text(raw, encoding="utf-8")
            item.update({"title": result.title, "source_file": path.name,
                         "source_sha256": hashlib.sha256(raw.encode()).hexdigest(),
                         "source_chars": len(raw),
                         "extraction_method": result.metadata["extraction_method"],
                         "status": "ready"})
        except Exception as exc:
            item.update({"status": "unavailable", "error": f"{type(exc).__name__}: {exc}"[:250]})
        manifest.append(item)
        print(f"{number}: {item['status']} {item.get('source_chars', 0)} chars", flush=True)
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Ready: {sum(x['status']=='ready' for x in manifest)}/10; {OUT}")


def _prompt(item: dict) -> str:
    source = (OUT / item["source_file"]).read_text(encoding="utf-8")
    return f"{SYSTEM}\n\nSOURCE TRANSCRIPT\n{source}\nEND SOURCE\n\nReturn only the seven Markdown sections."


def run_anthropic(model: str, cap_usd: float) -> None:
    import sys
    sys.path.insert(0, str(ROOT))
    from dotenv import load_dotenv
    load_dotenv(os.environ.get("MEGAMIND_EVAL_ENV", str(ROOT / ".env")))
    import anthropic
    import config

    if model not in PRICES:
        raise ValueError(model)
    _ensure_out()
    client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY, timeout=180)
    spent = 0.0
    for item in _manifest():
        if item["status"] != "ready":
            continue
        output = OUT / f"output-{item['index_number']}-{model}.md"
        receipt = OUT / f"receipt-{item['index_number']}-{model}.json"
        if receipt.exists():
            spent += json.loads(receipt.read_text()).get("estimated_usd", 0)
            continue
        # Conservative preflight: chars/2 input tokens, full 3200 output tokens.
        input_ceiling = len(_prompt(item)) / 2
        reserve = (input_ceiling * PRICES[model][0] + 3200 * PRICES[model][1]) / 1_000_000
        if spent + reserve > cap_usd:
            raise RuntimeError(f"Cost cap would be exceeded: ${spent + reserve:.2f} > ${cap_usd:.2f}")
        started = time.monotonic()
        response = client.messages.create(model=model, max_tokens=3200,
            system=SYSTEM, messages=[{"role": "user", "content":
                (OUT / item["source_file"]).read_text(encoding="utf-8") +
                "\n\nReturn only the seven Markdown sections."}])
        content = "\n".join(block.text for block in response.content if block.type == "text")
        output.write_text(content, encoding="utf-8")
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens
        cost = (input_tokens * PRICES[model][0] + output_tokens * PRICES[model][1]) / 1_000_000
        spent += cost
        receipt.write_text(json.dumps({"model": model, "index_number": item["index_number"],
            "input_tokens": input_tokens, "output_tokens": output_tokens,
            "estimated_usd": round(cost, 6), "seconds": round(time.monotonic()-started, 2),
            "stop_reason": response.stop_reason, "source_sha256": item["source_sha256"]}, indent=2), encoding="utf-8")
        print(f"{model} #{item['index_number']} ${cost:.4f} {response.stop_reason}", flush=True)


def run_codex(model: str, executable: str) -> None:
    if model not in MODELS or not model.startswith("gpt-"):
        raise ValueError(model)
    _ensure_out()
    for item in _manifest():
        if item["status"] != "ready":
            continue
        output = OUT / f"output-{item['index_number']}-{model}.md"
        receipt = OUT / f"receipt-{item['index_number']}-{model}.json"
        if receipt.exists():
            continue
        started = time.monotonic()
        command = [executable, "exec", "--ephemeral", "--ignore-user-config",
                   "--skip-git-repo-check", "--sandbox", "read-only",
                   "-c", "model_reasoning_effort=medium", "-m", model,
                   "-o", str(output), "-"]
        prompt = _prompt(item) + "\nDo not use tools or inspect files; the complete source is above."
        completed = subprocess.run(command, input=prompt, text=True, cwd="/tmp",
                                   capture_output=True, timeout=300)
        receipt.write_text(json.dumps({"model": model, "index_number": item["index_number"],
            "seconds": round(time.monotonic()-started, 2), "returncode": completed.returncode,
            "source_sha256": item["source_sha256"],
            "stderr_tail": completed.stderr[-600:] if completed.returncode else ""}, indent=2), encoding="utf-8")
        print(f"{model} #{item['index_number']} rc={completed.returncode} {round(time.monotonic()-started,1)}s", flush=True)
        if completed.returncode:
            raise RuntimeError(f"Codex model call failed: {completed.stderr[-350:]}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("command", choices=("prepare", "anthropic", "codex"))
    p.add_argument("--model", choices=MODELS)
    p.add_argument("--cap-usd", type=float, default=12)
    p.add_argument("--codex", default=os.environ.get("MEGAMIND_CODEX_CLI", "codex"))
    args = p.parse_args()
    if args.command == "prepare":
        prepare()
    elif args.command == "anthropic":
        run_anthropic(args.model, args.cap_usd)
    else:
        run_codex(args.model, args.codex)
