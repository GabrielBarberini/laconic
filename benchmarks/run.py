#!/usr/bin/env python3
"""Benchmark laconic vs normal output token counts via Langdock.

Adapted from github.com/JuliusBrussee/caveman/benchmarks/run.py (MIT).
Uses Langdock's Anthropic-compatible API instead of the Anthropic SDK directly.
"""

import argparse
import hashlib
import json
import os
import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import httpx

# ---------------------------------------------------------------------------
# .env.local loader (same pattern as caveman)
# ---------------------------------------------------------------------------
_env_file = Path(__file__).parent.parent / ".env.local"
if _env_file.exists():
    for line in _env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SCRIPT_VERSION = "1.0.0"
SCRIPT_DIR = Path(__file__).parent
REPO_DIR = SCRIPT_DIR.parent
PROMPTS_PATH = SCRIPT_DIR / "prompts.json"
SKILL_PATH = REPO_DIR / "skills" / "laconic" / "SKILL.md"
README_PATH = REPO_DIR / "README.md"
RESULTS_DIR = SCRIPT_DIR / "results"

NORMAL_SYSTEM = "You are a helpful assistant."
BENCHMARK_START = "<!-- BENCHMARK-TABLE-START -->"
BENCHMARK_END = "<!-- BENCHMARK-TABLE-END -->"

# Langdock Anthropic-compatible endpoint
LANGDOCK_BASE_URL = os.environ.get("LANGDOCK_BASE_URL", "https://api.langdock.com")
LANGDOCK_REGION = os.environ.get("LANGDOCK_REGION", "eu")
LANGDOCK_API_URL = f"{LANGDOCK_BASE_URL}/anthropic/{LANGDOCK_REGION}/v1/messages"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def load_prompts():
    with open(PROMPTS_PATH) as f:
        data = json.load(f)
    return data["prompts"]


def load_laconic_system():
    return SKILL_PATH.read_text()


def sha256_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def get_api_key():
    key = os.environ.get("LANGDOCK_API_KEY")
    if not key:
        print(
            "ERROR: LANGDOCK_API_KEY not set. "
            "Add it to .env.local at the repo root or export it.",
            file=sys.stderr,
        )
        sys.exit(1)
    return key


