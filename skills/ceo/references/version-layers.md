# version-layers.md — cumulative invariants

Each release layer is still in effect. The CEO playbook in `SKILL.md` is the condensed view; this is the long form.

## v0.3.0-alpha.6 — red-team + self-modifying playbooks (Wave 6)

One new council + two new skills + a blocking prompt-diff review gate give the agency adversarial defense that scales with the system itself:

- **Red-Team Council** — Chief: `red-team-lead` (Sonnet, CRT). Specialists: `adversarial-prompter`, `tool-abuse-tester`, `data-exfil-tester`, `model-poisoning-scout`, `supply-chain-attacker`, `social-engineering-tester`, `playbook-author`. Informing + **independent** — same structural invariant as Audit + Eval. Never on any project's delivery path. Outputs live in `<slug>/red-team/` (per-project) and `_vision/playbooks/` (portfolio stones).
- **`red-team`** — OWASP ASI Top 10 (2025) mapping across all five kinds: pre-release (every ship, parallel with close-audit + close-eval), prompt-upgrade (every `agents/*.md` or `councils/*/AGENTS.md` edit — blocking via prompt-diff review), integration (every new tool / skill / MCP / model-family swap), portfolio-sweep (quarterly), incident (on demand after a live breach or near-miss). Severity rubric = reproducibility × impact × boundary × mitigation → critical/high/medium/low/info. Severity → gate → ladder routing in `skills/red-team/references/severity-gate-map.md` (default Rung 3; only Rung 6 accepts-without-fix). Attack catalogs per specialist in `skills/red-team/references/attack-catalogs.md`. Canonical credential regexes + memory-contamination scans in `skills/red-team/references/owasp-asi-top-10.md`. CRT never on delivery path.
- **`playbook`** — DGM-style stepping-stone archive under `_vision/playbooks/`. One stone per remediated `high`+ red-team finding. Stone file = `stones/stone-NNNN-<slug>.md`; registry = `ARCHIVE.md`. Stone YAML: `id · slug · asi · severity · hardened_skill · adr · created · superseded_by`. Stones are **immutable** — the only allowed mutation is the single `superseded_by:` pointer field. Supersession / augment / deprecate rules in `skills/playbook/references/supersession-rules.md`. Stone abstraction rules (no instance-specific patterns) in `skills/playbook/references/stone-authoring.md`. ARCHIVE.md table format + 500-row/quarter cap in `skills/playbook/references/archive-format.md`.
- **Prompt-diff review** — blocking gate run by `playbook-author` on every proposed `agents/*.md` or `councils/*/AGENTS.md` diff before it lands. Matches diff against `ARCHIVE.md` via `hardened_skill` field + ASI category. Weakening phrasing patterns auto-reject: `Never → Should not`, `Must → Should`, `Required → Recommended`, `forbidden → discouraged`, `critical → important`, `always → usually`, quantified thresholds relaxed, invariants downgraded to guidelines. Rejections auto-rollback the diff — never land, never enter the ladder.

Invariants added in Wave 6 (cumulative 1-14 in SKILL.md; 28-32 below):

28. Every project close runs CRT pre-release red-team in parallel with CAO close-audit + CEVO close-eval. All three mandatory before archival. CRT reds block ship per severity-gate-map; only Rung 6 user-waiver waives them.
29. Every `agents/*.md` or `councils/*/AGENTS.md` edit runs prompt-diff review before it lands. Weakening-phrasing diffs auto-reject and auto-rollback; rejected diffs do not enter the ladder. New stones must be authored before a rejected diff can be re-applied.
30. Every remediated `high`+ red-team finding authors an immutable stepping-stone. Stone body never edits after acceptance. Supersession is the only allowed evolution; `supersedes:` on the new stone + single-field `superseded_by:` on the old stone, both covered by an ADR.
31. CRT + every red-team specialist cannot dual-hat with any delivery role (CTO/VP-Eng/CISO/CQO/CEVO/CAO). A red-team specialist red-teaming a project they delivered requires a blind-peer-review gate. Independence breaches are automatic critical findings + CAO reds.
32. Real PII / credential exfil during red-team tests is an automatic critical finding. Use synthetic fixtures from `skills/red-team/references/owasp-asi-top-10.md > credential regexes`. Tests that exfil real data are treated as the breach they simulate.

