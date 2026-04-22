# LESSONS.md — cross-project lessons ledger

Root document. Append-only. One row per project close. Written by the CEO via [`skills/lessons-ledger/SKILL.md`](skills/lessons-ledger/SKILL.md) after CAO close-audit, CEVO close-eval, and CRT pre-release red-team all land.

Not a retro (retros live in `_meetings/<slug>-retro-*.md`). Not a memory file (memory lives in `_memory/`). This is the **cross-project ledger** — the thing future CEO sessions read to know what past runs of the agency learned.

## Contract

- **One row per shipped project.** Blocked projects and Rung-7 parked projects also emit a row, flagged accordingly.
- **Append-only.** Never edit a prior row. Corrections live in a new row that cites the original.
- **Terse.** ≤ 120 chars per field. Long detail goes in `_memory/patterns/<slug>.md` or the retro minutes.
- **Cited.** Every claim references an ADR, a stone, a session log, or a retro minute.
- **Deterministic order.** Rows sorted by `closedAt` ascending. Newest at the bottom.

## Row schema

One Markdown H3 block per row:

```
### <slug> — <closedAt ISO date>

| Field | Value |
| --- | --- |
| outcome | shipped / blocked / parked-rung-7 |
| council-lead ship | <CISO gate>, <GC gate> |
| okr-alignment final | green / yellow / red |
| rungs traversed | e.g. 0, 1-2, 1-5, 7 |
| fix-loops (sum) | <n> |
| waivers | <count> — see ADRs |
| stones authored | <count> — paths or none |
| lessons | <= 3 bullets, each cited |
| reusable decisions | <= 2 bullets citing ADRs to reuse |
| what we'd change | <= 2 bullets |
| next-run trigger | <condition that would resurrect this project> |
```

### Field rules

- **outcome** — exactly one of `shipped`, `blocked`, `parked-rung-7`. No other values. `blocked` means the project never reached Ship phase; `parked-rung-7` means it reached Rung 7 with preserved artifacts.
- **council-lead ship** — the final gate colour for CISO and GC only. Format: `CISO=green, GC=green`. `-` for never-reached.
- **okr-alignment final** — the final value from `_vision/projects/<slug>.md > ## Closed > alignment`. `n/a` for pre-OKR legacy projects.
- **rungs traversed** — list of ladder rungs hit. `0` means never escalated past fix-loop-cap. `1-5` means walked rungs 1 through 5.
- **fix-loops (sum)** — integer total across all `(council, phase)` pairs. From `status.json > metrics.fixLoops`.
- **waivers** — count of ADRs with `kind: waiver` filed in this project. List the ADR numbers.
- **stones authored** — count + paths of stepping-stones authored from this project's red-team findings. `0` / `none` for clean projects.
- **lessons** — the thing we learned. Each bullet cites an artifact (`ADR-0042`, `_memory/patterns/<slug>.md:§Recurring risks`, `_meetings/<slug>-retro-<date>.md:§Lessons`).
- **reusable decisions** — decisions with cross-project value. Usually cite an ADR. Read by `idea-pipeline` during next-run adjacency scoring.
- **what we'd change** — honesty about where the agency ran poorly. Fuels next-wave skill edits.
- **next-run trigger** — a condition that would make the user want to revisit this project. For parked-rung-7 projects, this is mandatory; for shipped projects, often `-`.

## Read paths

- **`idea-pipeline`** reads the ledger when scoring new-project adjacencies against past lessons.
- **`memory`** (Deep dreaming at project close) writes `_memory/patterns/<slug>.md` and cross-references the ledger row.
- **`retrospective`** reads prior ledger rows to check whether any "what we'd change" from the last 3 projects carried into this one unchanged (a CAO red if so).
- **`ceo`** reads the latest 5 rows at session start of any new project under the same slug root.
- **`cao`** runs `audit` across the whole ledger on portfolio-audit cadence.

## Write path

The CEO invokes `skills/lessons-ledger/SKILL.md` as the last step of close-out — after `memory.deep`, after retro minutes, before the notify. The skill:

1. Reads `status.json`, `_vision/projects/<slug>.md`, the retro minutes, and the ADR list for the project.
2. Drafts the row per the schema above.
3. Writes via append (never edit).
4. Files an ADR `_decisions/ADR-NNNN-lessons-<slug>.md` citing the written row.

## Anti-patterns

- **Don't write the row before close-audit lands.** Reds on close-audit can flip "shipped" to "blocked" on late findings. Wait for the audit.
- **Don't write generic lessons.** "We learned more about X" is noise. Lessons cite a specific file line and describe a behaviour to replicate or avoid.
- **Don't edit a prior row to "correct" it.** File a new row. Prior rows are preserved. `VALUES.md §4` (append-only).
- **Don't skip the row because "the project went fine."** A project that shipped with zero waivers, zero stones, and zero rungs is still a row — the lesson is *what made that happen*.
- **Don't split a row across multiple H3 blocks.** One H3 per project, one table per H3. The parser (and the eye) reads by H3 → table.
- **Don't write more than 3 lessons bullets.** Long ledgers bloat the read-at-session-start path. Detail goes in retro minutes and `_memory/patterns/`.

## Starter state

Empty — this repo has not shipped an end-user project yet. The first row will be appended when the first `/devsecops-agency:ceo <idea>` run closes.

See also: [`MISSION.md`](MISSION.md), [`VALUES.md`](VALUES.md), [`skills/lessons-ledger/SKILL.md`](skills/lessons-ledger/SKILL.md), [`skills/retrospective/SKILL.md`](skills/retrospective/SKILL.md).