def call_api(api_key, model, system, prompt, max_retries=3):
    """Send a single message via Langdock's Anthropic-compatible API."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01",
    }
    payload = {
        "model": model,
        "max_tokens": 4096,
        "temperature": 0,
        "system": system,
        "messages": [{"role": "user", "content": prompt}],
    }

    delays = [5, 10, 20]
    for attempt in range(max_retries + 1):
        try:
            with httpx.Client(timeout=120) as client:
                resp = client.post(LANGDOCK_API_URL, headers=headers, json=payload)

            if resp.status_code == 429:
                raise _RateLimited()

            if resp.status_code >= 400:
                print(
                    f"  API error {resp.status_code}: {resp.text[:500]}",
                    file=sys.stderr,
                )
            resp.raise_for_status()
            data = resp.json()

            usage = data.get("usage", {})
            content = data.get("content", [])
            text = ""
            for block in content:
                if block.get("type") == "text":
                    text += block.get("text", "")

            return {
                "input_tokens": usage.get("input_tokens", 0),
                "output_tokens": usage.get("output_tokens", 0),
                "text": text,
                "stop_reason": data.get("stop_reason", "?"),
            }

        except (_RateLimited, httpx.HTTPStatusError) as exc:
            status = getattr(exc, "response", None)
            status = status.status_code if status is not None else 429
            if status in (429, 502, 503, 504) and attempt < max_retries:
                delay = delays[min(attempt, len(delays) - 1)]
                print(
                    f"  HTTP {status}, retrying in {delay}s...",
                    file=sys.stderr,
                )
                time.sleep(delay)
            else:
                raise


class _RateLimited(Exception):
    pass


# ---------------------------------------------------------------------------
# Benchmark runner
# ---------------------------------------------------------------------------


def run_benchmarks(api_key, model, prompts, laconic_system, trials):
    results = []
    total = len(prompts)

    for i, prompt_entry in enumerate(prompts, 1):
        pid = prompt_entry["id"]
        prompt_text = prompt_entry["prompt"]
        entry = {
            "id": pid,
            "category": prompt_entry["category"],
            "prompt": prompt_text,
            "normal": [],
            "laconic": [],
        }

        for mode, system in [("normal", NORMAL_SYSTEM), ("laconic", laconic_system)]:
            for t in range(1, trials + 1):
                print(
                    f"  [{i}/{total}] {pid} | {mode} | trial {t}/{trials}",
                    file=sys.stderr,
                )
                result = call_api(api_key, model, system, prompt_text)
                entry[mode].append(result)
                time.sleep(0.5)

        results.append(entry)

    return results


# ---------------------------------------------------------------------------
# Stats & formatting
# ---------------------------------------------------------------------------


def compute_stats(results):
    rows = []
    all_savings = []

    for entry in results:
        normal_median = statistics.median(
            [t["output_tokens"] for t in entry["normal"]]
        )
        laconic_median = statistics.median(
            [t["output_tokens"] for t in entry["laconic"]]
        )
        savings = 1 - (laconic_median / normal_median) if normal_median > 0 else 0
        all_savings.append(savings)

        rows.append(
            {
                "id": entry["id"],
                "category": entry["category"],
                "prompt": entry["prompt"],
                "normal_median": int(normal_median),
                "laconic_median": int(laconic_median),
                "savings_pct": round(savings * 100),
            }
        )

    avg_savings = round(statistics.mean(all_savings) * 100)
    min_savings = round(min(all_savings) * 100)
    max_savings = round(max(all_savings) * 100)
    avg_normal = round(statistics.mean([r["normal_median"] for r in rows]))
    avg_laconic = round(statistics.mean([r["laconic_median"] for r in rows]))

    return rows, {
        "avg_savings": avg_savings,
        "min_savings": min_savings,
        "max_savings": max_savings,
        "avg_normal": avg_normal,
        "avg_laconic": avg_laconic,
    }


PROMPT_LABELS = {
    "react-rerender": "Explain React re-render bug",
    "auth-middleware-fix": "Fix auth middleware token expiry",
    "postgres-pool": "Set up PostgreSQL connection pool",
    "git-rebase-merge": "Explain git rebase vs merge",
    "async-refactor": "Refactor callback to async/await",
    "microservices-monolith": "Architecture: microservices vs monolith",
    "pr-security-review": "Review PR for security issues",
    "docker-multi-stage": "Docker multi-stage build",
    "race-condition-debug": "Debug PostgreSQL race condition",
    "error-boundary": "Implement React error boundary",
}

# Caveman benchmark savings (%) from github.com/JuliusBrussee/caveman README.
# Same 10 prompts, used to compute the "vs Caveman" delta column.
CAVEMAN_SAVINGS = {
    "react-rerender": 87,
    "auth-middleware-fix": 83,
    "postgres-pool": 84,
    "git-rebase-merge": 58,
    "async-refactor": 22,
    "microservices-monolith": 30,
    "pr-security-review": 41,
    "docker-multi-stage": 72,
    "race-condition-debug": 81,
    "error-boundary": 87,
}


def _fmt_delta(delta):
    """Format a percentage-point delta as '+Npp', '0pp', or '−Npp'."""
    if delta > 0:
        return f"+{delta}pp"
    elif delta < 0:
        return f"\u2212{abs(delta)}pp"
    return "0pp"


def format_table(rows, summary):
    lines = [
        "| Task | Normal (tokens) | Laconic (tokens) | Saved | vs Caveman |",
        "|------|---------------:|----------------:|------:|-----------:|",
    ]
    deltas = []
    for r in rows:
        label = PROMPT_LABELS.get(r["id"], r["id"])
        caveman_pct = CAVEMAN_SAVINGS.get(r["id"])
        if caveman_pct is not None:
            delta = r["savings_pct"] - caveman_pct
            deltas.append(delta)
            delta_str = _fmt_delta(delta)
        else:
            delta_str = "n/a"
        lines.append(
            f"| {label} | {r['normal_median']} | {r['laconic_median']} | {r['savings_pct']}% | {delta_str} |"
        )

    avg_delta = round(statistics.mean(deltas)) if deltas else 0
    lines.append(
        f"| **Average** | **{summary['avg_normal']}** | **{summary['avg_laconic']}** | **{summary['avg_savings']}%** | **{_fmt_delta(avg_delta)}** |"
    )
    lines.append("")
    caveman_avg = round(statistics.mean(CAVEMAN_SAVINGS.values()))
    lines.append(
        f"*Range: {summary['min_savings']}%\u2013{summary['max_savings']}% savings across prompts. [Caveman benchmarks](https://github.com/JuliusBrussee/caveman#benchmarks) averaged {caveman_avg}%.*"
    )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------


def save_results(results, rows, summary, model, trials, skill_hash):
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    output = {
        "metadata": {
            "script_version": SCRIPT_VERSION,
            "model": model,
            "provider": "langdock",
            "api_url": LANGDOCK_API_URL,
            "date": datetime.now(timezone.utc).isoformat(),
            "trials": trials,
            "skill_md_sha256": skill_hash,
        },
        "summary": summary,
        "rows": rows,
        "raw": results,
    }
    path = RESULTS_DIR / f"benchmark_{ts}.json"
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(output, f, indent=2)
    return path


def update_readme(table_md):
    content = README_PATH.read_text()
    start_idx = content.find(BENCHMARK_START)
    end_idx = content.find(BENCHMARK_END)
    if start_idx == -1 or end_idx == -1:
        print(
            "ERROR: Benchmark markers not found in README.md",
            file=sys.stderr,
        )
        sys.exit(1)

    before = content[: start_idx + len(BENCHMARK_START)]
    after = content[end_idx:]
    new_content = before + "\n" + table_md + "\n" + after
    README_PATH.write_text(new_content)
    print("README.md updated.", file=sys.stderr)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def dry_run(prompts, model, trials):
    print(f"Model:      {model}")
    print(f"Provider:   Langdock ({LANGDOCK_API_URL})")
    print(f"Trials:     {trials}")
    print(f"Prompts:    {len(prompts)}")
    print(f"API calls:  {len(prompts) * 2 * trials}")
    print()
    for p in prompts:
        print(f"  [{p['id']}] ({p['category']})")
        preview = p["prompt"][:80]
        if len(p["prompt"]) > 80:
            preview += "..."
        print(f"    {preview}")
    print()
    print("Dry run complete. No API calls made.")


def main():
    parser = argparse.ArgumentParser(
        description="Benchmark laconic vs normal output tokens (via Langdock)"
    )
    parser.add_argument(
        "--trials",
        type=int,
        default=3,
        help="Trials per prompt per mode (default: 3)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print config, no API calls",
    )
    parser.add_argument(
        "--update-readme",
        action="store_true",
        help="Update README.md benchmark table",
    )
    parser.add_argument(
        "--model",
        default="claude-sonnet-4-6-default",
        help="Langdock model ID (default: claude-sonnet-4-6-default)",
    )
    args = parser.parse_args()

    prompts = load_prompts()

    if args.dry_run:
        dry_run(prompts, args.model, args.trials)
        return

    api_key = get_api_key()
    laconic_system = load_laconic_system()
    skill_hash = sha256_file(SKILL_PATH)

    print(
        f"Running benchmarks: {len(prompts)} prompts x 2 modes x {args.trials} trials",
        file=sys.stderr,
    )
    print(f"Model: {args.model}", file=sys.stderr)
    print(f"Provider: Langdock ({LANGDOCK_API_URL})", file=sys.stderr)
    print(file=sys.stderr)

    results = run_benchmarks(api_key, args.model, prompts, laconic_system, args.trials)
    rows, summary = compute_stats(results)
    table_md = format_table(rows, summary)

    json_path = save_results(
        results, rows, summary, args.model, args.trials, skill_hash
    )
    print(f"\nResults saved to {json_path}", file=sys.stderr)

    if args.update_readme:
        update_readme(table_md)

    print(table_md)


if __name__ == "__main__":
    main()