## v0.3.0-alpha.5 — evaluation + budget (Wave 5)

One new council + two new skills + one reusable compaction capability give the agency a mandatory quality check and a first-class cost signal:

- **Evaluation Council** — Chief: `evaluation-lead` (Sonnet, CEVO). Specialists: `eval-designer`, `benchmark-runner`, `regression-detector`, `budget-monitor`, `token-compactor`. Informing + independent. Never on any project's delivery path. Outputs live in `<slug>/eval/` (per-project) and `_vision/eval/` (portfolio).
- **`eval`** — close-eval (mandatory on every ship, in parallel with close-audit), portfolio-regression (per quarter, 5 pp threshold), benchmark-sweep (SWE-bench-lite + MLE-bench-lite + per-project harnesses), compaction-check (token-compactor structural rewrite review). Eval items derive from PKRs at close time — never from shipped artifacts. ≤ 25 items per set across three tiers (functional / ux / promise). Per-tier shapes + rejection patterns + subjectivity budget (max 30 % promise-tier) in `skills/eval/references/eval-set-rubric.md`. Baselines freeze per quarter; unfrozen baselines are a regression-detector hard error.
- **`budget`** — four size classes (`small` 75 k/$1.50, `medium` 250 k/$5, `large` 1 M/$20, `custom`). Per-phase allocation defaults in `skills/budget/SKILL.md`. Burn tracked on every Chief report into `<slug>/eval/budget-ledger.md`. Thresholds: phase WARN at 20 % overrun, cumulative STOP + Rung 6 at 110 %. Per-model costs in `skills/budget/references/cost-table.md`. Size-class decision tree + re-class ADR rules in `skills/budget/references/size-class-calibration.md`.

Token-compactor contract: **structured rewrite, never delete.** Emits a `[rollup]` entry spanning the compacted range + a `[correction]` pointer at the original location. Never-compact list: decisions, errors, reports, ADR-refs, worktree lines, survived-novelty-gate writes, meeting lines, rung transitions, any entry under 48 h old.

Invariants added in Wave 5 (cumulative 1-12 in SKILL.md; 23-27 below):

23. Every project close runs a mandatory close-eval in parallel with the close-audit. Reds (regression ≥ 5 pp unresolved) block ship until root-cause tagged (one of `prompt-rot · tier-drift · skill-edit · budget-squeeze · input-drift · baseline-defect · unknown`).
24. Eval items are derived from PKRs before ship, never retrofitted from what was actually built. Retrofit detection → eval-designer files an error + escalates to CEVO.
25. Regression baselines freeze per quarter. Never update a baseline mid-quarter; mid-quarter changes require a baseline-update ADR at quarter boundary.
26. Every project declares a budget (size class + per-phase allocation) at OKR derivation. Later class changes require an ADR citing the trigger in `skills/budget/references/size-class-calibration.md > ## Triggers to re-class mid-flight`.
27. Rung 6 is the only ladder rung that can expand a project budget. All other rungs operate within the declared envelope; exhaustion at any rung ≠ Rung 6 climbs the ladder, it does not silently borrow tokens.

## v0.3.0-alpha.4 — resilience ladder (Wave 4)

One new skill wires the agency's never-give-up rule into the existing state machine without letting token spend go unbounded:

- **`ladder`** — 8 rungs from `Retry with refreshed context` (0) → `Fix-loop` (1, existing 2-attempt cap) → `Alternate approach within scope` (2) → `Cross-council escalation` (3) → `Hire / repurpose a specialist (COO)` (4) → `Scope pivot (CPO + user)` (5) → `User consult` (6) → `Parking lot` (7). Per-rung owners, budgets, entry/exit signals in `skills/ladder/references/rung-rules.md`. Task state × blocker kind → starting rung in `skills/ladder/references/ladder-matrix.md`.

