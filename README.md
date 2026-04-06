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

A [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill that cuts **~75% of tokens** — short words, trusted context, implication over explanation.

Inspired by [caveman](https://github.com/JuliusBrussee/caveman). Same compression, different style.

Say the minimum. Trust context. Every word earns its place.

## Benchmarks

Real token counts from Claude Sonnet 4 via Langdock API. Each prompt sent with a generic system prompt ("You are a helpful assistant") vs the full laconic SKILL.md. Median of 3 trials per mode.

<!-- BENCHMARK-TABLE-START -->
| Task | Normal (tokens) | Laconic (tokens) | Saved | vs Caveman |
|------|---------------:|----------------:|------:|-----------:|
| Explain React re-render bug | 941 | 106 | 89% | +2pp |
| Fix auth middleware token expiry | 1100 | 83 | 92% | +9pp |
| Set up PostgreSQL connection pool | 2104 | 361 | 83% | −1pp |
| Explain git rebase vs merge | 1004 | 347 | 65% | +7pp |
| Refactor callback to async/await | 461 | 141 | 69% | +47pp |
| Architecture: microservices vs monolith | 889 | 356 | 60% | +30pp |
| Review PR for security issues | 758 | 244 | 68% | +27pp |
| Docker multi-stage build | 2583 | 379 | 85% | +13pp |
| Debug PostgreSQL race condition | 1339 | 197 | 85% | +4pp |
| Implement React error boundary | 4096 | 658 | 84% | −3pp |
| **Average** | **1528** | **287** | **78%** | **+14pp** |

*Range: 60%–92% savings across prompts. [Caveman benchmarks](https://github.com/JuliusBrussee/caveman#benchmarks) averaged 64%.*
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

### Claude Code (skill)

```bash
npx skills add GabrielBarberini/laconic
```

### Claude Code (plugin)

```bash
claude plugin marketplace add GabrielBarberini/laconic
claude plugin install laconic@laconic
```

### Codex

Install from the `.agents/plugins/marketplace.json` registry or copy the `plugins/laconic/` directory into your Codex plugins folder.

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

## Caveman vs Laconic

| | Caveman | Laconic |
|--|---------|---------|
| Grammar | Broken | Minimal but clean |
| Tone | Primitive | Terse, Concealed wisdom |
| Articles | Always dropped | Dropped unless ambiguous |
| Word choice | Shortest word | Simplest common word |
| Explanation | Still explains | Trusts context, skips what reader knows |
| Token savings | ~65% | ~79% |

Laconic speech is not just brevity — it is the weaponization of implication

## Why

- **Save money** — ~79% fewer output tokens
- **Faster** — fewer tokens to generate
- **Trusts the reader** — skips what devs already know
- **Preserves facts** — compresses words, not substance
- "Para bom entendedor 🧦🪏"

## Star

Useful? One star suffices. ⭐

[![Star History Chart](https://api.star-history.com/svg?repos=GabrielBarberini/laconic&type=Date)](https://star-history.com/#GabrielBarberini/laconic&Date)

## License

MIT — Sparta needed no walls. Neither does this license.
