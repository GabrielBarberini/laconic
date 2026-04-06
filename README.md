<p align="center">
  <img src="https://raw.githubusercontent.com/GabrielBarberini/laconic/main/laconic.png" width="120" />
</p>

<h1 align="center">laconic</h1>

<p align="center">
  <strong>Philip II: "If I bring my army into your land, I will destroy your farms, slay your people, and raze your city."<br/>Sparta: "If."</strong>
</p>

<p align="center">
  <a href="https://github.com/GabrielBarberini/laconic/stargazers"><img src="https://img.shields.io/github/stars/GabrielBarberini/laconic?style=flat&color=yellow" alt="Stars"></a>
  <a href="https://github.com/GabrielBarberini/laconic/commits/main"><img src="https://img.shields.io/github/last-commit/GabrielBarberini/laconic?style=flat" alt="Last Commit"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/GabrielBarberini/laconic?style=flat" alt="License"></a>
  <a href="https://gabrielbarberini.github.io/laconic/"><img src="https://img.shields.io/badge/web-gabrielbarberini.github.io%2Flaconic-blue?style=flat" alt="Website"></a>
</p>

<p align="center">
  <a href="#install">Install</a> &bull;
  <a href="#benchmarks">Benchmarks</a> &bull;
  <a href="#examples">Examples</a> &bull;
  <a href="#caveman-vs-laconic">Caveman vs Laconic</a> &bull;
  <a href="#why">Why</a>
</p>

---
Inspired by [caveman](https://github.com/JuliusBrussee/caveman). 

A [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill that cuts **~80% of tokens** — short words, just enough code, trusted context, implication over explanation.

Every word earns its place. 

## Benchmarks

### Caveman bench
Real token counts from Claude Sonnet 4 via Langdock API. Each prompt sent with a generic system prompt ("You are a helpful assistant") vs the full laconic SKILL.md. Median of 3 trials per mode.

<!-- BENCHMARK-TABLE-START -->
| Task | Normal (tokens) | Laconic (tokens) | Saved | vs Caveman |
|------|---------------:|----------------:|------:|-----------:|
| Explain React re-render bug | 940 | 100 | 89% | +2pp |
| Fix auth middleware token expiry | 1292 | 58 | 96% | +13pp |
| Set up PostgreSQL connection pool | 2038 | 384 | 81% | −3pp |
| Explain git rebase vs merge | 987 | 399 | 60% | +2pp |
| Refactor callback to async/await | 454 | 195 | 57% | +35pp |
| Architecture: microservices vs monolith | 956 | 334 | 65% | +35pp |
| Review PR for security issues | 971 | 223 | 77% | +36pp |
| Docker multi-stage build | 2627 | 186 | 93% | +21pp |
| Debug PostgreSQL race condition | 1398 | 94 | 93% | +12pp |
| Implement React error boundary | 4096 | 579 | 86% | −1pp |
| **Average** | **1576** | **255** | **80%** | **+15pp** |

*Range: 57%–96% savings across prompts. [Caveman benchmarks](https://github.com/JuliusBrussee/caveman#benchmarks) averaged 64%.*
<!-- BENCHMARK-TABLE-END -->

> [!IMPORTANT]
> Laconic only affects **output tokens** — thinking/reasoning tokens are untouched. Compression targets prose, not cognition. Biggest win is **readability and speed**; cost savings are a bonus.

<details>
<summary>Run benchmarks yourself</summary>

```bash
cd benchmarks
pip install -r requirements.txt

# Add your Langdock API key to .env.local at the repo root
echo "LANGDOCK_API_KEY=sk-your-key" > ../.env.local

# Dry run (no API calls)
python run.py --dry-run

# Full run (60 API calls: 10 prompts x 2 modes x 3 trials)
python run.py

# Auto-update README table
python run.py --update-readme
```

</details>

## Examples

<table>
<tr>
<td width="33%">

### 🗣️ Normal (69 tokens)

> "The reason your React component is re-rendering is likely because you're creating a new object reference on each render cycle. When you pass an inline object as a prop, React's shallow comparison sees it as a different object every time, which triggers a re-render. I'd recommend using useMemo to memoize the object."

</td>
<td width="33%">

### 🪨 Caveman (19 tokens)

> "New object ref each render. Inline object prop = new ref = re-render. Wrap in `useMemo`."

</td>
<td width="33%">

### Λ Laconic (10 tokens)

> "Inline object prop creates new reference. Wrap in `useMemo`."

</td>
</tr>
<tr>
<td>

### 🗣️ Normal

> "Sure! I'd be happy to help you with that. The issue you're experiencing is most likely caused by your authentication middleware not properly validating the token expiry. Let me take a look and suggest a fix."

</td>
<td>

### 🪨 Caveman

> "Bug in auth middleware. Token expiry check use `<` not `<=`. Fix:"

</td>
<td>

### Λ Laconic

> "Auth middleware expiry check requires `<`. Fix:"

</td>
</tr>
</table>

## Install

### Any agent (40+ supported)

```bash
npx skills add GabrielBarberini/laconic
```

`npx skills` supports Claude Code, GitHub Copilot, Cursor, Windsurf, Cline, and [40+ more](https://github.com/vercel-labs/skills). To install for a specific agent:

```bash
npx skills add GabrielBarberini/laconic -a cursor
npx skills add GabrielBarberini/laconic -a copilot
npx skills add GabrielBarberini/laconic -a cline
npx skills add GabrielBarberini/laconic -a windsurf
```

### Claude Code (plugin)

```bash
claude plugin marketplace add GabrielBarberini/laconic
claude plugin install laconic@laconic
```

### Codex

1. Clone repo
2. Open Codex in repo
3. Run `/plugins`
4. Search `Laconic`
5. Install plugin

Or copy the `plugins/laconic/` directory into your Codex plugins folder.

Install once. Works in all sessions after that.

## Usage

Trigger with:
- `/laconic`
- "laconic mode"
- "be laconic"
- "less tokens please"

Stop with: "stop laconic" or "normal mode"

## What Laconic Does

| Category | Rule |
|----------|------|
| Prose | Stripped to what matters. Short common words. |
| Articles (a/an/the) | Dropped unless ambiguity results |
| Filler / pleasantries / hedging | Gone |
| Mechanism / explanation | Omit unless asked — give diagnosis and fix |
| Word choice | Shortest common word that works |
| Context | Assumes reader has domain knowledge — don't explain what a domain-aware individual already knows and don't restate what user says |
| Technical substance | Preserved — compress words, not facts |
| Error messages | Quoted verbatim |
| Code | Just enough

## Caveman vs Laconic

| | Caveman | Laconic |
|--|---------|---------|
| Tone | Primitive | Terse, Concealed wisdom |
| Explanation | Normal | Trusts context, skips what reader knows |
| Code | Normal | Just enough code |
| Token savings | ~65% | ~80% |

Laconic speech is not just brevity — it is the weaponization of implication

## Why

- **Save money** — ~80% fewer output tokens
- **Faster** — fewer tokens to generate
- **Trusts the reader** — skips what is already known
- **Preserves facts** — compresses words, not substance
- "Para bom entendedor 🧦🪏"

## Star

Useful? One star suffices. ⭐

[![Star History Chart](https://api.star-history.com/svg?repos=GabrielBarberini/laconic&type=Date)](https://star-history.com/#GabrielBarberini/laconic&Date)

## License

MIT — Sparta needed no walls. Neither does this license.
