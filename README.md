<p align="center">
  <img src="https://raw.githubusercontent.com/GabrielBarberini/laconic/main/laconic.png" width="120" />
</p>

<h1 align="center">laconic</h1>

<p align="center">
  <strong>Philip II: "If I bring my army into your land, I will destroy your farms, slay your people, and raze your city."<br/>Sparta: "If."</strong>
</p>

<p align="center">
  <a href="#install">Install</a> &bull;
  <a href="#examples">Examples</a> &bull;
  <a href="#caveman-vs-laconic">Caveman vs Laconic</a> &bull;
  <a href="#why">Why</a>
</p>

---

A [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill that cuts **~75% of tokens** — short words, trusted context, implication over explanation.

Inspired by [caveman](https://github.com/JuliusBrussee/caveman). Same compression, different style.

Say the minimum. Trust context. Every word earns its place.

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

```bash
npx skills add GabrielBarberini/laconic
```

Or with Claude Code plugin system:

```bash
claude plugin marketplace add GabrielBarberini/laconic
claude plugin install laconic@laconic
```

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
| Code blocks | Unchanged — laconic governs prose only |
| Error messages | Quoted verbatim |
| Mechanism / explanation | Omit unless asked — give diagnosis and fix |
| Word choice | Shortest common word that works |
| Context | Assumes reader has domain knowledge — don't explain what a domain-aware individual already knows and don't restate what user says |
| Technical substance | Preserved — compress words, not facts |

## Caveman vs Laconic

| | Caveman | Laconic |
|--|---------|---------|
| Grammar | Broken | Minimal but clean |
| Tone | Primitive | Terse, blunt |
| Articles | Always dropped | Dropped unless ambiguous |
| Word choice | Shortest word | Simplest common word |
| Explanation | Still explains | Trusts context, skips what reader knows |
| Reads like | Broken English | Clipped military briefing |
| Token savings | ~75% | ~75% |

Same compression, different voice. Caveman: grammar deleted. Laconic: verbosity offensive.

## Why

- **Save money** — ~75% fewer output tokens
- **Faster** — fewer tokens to generate
- **Trusts the reader** — skips what devs already know
- **Preserves facts** — compresses words, not substance
- "Para bom entendedor 🧦🪏"

## License

MIT
