---
name: okr
description: >
  This skill should be used when the agency needs to derive, score, or roll
  up OKRs (Objectives and Key Results). It complements `vision-doc`: where
  vision-doc stores the workspace-level OKRs, this skill handles (1) deriving
  per-project OKRs from the workspace vision when the user picks an idea,
  (2) scoring every phase report against relevant KRs with a green/yellow/red
  `okr_alignment` signal, and (3) rolling up end-of-quarter OKR scores during
  retro. Trigger phrases: "score against OKRs", "derive project OKRs",
  "roll up OKRs", "what's the OKR alignment", or internal invocation by the
  `ceo`, `vision-doc`, or `retro` skills. Part of Wave 1 of v0.3.0 — the
  company release.
metadata:
  version: "0.1.0"
---

# okr — derive, score, roll up

OKRs without scoring are theatre. This skill closes the loop: every phase report gets an `okr_alignment` signal, every close-out rolls project KR progress into workspace VISION, every retro grades the quarter.

## Three entry points

1. **Derive** (on user idea pick) — create `_vision/projects/<slug>.md`.
2. **Score** (on every Chief report) — append `okr_alignment: green|yellow|red|n/a` to the report's gate block.
3. **Roll up** (on retro) — update `_vision/VISION.md > ## Active OKRs` progress lines from the quarter's project score logs.

## Derive flow

**When:** user picks an idea from the top-5 meeting (Wave 2) and the CEO is authoring the project brief.

**Steps:**
1. Read `_vision/VISION.md`.
2. Identify which workspace-level KRs this project plausibly advances (by topic + keyword overlap).
3. Write `_vision/projects/<slug>.md` with the skeleton in `references/project-okr-template.md`. Every project-level KR must trace back to ≥ 1 workspace KR (write the traceback line `_traces_ ← [KR<n.n>]`).
4. Cap at **3 project KRs**. Fewer is fine; more is a smell.
5. File an ADR via the `adr` skill titled `derive-okrs-for-<slug>` with the traceback logic.

## Score flow

**When:** immediately after a Chief reports a gate. The CEO runs score before validating the gate with `gates`.

**Steps:**
1. Read `_vision/VISION.md` + `_vision/projects/<slug>.md`.
2. Select the same 3 KRs that were prepended to the dispatch via `vision-doc > cascade-rules.md`.
3. For each of the 3 KRs, classify progress this report contributes:
   - `green` — the phase measurably advanced this KR.
   - `yellow` — neutral or tangential; no backslide.
   - `red` — the phase **regressed** against this KR (e.g. increased time-to-launch, added non-goal scope).
   - `n/a` — KR does not apply to this phase.
4. Aggregate the 3 KR signals via: worst-case (any `red` → project `red`; else any `yellow` → `yellow`; else `green`).
5. Write the aggregate as `okr_alignment: <color>` to the report's gate block. Record per-KR score lines in `_vision/projects/<slug>.md > ## Score log` (append-only, dated).

See `references/scoring-rules.md` for the classification rubric.

## Roll-up flow

**When:** `/devsecops-agency:retro` at quarter boundary (or when user says "wrap the quarter").

**Steps:**
1. Read every `_vision/projects/*.md > ## Score log` whose closure date falls in this quarter.
2. For each workspace KR, compute a progress signal:
   - `green` — ≥ 2 projects scored green on traced project-KRs AND the quantitative threshold (if any) is met.
   - `yellow` — mixed evidence OR quantitative threshold partially met.
   - `red` — no green evidence OR measurable regression.
3. Append a `## Q<n> progress` block to `_vision/VISION.md` above `## Last updated` with one line per KR and the color.
4. Write `_vision/history/<today>.md` with the full roll-up block.
5. Do NOT auto-retire OKRs — retirement is a user decision at the next top-5 meeting.

See `references/rollup-rubric.md` for aggregation edge cases.

## Contract with other skills

- **`vision-doc`** writes `VISION.md`; this skill reads it and appends `## Q<n> progress`. Never edits mission / OKR definitions — only progress.
- **`ceo`** invokes `okr.score` on every Chief report before `gates.validate`.
- **`gates`** receives `okr_alignment` as an additional signal but does NOT auto-fail a gate on red alignment alone. Council gate + OKR signal aggregate via `gates/references/gate-rules.md` (extended in Wave 1).
- **`retro`** invokes `okr.rollup` once per quarter boundary.
- **`adr`** is invoked on every derive-flow and on every mid-project OKR amendment.

## Write rules

- **Append-only for score logs.** Never edit a past score.
- **Structured rewrite for `projects/<slug>.md > ## Project OKRs`.** Same caps as workspace (≤ 3 Os, ≤ 3 KRs per O).
- **Every KR has an owner.** Owner is a Chief slug or `ceo`. Unowned KRs are rejected at write time.
- **Every score has a cite.** Score log line: `YYYY-MM-DD · phase <n> · [KR<a.b>] <color> — <one-line reason, cite artifact path>`.

## Integration with the CEO skill

CEO SKILL.md section 3 (Executive sessions) will be updated to:
- Run `okr.score` after receiving a Chief report (before `gates.validate`).
- Emit the `okr_alignment` line into the `chat.jsonl > exec-decision` entry.
- If `okr_alignment: red` AND council gate is `green`, escalate a decision item to `inbox.json` (user choice: proceed-with-misalignment vs halt). Record via `adr`.

CEO SKILL.md section 5 (Close-out) will be updated to:
- Run `okr.rollup` if this project's close spans a quarter boundary.
- Attach the project-level KR final scores to the closing memo.

## Anti-patterns

- Scoring every phase `green` because nothing regressed. (Yellow is the default; green requires measurable advance.)
- Deriving 6 project KRs "to be thorough." (Cap = 3.)
- Skipping `okr.score` on a phase because "this phase is infrastructure." (Score with `n/a` if no KR applies — still log it.)
- Auto-retiring an OKR that scored red all quarter. (Retirement is a user decision with ADR.)

## Progressive disclosure

- `references/project-okr-template.md` — exact markdown for `projects/<slug>.md`.
- `references/scoring-rules.md` — green/yellow/red/n/a rubric with examples.
- `references/rollup-rubric.md` — quarter aggregation rules and edge cases.
