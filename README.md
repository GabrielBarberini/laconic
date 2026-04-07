<p align="center">
  <img src="https://raw.githubusercontent.com/GabrielBarberini/laconic/main/laconic.png" width="120" />
</p>

<h1 align="center">laconic</h1>

<p align="center">
  <strong>Philip II: "If I invade Laconia, I shall turn you out."<br/>Sparta: "If."</strong>
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
  <a href="#caveman-vs-laconic">Caveman vs Laconic</a>
</p>

---

**laconic** is a 300 word skill for AI coding agents. Inspired by [caveman](https://github.com/JuliusBrussee/caveman). 

It cuts filler.
It keeps meaning.
It trusts context.

Think: short, clear, cold.

Every word earns its place. 

## Benchmarks

### Caveman Benchmark
Claude Sonnet 4 via Langdock API. Each prompt: generic system prompt vs full laconic SKILL.md. Median of 3 runs per mode.

<!-- BENCHMARK-TABLE-START -->
| Task | Normal (tokens) | Laconic (tokens) | Saved | vs Caveman |
|------|---------------:|----------------:|------:|-----------:|
| Explain React re-render bug | 885 | 68 | 92% | +5pp |
| Fix auth middleware token expiry | 1059 | 39 | 96% | +13pp |
| Set up PostgreSQL connection pool | 2167 | 189 | 91% | +7pp |
| Explain git rebase vs merge | 996 | 95 | 90% | +32pp |
| Refactor callback to async/await | 494 | 62 | 87% | +65pp |
| Architecture: microservices vs monolith | 826 | 209 | 75% | +45pp |
| Review PR for security issues | 940 | 126 | 87% | +46pp |
| Docker multi-stage build | 2635 | 149 | 94% | +22pp |
| Debug PostgreSQL race condition | 1370 | 49 | 96% | +15pp |
| Implement React error boundary | 4096 | 400 | 90% | +3pp |
| **Average** | **1547** | **139** | **90%** | **+25pp** |

*Range: 75%–96% savings across prompts. [Caveman benchmarks](https://github.com/JuliusBrussee/caveman#benchmarks) averaged 64%.*
<!-- BENCHMARK-TABLE-END -->

> [!IMPORTANT]
> Laconic cuts output tokens only.

<details>
<summary>Run benchmarks yourself</summary>

```bash
cd benchmarks
pip install -r requirements.txt

echo "LANGDOCK_API_KEY=sk-your-key" > ../.env.local

python run.py --dry-run
python run.py
python run.py --update-readme
```

</details>

## Examples

**Prompt**: *"My Express auth middleware is letting expired JWT tokens through. The expiry check uses `Date.now()` compared to the token's `exp` field. What's wrong and how do I fix it?"*

<table>
<tr>
<td width="50%">

### 🗣️ Normal (~1,300 tokens)

Explains JWT spec, Unix timestamps vs JavaScript milliseconds, walks through middleware architecture, adds error handling, suggests libraries, and outputs a full refactored file (...)

</td>
<td width="50%">

### Λ Laconic (19 tokens)

> `exp` is in seconds. `Date.now()` is milliseconds.
>
> ```js
> if (Date.now() / 1000 > payload.exp) // expired
> ```

</td>
</tr>
</table>

## Caveman vs Laconic

| | Caveman | Laconic |
|--|---------|---------|
| Tone | Primitive | Terse |
| Explanation | Normal | Trusts context, skips what reader knows |
| Code | Normal | Just enough code |
| Token savings | ~65% | ~90% |

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

## Usage

Trigger with:
- `/laconic`
- "laconic mode"
- "be laconic"

## License

MIT — Sparta needed no walls. Neither does this license.
