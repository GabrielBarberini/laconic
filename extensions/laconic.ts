/**
 * Laconic — pi extension driving the laconic skill. Pi-only.
 *
 * One switch: full laconic or off.
 *   - `/laconic [on|off]` — toggle (no arg flips).
 *   - Natural-language triggers ("be laconic", "less tokens", "normal mode").
 *   - Injects the rules into the system prompt while on.
 *   - `laconic` statusline; per-project state in `.pi/laconic-mode.json`.
 */

import type {
  ExtensionAPI,
  ExtensionContext,
} from "@earendil-works/pi-coding-agent";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const STATUS_KEY = "laconic";
const STATE_FILE = join(".pi", "laconic-mode.json");

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

function readProjectState(cwd: string): boolean {
  try {
    const parsed = JSON.parse(readFileSync(join(cwd, STATE_FILE), "utf8"));
    return parsed?.active === true;
  } catch {
    return false;
  }
}

function writeProjectState(cwd: string, active: boolean): void {
  try {
    mkdirSync(join(cwd, ".pi"), { recursive: true });
    writeFileSync(join(cwd, STATE_FILE), `${JSON.stringify({ active })}\n`, "utf8");
  } catch {
    /* best-effort; a read-only cwd must not break the turn */
  }
}

export default function laconic(pi: ExtensionAPI): void {
  const contract = loadSkillContract();
  let active = false;

  const refreshStatus = (ctx: ExtensionContext): void => {
    if (!ctx.ui.isInteractive) return;
    ctx.ui.setStatus(STATUS_KEY, active ? "laconic" : undefined);
  };

  const setActive = (next: boolean, ctx: ExtensionContext): void => {
    active = next;
    writeProjectState(process.cwd(), active);
    refreshStatus(ctx);
  };

  pi.on("session_start", async (_event, ctx) => {
    active = readProjectState(process.cwd());
    refreshStatus(ctx);
  });

  pi.registerCommand("laconic", {
    description: "Toggle laconic mode: /laconic [on|off].",
    handler: async (args: string, ctx: ExtensionContext) => {
      const arg = (args || "").trim().toLowerCase();
      let next: boolean;
      if (arg === "") next = !active;
      else if (arg === "on") next = true;
      else if (arg === "off") next = false;
      else {
        ctx.ui.notify(`laconic: unknown argument '${arg}' — use on|off`, "info");
        return;
      }
      setActive(next, ctx);
      ctx.ui.notify(active ? "laconic: on" : "laconic: off", "info");
    },
  });

  pi.on("before_agent_start", async (event, ctx) => {
    const prompt = event.prompt ?? "";
    if (DEACTIVATE_RE.test(prompt)) setActive(false, ctx);
    else if (!active && ACTIVATE_RE.test(prompt)) setActive(true, ctx);

    if (!active) return;

    return {
      systemPrompt: `${event.systemPrompt}\n\n# Laconic mode\n\n${contract}`,
    };
  });
}