Taskflow contract change: `status.json > tasks[].ladderRung` field seeded from the matrix when state becomes `blocked`. Fix-loop cap now feeds Rung 2, not a dead-end. `metrics.rungAttempts[rung_N]` + `metrics.ladderClimbs` + `metrics.ladderMeanTime` logged to `status.json > metrics`.

Gates contract change: blocking-council reds do not durably ship-block. They start the ladder. Durable block only after Rung 6 user-waiver refusal + Rung 7 park.

Invariants added in Wave 4 (cumulative 1-10 in SKILL.md; 18-22 below):

18. Never give up below Rung 7. Every blocked task climbs until shipped, superseded, pivoted, or parked with reconsider-trigger.
19. Every rung transition files an ADR. Upward rung skips require an ADR citing an exception in `ladder-matrix.md > Routing rules`.
20. Rung 7 preserves everything. Artifacts, session logs, worktree branches, partial commits stay; parking is resumable.
21. Rung 6 is bounded — 7-day user-response timeout auto-advances to Rung 7.
22. `metrics.fixLoops` counts only Rung 1 attempts. Rung 2+ goes in `metrics.rungAttempts[rung_N]`. Misclassification rots audit signals.

## v0.3.0-alpha.3 — people-ops + audit (Wave 3)

Two new councils + three new skills give the agency a self-modifying roster and an independent integrity check:

- **People-ops Council** — Chief: `coo` (Sonnet). Specialists: `roster-manager`, `hiring-lead`, `performance-reviewer`. Informing council. Outputs live in `_vision/roster/`. Convened by CEO at project kick-off/close, quarter roll-up, REM retro, and on 2-attempt fix-loop-cap hit within 30 days.
- **Audit Council** — Chief: `cao` (Sonnet). Specialists: `adr-auditor`, `gate-auditor`, `okr-auditor`, `memory-auditor`. Independent — never in any project's delivery path. Outputs live in `_vision/audit/`. Close-audit mandatory on every ship; portfolio-audit mandatory per quarter.
- **`roster`** — census.md (alphabetical agent table), performance.md (30/90d ratings), proposals.md (hire/fire/tier-change/repurpose/prompt-upgrade), coo-brief.md (synthesis). Archives in `_vision/roster/_archive/`.
- **`audit`** — 4 audit kinds (close, portfolio, pre-release, incident). Every red files an ADR in the same CEO turn. Every yellow pairs with a taskflow task. Machine-checkable rows walk every entry — no sampling.
- **`capacity`** — per-agent bands (idle/low/healthy/hot/overloaded) + per-council parallel utilization + KR coverage gaps.

Invariants added in Wave 3 (cumulative 1-8 from Waves 1-3 in `SKILL.md`):

11. Never skip a close-audit. `audit` is mandatory on every project close; CEO cannot archive without green/yellow audit.
12. Never mutate an agent's `agents/<name>.md` prompt without an ADR proposing the change and `skill-creator` executing it.
13. Never fire a blocking-council agent (`security-lead`, `gc`, or their specialists) without a user-signed waiver in `inbox.json`.
14. Never propose a tier downgrade. `skills/model-tiering/SKILL.md` forbids it; propose prompt upgrade instead.
15. Never delete a retired agent file. Preserve in `_vision/roster/_archive/<name>.md` with redirect line and frozen "Original prompt" block.
16. Audit Council is read-only on the records being audited. Corrections flow through new ADRs or `[correction]` session-log lines — never revert, never rewrite.
17. No Audit specialist may also be in any project's delivery path. Independence violation → pause audit + file breach ADR + reassign via COO.

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

Waves 3–7 extend: people-ops + audit (Wave 3, shipped), never-give-up ladder (Wave 4, shipped), eval + benchmark + budget (Wave 5, shipped), red-team + self-modifying playbooks (Wave 6), SRE + tool-scout + provenance (Wave 7).

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
