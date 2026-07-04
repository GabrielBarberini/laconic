/**
 * Laconic — a pi extension layering interactive control over the laconic skill.
 *
 * The universal artifact is `skills/laconic/SKILL.md`, consumed by every
 * harness laconic supports (npx skills, Claude Code, Codex, and pi's own
 * skill loader). This extension is pi-only: it does not replace the skill,
 * it drives it. The `## Rules` and `## Pattern` sections are read straight
 * from that SKILL.md at load time, so the extension and the skill never
 * diverge — edit the skill, the extension follows.
 *
 * Adds:
 *   - `/laconic [low|medium|high|off]` — toggle terse mode for the session.
 *   - Natural-language activation ("be laconic", "less tokens", "normal mode").
 *   - Per-turn system-prompt injection scaled by intensity.
 *   - A `laconic:<mode>` statusline indicator.
 *   - Per-project persistence in `.pi/laconic-mode.json`.
 */

import type {
  ExtensionAPI,
  ExtensionContext,
} from "@earendil-works/pi-coding-agent";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

type Mode = "off" | "low" | "medium" | "high";

const MODES: readonly Mode[] = ["off", "low", "medium", "high"];
const STATUS_KEY = "laconic";
const STATE_FILE = join(".pi", "laconic-mode.json");

const INTENSITY: Record<Exclude<Mode, "off">, string> = {
  low: "Drop filler, hedging, and pleasantries. Keep full sentences and articles.",
  medium:
    "Drop articles, filler, pleasantries, and hedging. Sentence fragments are fine.",
  high: "Extreme compression. Bare fragments. Abbreviate prose words; use arrows (X -> Y). Never pad.",
};

const ACTIVATE_RE =
  /\b(laconic mode|be laconic|use laconic|talk like a spartan|less tokens|fewer tokens|save tokens|be brief)\b/i;
const DEACTIVATE_RE = /\b(normal mode|stop laconic|disable laconic|verbose mode)\b/i;

const FALLBACK_BODY = [
  "## Rules",
  "- Simplest common word over longer synonym. One word over a phrase.",
  "- Answer or diagnosis first. Reason only if the reader cannot derive it.",
  "- Cut filler, hedging, pleasantries, and preamble.",
  "- Never repeat a point; restatement is disguised filler.",
  "- Keep technical terms, code, and exact strings verbatim.",
  "- Response length inversely proportional to input length.",
  "- Be laconic.",
  "",
  "## Pattern",
  "```text",
  "[problem]. [fix].",
  "```",
].join("\n");

/** Read `## Rules` + `## Pattern` from the sibling SKILL.md, stripping front-matter. */
function loadSkillContract(): string {
  try {
    const here = dirname(fileURLToPath(import.meta.url));
    const skillPath = join(here, "..", "skills", "laconic", "SKILL.md");
    const raw = readFileSync(skillPath, "utf8");
    const parts = raw.split("---");
    const body = parts.length >= 3 ? parts.slice(2).join("---") : raw;
    const extracted = extractSections(body, ["## Rules", "## Pattern"]);
    return extracted || FALLBACK_BODY;
  } catch {
    return FALLBACK_BODY;
  }
}

function extractSections(body: string, headings: readonly string[]): string {
  const wanted = new Set(headings);
  const collected: Record<string, string[]> = {};
  let current: string | null = null;
  for (const line of body.split("\n")) {
    const stripped = line.trimEnd();
    if (stripped.startsWith("## ")) {
      current = wanted.has(stripped) ? stripped : null;
      if (current) collected[current] = [stripped];
      continue;
    }
    if (current) collected[current].push(line);
  }
  return headings
    .filter((h) => h in collected)
    .map((h) => collected[h].join("\n").trimEnd())
    .join("\n\n");
}

function readProjectMode(cwd: string): Mode {
  try {
    const parsed = JSON.parse(readFileSync(join(cwd, STATE_FILE), "utf8"));
    return MODES.includes(parsed?.mode) ? (parsed.mode as Mode) : "off";
  } catch {
    return "off";
  }
}

function writeProjectMode(cwd: string, mode: Mode): void {
  try {
    mkdirSync(join(cwd, ".pi"), { recursive: true });
    writeFileSync(join(cwd, STATE_FILE), `${JSON.stringify({ mode })}\n`, "utf8");
  } catch {
    /* best-effort persistence; a read-only cwd must not break the turn */
  }
}

export default function laconic(pi: ExtensionAPI): void {
  const contract = loadSkillContract();
  let mode: Mode = "off";

  const refreshStatus = (ctx: ExtensionContext): void => {
    if (!ctx.ui.isInteractive) return;
    ctx.ui.setStatus(STATUS_KEY, mode === "off" ? undefined : `laconic:${mode}`);
  };

  const setMode = (next: Mode, ctx: ExtensionContext): void => {
    mode = next;
    writeProjectMode(process.cwd(), mode);
    refreshStatus(ctx);
  };

  pi.on("session_start", async (_event, ctx) => {
    mode = readProjectMode(process.cwd());
    refreshStatus(ctx);
  });

  pi.registerCommand("laconic", {
    description:
      "Toggle laconic terse-output mode: /laconic [low|medium|high|off] (default medium).",
    handler: async (args: string, ctx: ExtensionContext) => {
      const arg = (args || "").trim().toLowerCase();
      let next: Mode | null = null;
      if (arg === "") next = "medium";
      else if ((MODES as readonly string[]).includes(arg)) next = arg as Mode;

      if (next === null) {
        ctx.ui.notify(
          `laconic: unknown mode '${arg}' — use low|medium|high|off`,
          "info",
        );
        return;
      }
      setMode(next, ctx);
      ctx.ui.notify(mode === "off" ? "laconic: off" : `laconic: ${mode}`, "info");
    },
  });

  pi.on("before_agent_start", async (event, ctx) => {
    const prompt = event.prompt ?? "";
    if (DEACTIVATE_RE.test(prompt)) setMode("off", ctx);
    else if (mode === "off" && ACTIVATE_RE.test(prompt)) setMode("medium", ctx);

    if (mode === "off") return;

    const injection = `\n\n# Laconic mode (${mode})\n${INTENSITY[mode]}\n\n${contract}`;
    return { systemPrompt: event.systemPrompt + injection };
  });
}
