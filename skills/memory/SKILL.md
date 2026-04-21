---
name: memory
description: >
  This skill should be used when the agency needs to read or write durable
  memory — cross-phase, cross-project, cross-session. The CEO and Chiefs
  invoke it at three moments: (1) project init to pull relevant prior
  learnings into the brief; (2) phase completion to roll up new facts
  (Light dreaming); (3) project close to consolidate the project into a
  pattern file (Deep dreaming). A fourth entry, REM dreaming, runs on
  `/devsecops-agency:retro` to extract cross-project patterns. Trigger
  phrases: "pull memory", "check prior learnings", "run dreaming",
  "consolidate this project", "extract patterns", or internal invocation
  by the `ceo` skill.
metadata:
  version: "0.1.0"
---

# memory — durable agency learning

Three-tier consolidation (Light / Deep / REM), append-only writes, grep-first retrieval. Ported pattern from openclaw's `memory-host-sdk/dreaming.ts`.

## Storage layout

All memory lives under `/sessions/loving-adoring-maxwell/mnt/outputs/devsecops-agency/_memory/`:

```
_memory/
├── MEMORY.md                  # durable preferences + cross-project patterns (REM output)
├── memory/
│   └── YYYY-MM-DD.md          # dated facts (Light dreaming output)
├── patterns/
│   └── <project-slug>.md      # per-project consolidated learnings (Deep dreaming output)
└── index.json                 # lightweight index: {projects, agents, lastDream, byAgent}
```

Append-only. Never overwrite an existing line — add new entries with a timestamp.

## Three tiers

### Light dreaming — per phase

**When:** after any phase completes (before the next phase starts).
**Input:** the artifacts listed in `status.artifacts` for the phase that just finished + the phase's meeting entries from `chat.jsonl`.
**Output:** 3–7 bullet points appended to `_memory/memory/<today>.md` under a `## <slug> · phase <n>` header.
**Knobs** (see `references/dreaming-config.md`): `lookback_days=1`, `dedupe_similarity=0.85`, `max_bullets=7`.

Bullet format: `- [facts|risk|decision|pattern] <one line>` e.g. `- [pattern] Stripe webhook replay requires idempotency key in custom metadata`.

### Deep dreaming — per project close

**When:** Phase 7 (close) of a project.
**Input:** full project folder — brief, research, architecture, threat-model, qa-report, deploy, retro notes.
**Output:** a single file at `_memory/patterns/<slug>.md` with five sections: **What shipped · What worked · What was gated · Recurring risks · Reusable decisions**.
**Knobs:** `recency_half_life_days=14`, `recovery_enabled=true`, `recovery_trigger_below_health=0.6`, `recovery_auto_write_min_confidence=0.75`.

If the project was blocked or abandoned, still write the file — the `What was gated` and `Recurring risks` sections are where the value is.

### REM dreaming — cross-project

**When:** user runs `/devsecops-agency:retro` with no active project, or explicitly asks "run REM dreaming" / "extract patterns".
**Input:** every file under `_memory/patterns/` + existing `MEMORY.md`.
**Output:** appended bullets in `MEMORY.md` under the correct section: **Preferences (from user) · Recurring risks · Proven stacks · Anti-patterns · Open questions**.
**Knobs:** `min_pattern_strength=0.7` (a pattern must appear in ≥ 2 project files to be written).

Do not duplicate a pattern already present in `MEMORY.md` — check first, or quote the existing line.

## Read path (retrieval)

At project init, the CEO runs this before intake:

1. Read `_memory/MEMORY.md` top-to-bottom (always small enough).
2. `rg -l "<keywords from idea>" _memory/patterns/` to find relevant prior projects.
3. For the top 1–3 matches, read the section headers only.
4. Inject a "## Prior learnings" section into `brief.md` with the 3–6 most relevant bullets and file-path citations.

See `references/retrieval.md` for the exact grep recipes.

## Write policy

- **Append-only.** Never rewrite a line. Add new timestamped entries instead.
- **Opt-in implicit.** The Cowork outputs folder is a private workspace — writes are allowed by default. If the user explicitly says "don't remember this project", skip all writes for that slug.
- **Redact.** Strip emails, tokens, API keys, customer PII before writing. If the fact requires a secret to be useful, write the fact without the secret and note "requires secret" instead.
- **Cite.** Every bullet in `patterns/<slug>.md` must reference the source file by project-relative path (e.g. `security/pentest-report.md:42`).
- **Deterministic ordering.** When assembling a list of facts for the model, sort by section, then by timestamp ascending. (Prompt-cache hit.)

See `references/write-policy.md` for the full rules.

## Integration with the CEO skill

The CEO playbook (`skills/ceo/SKILL.md`) calls this skill at four moments:

| Moment                    | Tier | What gets written                          |
| ------------------------- | ---- | ------------------------------------------ |
| Project init (before intake) | — (read only) | "Prior learnings" section in `brief.md`  |
| After each phase          | Light | New bullets in `memory/<today>.md`         |
| Project close (Phase 7)   | Deep  | New file `patterns/<slug>.md`              |
| On `/retro` (no active project) | REM | Appended bullets in `MEMORY.md`          |

Log every memory write as a `scope:"memory"` entry in the active project's `chat.jsonl` so the command-center shows it.

## Progressive disclosure

- `references/dreaming-config.md` — the exact knob defaults and when to tune them
- `references/write-policy.md` — append-only rules, redaction, opt-out
- `references/retrieval.md` — grep recipes for the read path
