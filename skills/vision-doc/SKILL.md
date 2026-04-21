---
name: vision-doc
description: >
  This skill should be used when the CEO needs to create, read, or update the
  agency's durable **vision document** — the mission, active OKRs, and
  non-goals that cascade from CEO to every Chief and specialist. The CEO
  invokes it at four moments: (1) first run per workspace (bootstrap
  `_vision/VISION.md`); (2) before every dispatch (read the 3 most relevant
  OKR bullets and prepend them to the Chief's context); (3) after the user
  picks an idea from the top-5 meeting (append a project OKR block); (4) on
  `/devsecops-agency:retro` when the mission or non-goals change. Trigger
  phrases: "set the vision", "update the vision", "cascade the mission",
  "what's our north star", "read the vision doc", or internal invocation by
  the `ceo` skill. Part of Wave 1 of v0.3.0 — the company release.
metadata:
  version: "0.1.0"
---

# vision-doc — the agency's north star

Every real company has a vision doc. So does this one. The CEO owns it; every Chief reads the relevant slice before dispatch; every phase report scores itself against it. Without this skill the agency is a contractor. With it, the agency is a company.

## Storage layout

All vision lives under `/sessions/loving-adoring-maxwell/mnt/outputs/devsecops-agency/_vision/`:

```
_vision/
├── VISION.md              # mission + active OKRs + non-goals (single source of truth)
├── projects/
│   └── <slug>.md          # per-project OKR block derived from VISION (authored via okr skill)
└── history/
    └── YYYY-MM-DD.md      # append-only log of every vision change with rationale
```

`VISION.md` is the **only** file a Chief reads before dispatch. `projects/<slug>.md` is read by the project's CEO session only. `history/` is audit trail — never read at dispatch time.

## VISION.md shape

Exactly four sections, in this order, every time:

```
# devsecops-agency · vision

## Mission
<one sentence — what the agency exists to do>

## Active OKRs (this quarter)
- [O1] <outcome>
  - [KR1.1] <measurable key result>
  - [KR1.2] <measurable key result>
- [O2] <outcome>
  - [KR2.1] <measurable key result>

## Non-goals
- <thing the agency explicitly will not do this quarter>
- <thing the agency explicitly will not do this quarter>

## Last updated
YYYY-MM-DD by <who> — <one-line rationale>
```

Cap: **5 active OKRs, 3 KRs per O, 5 non-goals**. If the count exceeds the cap, the oldest OKR rolls off into `history/` before the new one is written.

## Bootstrap flow (first run per workspace)

Run this once, the first time the CEO executes in a workspace with no `_vision/VISION.md`:

1. If the user has NOT yet had a top-5 meeting, write a provisional `VISION.md` with mission `"Build products and services that make life easier and generate revenue, autonomously, while shipping securely."` and **empty** OKR + non-goal sections.
2. Write `history/<today>.md` with entry `"bootstrap — provisional mission, OKRs deferred to first user meeting"`.
3. Do NOT prompt the user for OKRs at bootstrap. They are set during the first `user-meeting` (Wave 2).

## Pre-dispatch flow (every Chief dispatch)

Before the CEO fires any Task tool dispatch, it runs:

1. Read `_vision/VISION.md` top to bottom.
2. Read the current project's `_vision/projects/<slug>.md` if it exists.
3. Select the **3 most relevant OKR bullets** for the dispatch — relevance measured by keyword overlap with the Chief's phase name + the task's `title`.
4. Prepend a fenced block to the dispatch context:
   ```
   ## Vision slice (read-only, for alignment)
   Mission: <mission from VISION.md>
   Relevant OKRs:
   - <KR-a>
   - <KR-b>
   - <KR-c>
   Non-goals that apply: <0–2 non-goals from VISION.md, only if relevant>
   ```
5. Proceed with the dispatch as described in `skills/ceo/SKILL.md`.

The Chief uses the slice to **self-score** its report against the KRs and must include an `okr_alignment: green|yellow|red|n/a` line in its gate report (scored by the `okr` skill).

## Update flow (after a user meeting or scope change)

When the user picks 1–2 ideas from the top-5 meeting, the CEO:

1. Writes a new `_vision/projects/<slug>.md` via the `okr` skill with per-project Os + KRs derived from the workspace VISION.
2. If the idea introduces a new outcome that belongs at workspace level (e.g. a new revenue line), updates `VISION.md`:
   - Bump the `## Last updated` line.
   - Append the change to `history/<today>.md` with `"<what changed> — <why>"`.
   - If an OKR is being replaced, move the replaced OKR to `history/<today>.md` verbatim before deleting it from `VISION.md`.
3. File an ADR via the `adr` skill documenting the vision change.

Never edit `VISION.md` without a paired `history/` entry and ADR. Never exceed the caps.

## Read path (status + retro)

The `status` skill reads `VISION.md` and prints the mission + active OKRs at the top of every status summary.

The `retro` skill reads `history/*.md` for the current quarter to surface vision drift in its output.

The `okr` skill reads `VISION.md` + `projects/<slug>.md` to score every phase report.

## Write rules

- **Append-only for `history/`.** Never edit a past entry.
- **Structured rewrite for `VISION.md`.** Overwrites allowed, but every overwrite writes a paired `history/<today>.md` entry.
- **One actor.** Only the CEO writes `_vision/`. Chiefs and specialists read.
- **Deterministic order.** Mission → OKRs → Non-goals → Last updated. Same order every write.
- **No PII, no secrets.** Same redaction rule as the `memory` skill.

## Integration with the CEO skill

CEO SKILL.md section 1 (Project init) invokes the bootstrap flow if `_vision/` is missing. Section 3 (Board meetings) invokes the pre-dispatch flow before every Task dispatch. Section 5 (Close-out) invokes the update flow if the project introduced a new outcome.

## Anti-patterns

- Dispatching a Chief without prepending the vision slice. (Strips mission from execution.)
- Editing `VISION.md` without an ADR. (Loses rationale.)
- Writing more than 5 OKRs. (OKR bloat = OKR death.)
- Copying the full VISION.md into every dispatch. (Wastes context — 3 bullets only.)
- Writing an OKR with no KR. (Unmeasurable outcome = not an OKR.)

## Progressive disclosure

- `references/vision-template.md` — exact markdown skeleton + example filled.
- `references/okr-writing-rules.md` — how to write an OKR vs a KPI vs a to-do.
- `references/cascade-rules.md` — which 3 OKRs get selected for which phase.
