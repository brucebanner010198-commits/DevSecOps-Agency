# version-layers.md — cumulative invariants

Each release layer is still in effect. The CEO playbook in `SKILL.md` is the condensed view; this is the long form.

## v0.3.0-alpha.2 — idea pipeline + user-meeting (Wave 2)

Two new councils + four new skills add portfolio-level ideation and the formal CEO ↔ user convening:

- **Marketing Council** — Chief: `cmo` (Sonnet). Specialists: `positioning-strategist`, `comms-writer`, `brand-guardian`, `growth-analyst`. Per-project outputs to `<slug>/marketing/`; pipeline-mode outputs to `_vision/projects/_pipeline/pipeline-readout.md`. Informing council.
- **Strategy Council** — Chief: `cso` (Sonnet). Specialists: `trend-scout`, `competitive-analyst`, `market-sizer`, `opportunity-ranker`. Portfolio-only; outputs to `_vision/strategy/`. Informing council.
- **`idea-pipeline`** — 4-stage gated pipeline: Ideation (≥15 candidates) → Screening (≤10 survivors per `references/screening-filters.md`) → Deep ranking (per `references/ranking-matrix.md` — RICE · narrative 0.6/0.4 weighting) → Top-5 shortlist.
- **`user-meeting`** — 4-phase flow: Brief (solo pre-read) → Present (Cowork artifact, ≤60s per option, one at a time) → Capture (reflect-back, verbatim constraints) → Commit (ADRs + OKR derivation + taskflow tasks). The only structured agency ↔ user convening.
- **`market-intel`** — canonical shapes for three market artifacts (per-project wedge scan · portfolio sizes · portfolio competitive map). Downstream agents parse by section header.
- **`positioning`** — messaging canvas (audience · promise · proof · wedge · category · elevator ≤ 30 words · messaging hierarchy) + pipeline-mode narrative score rubric (narrative clarity · wedge strength · category fit, 1–5).

Invariants added in Wave 2:

6. Never start a new project with an empty backlog without invoking `idea-pipeline` first (unless the user has explicitly named the idea).
7. Never present ≥ 2 options to the user outside the `user-meeting` 4-phase flow.
8. Never short-circuit the top-5: pipeline runs to 5 one-pagers before user is convened.
9. Never skip the ranker disqualifier (OKR red-alignment or missing upstream artifact) — composite score alone does not qualify.
10. Never draft launch copy before `marketing/positioning.md` lands. Comms-writer always downstream of positioning-strategist.

## v0.3.0-alpha.1 — company foundations (Wave 1)

Four new skills add durable corporate paper trail:

- **`vision-doc`** — `_vision/VISION.md` owns mission + ≤ 5 active OKRs + ≤ 5 non-goals. Bootstrapped on first run per workspace. A 3-bullet KR slice (selected by `vision-doc/references/cascade-rules.md`) prepends to every Chief dispatch context.
- **`okr`** — per-project OKRs derived from workspace VISION into `_vision/projects/<slug>.md`. Every Chief report scored with `okr_alignment: green|yellow|red|n/a` (worst-of-3 aggregation). Quarter roll-up writes progress back into VISION.md.
- **`adr`** — `_decisions/ADR-NNNN-<slug>.md` per material decision. Mandatory triggers: user picks, roster changes, scope changes, waivers, vision mutations, non-trivial tech choices, regression acceptances, non-goal violations. Body immutable after acceptance; supersede via new ADR.
- **`meeting-minutes`** — `_meetings/<date>-<kind>.md` for user / board / blocking-council / red-team / audit / retro convenings. Every action item becomes a `taskflow` task with back-filled task ID.

Invariants (Waves 1-2 cumulative):

1. Never dispatch a Chief without the `## Vision slice` block prepended.
2. Never validate a gate without first invoking `okr.score`.
3. Never land a material decision without filing an ADR in the same CEO turn.
4. Never hold a meeting of the above kinds without writing minutes.
5. Minutes action items and `taskflow` tasks are 1:1 — never one without the other.

Waves 3–7 extend: people-ops + audit (Wave 3), never-give-up ladder (Wave 4), eval + benchmark + budget (Wave 5), red-team + self-modifying playbooks (Wave 6), SRE + tool-scout + provenance (Wave 7).

## v0.2.4 — worktree parallelism

- Parallel dispatches and fix-loops (attempt ≥ 1) write to `<slug>/_worktrees/<chief>-<attempt>/`, not the main tree.
- Lifecycle: allocate → {merged | discarded | stale}. See `skills/worktree/SKILL.md`.
- Merge is **atomic** (all-or-nothing), **scope-checked** (out-of-scope writes bounce), **deterministic** (alphabetical write order).
- Structural conflicts escalate to `inbox.json`. Non-structural merge with a note.
- Per-phase `writes[]` / `reads[]` matrix: `skills/worktree/references/parallel-matrix.md`.

## v0.2.3 — gates + taskflow

- **Gates vocabulary**: `green · yellow · red · n/a`. Nothing else.
- **Blocking councils**: security (CISO) + legal (GC). Their reds block ship unless user waives via `inbox.json`.
- **Informing councils** aggregate into the project gate; CEO may waive after consent.
- **`yellow` requires non-empty `followups[]`.** No silent yellows.
- **Aggregation**: blocking red unwaived → red; any red → red; any yellow → yellow; else green. `n/a` skipped.
- **Task states**: `queued → in-progress → needs-decision → blocked → done/cancelled`. See `skills/taskflow/references/state-machine.md`.
- **Fix-loop cap**: 2 per `(council, phase)`. Attempt 3 forces `blocked`.
- **Handoff invariants**: no `needs-decision` or unblocked `blocked` task; no open worktree for the phase.

## v0.2.2 — scoped AGENTS.md + determinism

Hierarchy:

- Root `AGENTS.md` — repo-wide conventions, gate vocabulary, anti-patterns.
- `agents/AGENTS.md` — persona file shape, dispatch/report contract.
- `skills/AGENTS.md` — SKILL.md shape, progressive disclosure, versioning.
- `councils/<council>/AGENTS.md` — per-council Must / Must not / Gate heuristic.

**Before every Chief dispatch:** quote the matching `councils/<council>/AGENTS.md` Must / Must not / Gate heuristic into the dispatch context. Largest single lever against hallucination.

**Prompt-cache rule:** sort maps/sets/lists/registries/file lists/network results by a stable key (alphabetical for names, timestamp ascending for events) before passing to a model or tool.

## v0.2.1 — durable memory + session logs

- `_memory/` — cross-project. Read at init, Light after each phase, Deep at close, REM on retro.
- `_sessions/<agentId>/<sid>.jsonl` — append-only transcripts. One entry per dispatch / report / handoff / note / error.
- See `skills/memory/SKILL.md`, `skills/session-log/SKILL.md`.

## v0.2.0 — org chart

- CEO + 9 Chiefs + ~28 specialists. Dual-hat: `engineering-lead` covers Architecture + Execution.
- 7-phase board. Sequential where dependent, parallel where disjoint.
