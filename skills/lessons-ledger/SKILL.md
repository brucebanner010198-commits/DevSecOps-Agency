---
name: lessons-ledger
description: >
  This skill should be used when a project closes and the CEO needs to append
  a row to the cross-project learning log `LESSONS.md`. The ledger is the
  primary artifact that persists across projects — it feeds idea-pipeline
  adjacency scoring, memory Deep dreaming reads, CAO portfolio audits, and the
  retrospective carry-over check. Trigger phrases: "append to lessons",
  "write the ledger row", "close the project ledger", "update LESSONS.md", or
  the final close-out step of `/devsecops-agency:ceo`. Always invoked after
  `retrospective` writes the retro minutes.
metadata:
  version: "0.1.0"
---

# lessons-ledger — append one row per project close

Read `references/row-schema.md` for the exact field rules. Read `references/append-contract.md` for the append semantics.

## When to trigger

- **Every project close.** After `retrospective` writes the minutes, before `notify` fires the close-shipped or close-blocked event. Mandatory per `MISSION.md > North stars § 5`.
- **Rung-7 park.** When `ladder` transitions a project to Rung 7. Outcome = `parked-rung-7`.
- **Wave close.** Optional. Waves write to `CHANGELOG.md`; the ledger stays project-scoped. Do not append wave rows.

## Inputs

1. `outputs/devsecops-agency/<slug>/status.json` — phase, gates, metrics.
2. `_vision/projects/<slug>.md` — final OKR scores.
3. `_meetings/<slug>-retro-<YYYY-MM-DD>.md` — retro-derived lessons, reusable decisions, what-we'd-change.
4. `_decisions/ADR-NNNN-*.md` — waiver counts, specific ADR IDs.
5. `_vision/playbooks/stones/*.md` — stones authored from this project (if any).
6. `_vision/audit/<slug>-close-audit.md` — CAO's final verdict.

## Output

A new H3 block appended to `LESSONS.md`. Schema in `references/row-schema.md`; exact table layout mirrors the one in `LESSONS.md > ## Row schema`.

## Process

1. **Verify preconditions.** `retrospective` has landed (the retro file exists and contains all 10 sections). CAO close-audit has landed. If either is missing, abort and log `blocked — pending <which>`.
2. **Read inputs.** Every file above, in order.
3. **Compute fields.** See `references/row-schema.md > ## Field derivation`.
4. **Check append contract.** See `references/append-contract.md`. Reject if slug already has a ledger row (corrections = new row, not edit).
5. **Write the row.** Append-only `Write` with the previous file contents followed by the new H3 block. Never call `Edit` on `LESSONS.md` — append-only (`VALUES.md §4`).
6. **Sort on write.** New row goes at the bottom; rows remain sorted by `closedAt` ascending. Sort on every write to enforce — the sort is a no-op if the new row is the most recent.
7. **File ADR.** `_decisions/ADR-NNNN-lessons-<slug>.md` kind `lessons-append`. Cites the new row's section heading.
8. **Update `_memory/index.json`.** Add a cross-ref pointer from `patterns/<slug>.md` → `LESSONS.md > <slug>-<date>`.
9. **Return.** One-line confirmation to the CEO with the row's H3 anchor.

## Skill index entry

Register in `skills/AGENTS.md > ## Skill index`:

```
| `lessons-ledger` (v0.3.8) | Append-only cross-project learning log LESSONS.md. CEO invokes on every close after retrospective. |
```

## Read paths (informational — these other skills read the ledger)

- `skills/idea-pipeline/SKILL.md` → reads ledger for adjacency scoring during idea screening.
- `skills/memory/SKILL.md` (Deep dreaming) → cross-references ledger row from `patterns/<slug>.md`.
- `skills/retrospective/references/carry-over-check.md` → reads last-3 rows for the carry-over Jaccard.
- `skills/audit/SKILL.md` → reads full ledger for portfolio audit.
- `skills/ceo/SKILL.md` → reads latest-5 rows at project init.

## Anti-patterns

- **Don't write before `retrospective` lands.** The retro is the source of truth for `lessons`, `reusable decisions`, and `what-we'd-change`. Writing first = empty fields.
- **Don't edit a prior row.** Corrections live in a new row. See `references/append-contract.md > Correction semantics`.
- **Don't write the same slug twice.** If the slug already has a row, the correct move is either (a) a correction row with a different `closedAt` or (b) a new slug suffix. See `references/append-contract.md > Slug collision`.
- **Don't skip the ADR.** Every ledger append files an ADR. No ADR = CAO red at next portfolio audit.
- **Don't write longer than 120 chars per field.** Long detail lives in the retro minutes and `_memory/patterns/<slug>.md`. The ledger is the scan-me-fast index.
- **Don't write wave rows.** Waves live in `CHANGELOG.md`. Mixing project + wave rows breaks the schema.

## Progressive disclosure

- `references/row-schema.md` — exact field schema, table layout, derivation rules.
- `references/append-contract.md` — append semantics, correction rows, slug collision policy.
- `references/examples.md` — three worked examples (shipped / blocked / parked-rung-7).
