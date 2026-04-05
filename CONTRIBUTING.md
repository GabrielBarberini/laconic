# Contributing

Improvements to `SKILL.md` are welcome. The bar is simple: run the benchmark, show it got better.

## How

1. Fork the repo
2. Edit `skills/laconic/SKILL.md`
3. Run the benchmark:
   ```bash
   cd benchmarks
   pip install -r requirements.txt
   python run.py
   ```
4. Open a PR with the benchmark output showing improvement — either the regression test (same 10 prompts) or an extended run including your own prompts

If savings go up or stay equal with better quality, it's a valuable change.

## Rules

- Keep all 3 SKILL.md copies in sync (`skills/laconic/`, `laconic/`, `plugins/laconic/skills/laconic/`)
- Small focused edits over rewrites
- No templates needed — benchmark numbers speak for themselves

## Ideas

See [issues labeled `good first issue`](../../issues?q=label%3A%22good+first+issue%22) for starter tasks.
