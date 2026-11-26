---
adr: 0011
title: The lessons ledger is a workspace record, and the memory index may be rewritten
status: accepted
date: 2026-11-25
deciders: user (Chairman)
kind: constitution-amend
related: docs/vision/CEO-ENTRY-REVIEW.md (F3, N1-e, Chairman's defaults 1 and 3), CONSTITUTION §5.2, §10
---

# ADR-0011: Workspace lessons ledger and memory index

## Status

**Accepted.** On 2026-11-25 the Chairman accepted the recommended defaults for the open items in `docs/vision/CEO-ENTRY-REVIEW.md` ("Accept all defaults", given in the chat interface). Defaults 1 and 3 change root documents, so they are filed here under §10.2. The §10.3 review roll is below.

## Context

**1. The lessons ledger has no writable home.**
- `AGENTS.md` points every close at the root `LESSONS.md`, and the CEO reads the plugin-root copy at session start.
- Writing it is refused. The guard keeps every write inside the launch folder (B1), and the plugin root is outside it.
- In run N1 the CEO read the plugin-root ledger but wrote a new `LESSONS.md` at the launch root (finding N1-e).
- Claude Code installs each plugin version in its own folder, and its documentation says not to keep state there. So a ledger in the plugin folder would not survive an update even if the guard allowed the write.

**2. The memory index cannot be append-only.**
- §5.2 makes `_memory/**` append-only.
- The `memory` skill rewrites `_memory/index.json` as a structure: cross-references and the `lastRem` marker.
- Only its `knobHistory[]` is written as an append (`skills/memory/references/novelty.md`).

## Decision

1. **Ledger location.** Each workspace keeps its ledger at `outputs/devsecops-agency/LESSONS.md`.
   - The plugin-root `LESSONS.md` stays as the schema and the seed. Agents read it and never write it.
   - A ledger read takes the plugin-root rows, then the workspace rows.
   - A missing workspace ledger is normal on a first run. It is not an `identity-missing` abort; that check needs only the plugin-root file.
   - The ledger is still append-only (§5.2, guard B2).
2. **Memory index.** `_memory/index.json` is exempt from §5.2 and may be rewritten as a structure. Its `knobHistory[]` entries stay append-only.

## Redline (§10.2)

```diff
@@ §5.2 Append-only (VALUES §4)
-- `_memory/**`
+- `_memory/**`, except `_memory/index.json`, which the `memory` skill rewrites as a structure; its `knobHistory[]` entries are append-only
```

```diff
@@ AGENTS.md, Identity + Learning (v0.3.8)
-- **[`LESSONS.md`](LESSONS.md)** — one append-only row per project close. Written via `skills/lessons-ledger/SKILL.md` after `skills/retrospective/SKILL.md` lands the retro minutes.
-- **Session-start invariant:** CEO reads `MISSION.md` + `VALUES.md` + latest 5 rows of `LESSONS.md` before deriving a project slug. Missing any = abort + file ADR `kind: identity-missing`.
+- **[`LESSONS.md`](LESSONS.md)** — one append-only row per project close. Written via `skills/lessons-ledger/SKILL.md` after `skills/retrospective/SKILL.md` lands the retro minutes. The rows are written to the workspace ledger, `outputs/devsecops-agency/LESSONS.md`. The plugin-root file is the schema and seed: read it, never write it. A ledger read takes the plugin-root rows, then the workspace rows (ADR-0011).
+- **Session-start invariant:** CEO reads `MISSION.md` + `VALUES.md` + latest 5 rows of `LESSONS.md` before deriving a project slug. Missing any of the three plugin-root files = abort + file ADR `kind: identity-missing`. A missing workspace ledger is not an abort.
```

The skills that name the write follow the same rule: `ceo` (session start step 2, close step 5), `lessons-ledger` (output and write steps) and `rca`. Skills that only read "`LESSONS.md` rows" (`retrospective`, `rhythm`) take the read rule from `AGENTS.md`.

## Effect on other root documents (§10.2)

- `MISSION.md` and `VALUES.md`: "every close appends ≥ 1 row to `LESSONS.md`" still holds; the row now lands in the workspace ledger. No text change.
- `GOVERNANCE.md`: the "Update `LESSONS.md` (append row)" matrix row is unchanged.
- `RESILIENCE.md`: no effect.
- The plugin-root `LESSONS.md` is not edited. It is append-only, and its header still describes the schema correctly.

## Rollback

Revert this ADR's merge commit. Workspace ledgers already written stay where they are, because they are append-only records; a later ADR would say whether to fold them back.

## Review roll (§10.3)

The reviews are pasted below unedited.
