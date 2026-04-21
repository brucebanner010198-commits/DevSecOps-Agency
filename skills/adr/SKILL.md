---
name: adr
description: >
  This skill should be used whenever the agency makes a **material decision**
  — anything the CEO would want to justify to a future self or to an auditor.
  It writes architecture decision records (ADRs) in `_decisions/ADR-NNNN-<slug>.md`
  with a fixed, reviewable format. The CEO invokes it on: (1) every user
  meeting outcome (idea picked, scope cut, go/no-go); (2) every hire, fire,
  or repurpose of an agent; (3) every scope change or mid-project OKR
  amendment; (4) every waiver of a council gate; (5) every technology choice
  with non-trivial reversal cost; (6) every vision-doc mutation. Trigger
  phrases: "file an ADR", "record the decision", "why did we pick X",
  "document this trade-off", or internal invocation by any skill with a
  material decision. Part of Wave 1 of v0.3.0 — the company release.
metadata:
  version: "0.1.0"
---

# adr — decision receipts

If it's worth arguing about, it's worth writing down. ADRs are the agency's paper trail of decisions — CEO to auditor to retro to future-you.

## Storage layout

All ADRs live under `/sessions/loving-adoring-maxwell/mnt/outputs/devsecops-agency/_decisions/`:

```
_decisions/
├── ADR-0001-<slug>.md
├── ADR-0002-<slug>.md
├── ...
└── INDEX.md               # generated: ADR number, title, status, date, one-line summary
```

Numbering is workspace-global, zero-padded to 4 digits, monotonic. Never re-use a number. Never skip. The CEO (or any invoker) derives the next number by `max(existing) + 1`.

## ADR file format

Exactly this shape, every ADR:

```markdown
# ADR-NNNN: <title — imperative, ≤ 10 words>

- **Status:** proposed | accepted | rejected | superseded-by-ADR-MMMM | reversed
- **Date:** YYYY-MM-DD
- **Author:** <actor — `ceo` / `cro` / etc.>
- **Related:** ADR-XXXX (if any) | `_vision/VISION.md` section | project slug
- **Project:** <slug> | workspace

## Context

<1–3 short paragraphs. The problem. The forces at play. What's at stake.>

## Decision

<1 short paragraph. The call, in active voice. "We will...", not "It is recommended...".>

## Consequences

### Positive
- <one line>
- <one line>

### Negative
- <one line>
- <one line>

### Reversibility
- <one line: "reversible in X" or "one-way door" with the cost>

## Alternatives considered

- **<Alt A>** — <why not>
- **<Alt B>** — <why not>

## Follow-ups

- <concrete task, owner, due date>
- <concrete task, owner, due date>
```

Cap: **120 lines of markdown per ADR.** If an ADR is longer, it's likely conflating multiple decisions — split.

## When to file an ADR (triggers, not exhaustive)

- **User meeting outcome** — idea picked, scope cut, go/no-go, ETA committed.
- **Hire / fire / repurpose** — creating a new agent via skill-creator, retiring an agent, moving a specialist to a different council.
- **Scope change** — adding or removing a phase, adding a council, moving work across projects.
- **Waiver** — any council gate overridden (security waiver, legal waiver). Mandatory.
- **Vision mutation** — any edit to `_vision/VISION.md` (mission, OKR, non-goal).
- **Technology choice** with reversal cost > 1 day of rework.
- **Non-goal violation** — any time the CEO proceeds with work that touches a declared non-goal.
- **Regression acceptance** — any time OKR alignment is `red` and the CEO (with user) chooses to proceed.

If you're arguing whether to file one, file one.

## Status lifecycle

- `proposed` — written but not yet executed on. Rare — most ADRs are filed at decision time with `accepted`.
- `accepted` — decision made, executing or executed.
- `rejected` — the alternative won; kept for the record.
- `superseded-by-ADR-MMMM` — a later ADR replaces this one. The replacement explicitly names the predecessor in `Related:`.
- `reversed` — the decision was undone without a replacement (rare; implies learning).

Status changes are edits to the ADR header. Every edit appends a one-line `## Status history` section at the bottom:

```
## Status history
- YYYY-MM-DD: proposed → accepted (ceo)
- YYYY-MM-DD: accepted → superseded-by-ADR-0027 (ceo)
```

The body of an ADR is **immutable after acceptance** except for the status header and status-history block. Need to change the substance? File a new ADR that supersedes.

## INDEX.md

Generated (and regenerated) by the `adr` skill on every write. Shape:

```markdown
# ADR index

| #    | Title                                   | Status       | Date       | Project     |
| ---- | --------------------------------------- | ------------ | ---------- | ----------- |
| 0001 | Use Sonnet for all Chiefs               | accepted     | 2026-04-21 | workspace   |
| 0002 | Launch order: tracker before journal    | accepted     | 2026-04-22 | workspace   |
| 0003 | Waiver: skip a11y gate for internal MVP | accepted     | 2026-04-23 | tracker     |
```

INDEX.md is always sorted by ADR number ascending. Never manually edited.

## Integration with other skills

- **`vision-doc`** — every `VISION.md` mutation writes an ADR + `history/` entry.
- **`okr`** — every mid-project OKR amendment writes an ADR.
- **`gates`** — every waiver (yellow-with-waiver or override) writes an ADR.
- **`ceo`** — every user-meeting decision, hire/fire, scope cut writes an ADR.
- **`meeting-minutes`** — every meeting that produces a decision references the ADR number in its minutes.
- **`retro`** — reads recent ADRs to surface patterns (frequent waivers, frequent reversals = anti-pattern).

## Write rules

- **Atomic writes only.** Create the file, then update INDEX.md, in the same CEO turn.
- **Never delete an ADR.** Even rejected / reversed stay forever.
- **Reference, don't copy.** If two decisions share context, ADR B references ADR A's Context section — does not paste it.
- **Cite artifacts.** Every claim in Context / Decision must cite a file path if the claim originated in a Chief report.
- **No secrets, no PII.** Same redaction rule as `memory`.

## Anti-patterns

- Filing an ADR after the fact ("retrocon") when the decision already happened days ago. Write in-the-moment.
- 1000-line ADRs. Cap is 120 lines. Split.
- Reusing an ADR number. Never.
- "We decided to use React" with no context, no alternatives, no consequences. Reject at write time — at minimum one alternative is required.
- Editing an accepted ADR's body. Supersede with a new one.

## Progressive disclosure

- `references/adr-template.md` — paste-and-fill skeleton with 2 worked examples.
- `references/decision-triggers.md` — the full list of events that mandate an ADR.
- `references/status-lifecycle.md` — status transitions, immutability rules, supersede vs reverse.
