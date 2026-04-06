# Contributing

This repo has one goal: **be laconic**.

Compression is a side effect, not the objective. If a change squeezes out more tokens but the output stops sounding laconic — clean grammar, trusted context, every word earning its place — it gets rejected. A Spartan who mumbles isn't laconic. A Spartan who says "If." is.

## How

1. Fork the repo
2. Edit `skills/laconic/SKILL.md`
3. Run the benchmark:
   ```bash
   cd benchmarks
   pip install -r requirements.txt
   python run.py
   ```
4. Open a PR with the benchmark output — either the regression test (same 10 prompts) or an extended run including your own prompts

## Acceptance

- Benchmark savings stay equal or improve
- Output still reads as laconic — not broken, not telegraphic, not caveman
- Both conditions required. Numbers alone don't pass review

## Rules

- Keep all 3 SKILL.md copies in sync (`skills/laconic/`, `laconic/`, `plugins/laconic/skills/laconic/`)
- Small focused edits over rewrites
- No templates needed — benchmark numbers and voice speak for themselves
