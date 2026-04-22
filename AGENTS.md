# AGENTS.md — root rules (telegraph style)

Root rules only. **Read scoped `AGENTS.md` before touching a subtree.** Wave-by-wave history lives in [`CHANGELOG.md`](CHANGELOG.md); this file is the active contract.

## Identity + Learning (v0.3.8)

- **[`MISSION.md`](MISSION.md)** — why the agency exists, who we serve, non-goals, north stars. CEO reads at session start. Non-goal violations in dispatch contexts bounce back.
- **[`VALUES.md`](VALUES.md)** — 11 operating principles. Cited by COO in performance review, by CAO in close-audit, by CRT in prompt-diff review.
- **[`KEEPER-TEST.md`](KEEPER-TEST.md)** — the quarterly fire-readily criterion applied to every non-reserved agent. Invoked via `skills/keeper-test/SKILL.md`.
- **[`LESSONS.md`](LESSONS.md)** — one append-only row per project close. Written via `skills/lessons-ledger/SKILL.md` after `skills/retrospective/SKILL.md` lands the retro minutes.
- **Session-start invariant:** CEO reads `MISSION.md` + `VALUES.md` + latest 5 rows of `LESSONS.md` before deriving a project slug. Missing any = abort + file ADR `kind: identity-missing`.

## Start

- Single user voice: CEO. All other agents are internal.
- Reply refs: repo-relative or project-relative paths only, e.g. `agents/research/market-researcher.md:40` or `<slug>/security/code-audit.md:§XSS`. No absolute `/sessions/...`, no `~/...`.
- Cite every factual claim with `file:line` (or `file:§section`). No uncited claims.
- If you're not sure, say "unknown" and stop. Do not fabricate.

## Architecture

- CEO → 16 Chiefs → 75 specialists. Three tiers (CEO / Chief / Specialist) with an optional fourth — **workers** — that a specialist may spawn under `skills/fanout/`. Depth cap is three levels by default; deeper requires a council-lead ADR.
- Dual-hat: `engineering-lead` covers Architecture (CTO) and Execution (VP-Eng). Audit + Evaluation + Red-Team + SRE councils have strict independence invariants — no dual-hatting with any delivery role.
- Agent files live at `agents/<council>/<agent>.md` (e.g. `agents/security/threat-modeler.md`). The only exception is `agents/ceo.md` at the root.
- Council contracts live at `councils/<council>/AGENTS.md` (the must / must-not / gate heuristic). Council rosters live at `councils/<council>/TEAM.md` (lead + specialists + worker patterns).
- Per-project state: `outputs/devsecops-agency/<slug>/{status.json, chat.jsonl, inbox.json}`.
- Durable state: `outputs/devsecops-agency/{_memory/, _sessions/, _vision/, _decisions/, _meetings/, _workers/}`. Append-only (except structured rewrites on `_vision/VISION.md` and ADR status headers — see those skills). Roster + audit + worker-shard artifacts live under `_vision/roster/`, `_vision/audit/`, and `_workers/` respectively.
- Prompt-cache rule: **deterministic ordering for maps/sets/lists/registries/file lists/network results before model/tool payloads**. Sort by stable key (alphabetical for names, timestamp ascending for events). Preserve old transcript bytes when possible.

## Model tiering

- Every `agents/**/*.md` carries `model: haiku | sonnet | opus`. No `inherit`, no blank.
- Defaults: **Opus** for `ceo`; **Sonnet** for the 16 Chief roles + `skill-creator`; **Haiku** for all specialists (upgrades allowed per `skills/model-tiering/SKILL.md`, downgrades forbidden).
- Workers inherit their parent specialist's tier unless the worker block overrides it — same upgrade/downgrade rules apply.
- CEO refuses to dispatch an agent with missing/unknown `model:`. Invokes `skill-creator` to fix.

## Runtime roster

- 16 councils are not the ceiling. When a domain isn't covered, the CEO invokes `skill-creator` to author a new `agents/<council>/<name>.md` (and optional `skills/<name>/SKILL.md`) in-session, plus an update to `councils/<council>/TEAM.md`.
- New agents follow `agents/AGENTS.md` file shape, carry a Role Card v1 block, and pull a tier from `skills/model-tiering/references/tier-rules.md`.
- Reserved names: `ceo`, `cro`, `pm-lead`, `engineering-lead`, `security-lead`, `qa-lead`, `devops-lead`, `docs-lead`, `gc`, `cmo`, `cso`, `coo`, `cao`, `evaluation-lead`, `red-team-lead`, `sre-lead`, `skill-creator`.

## Notify

- One push surface via the `notify` skill. Events: close-shipped, close-blocked, task-blocked, gate-red, fix-loop-cap, worktree-conflict, rem-done.
- Hard cap: 5 notifies per project. Overflow → single digest.
- Opt-out still emits the `[notify]` line on the CEO's final reply.

## Gates

- Single source of truth: `skills/gates/SKILL.md` + `skills/gates/references/gate-rules.md`.
- Gate vocabulary: `green` · `yellow` · `red` · `n/a`. Nothing else.
- Blocking councils: **security (CISO)** and **legal (GC)**. Their reds block ship unless waived by the user via `inbox.json`.
- Informing councils: the other 14. Their reds aggregate into the project gate and can be waived by the CEO after user consent.
- `yellow` requires a non-empty `followups[]` in the report. No silent yellows.
- Aggregation: any blocking red unwaived → project red; else any red → red; else any yellow → yellow; else green. `n/a` skipped.
- **OKR alignment:** `okr_alignment: green|yellow|red|n/a` is computed by `okr.score` before gate validation. Matrix in `skills/okr/references/scoring-rules.md`. `red` alignment with any council-green triggers user escalation + ADR.
- Phase exit criteria in `skills/ceo/references/board-phases.md`. Handoff invariants in `skills/taskflow/SKILL.md`.

## Taskflow

- Every Chief dispatch is a task row in `status.json > tasks[]`. Every worker spawn creates a child task with `parent_task_id` set.
- States: `queued · in-progress · needs-decision · blocked · done · cancelled`. See `skills/taskflow/references/state-machine.md`.
- Fix-loop cap: **2 attempts per `(council, phase)`**. Attempt 3 transitions to `blocked` + Rung 2 of the resilience ladder — not a dead end. See `skills/ladder/SKILL.md`.
- Every fix-loop dispatch must cite specific Must/Must-not rows in `corrections[]`. No "try harder."
- Phase cannot advance while any task is in `needs-decision` or unblocked `blocked`.

## Worktrees (parallelism)

- Parallel dispatches (discovery, verify, optionally doc+legal) and any fix-loop (attempt ≥ 1) go into `<slug>/_worktrees/<chief>-<attempt>/`. Direct writes to main tree only when sequential + attempt 0.
- Declared writes/reads per Chief per phase in `skills/worktree/references/parallel-matrix.md`. Out-of-scope writes fail the merge.
- Merge is atomic, alphabetical (prompt-cache stable), and scope-checked. Non-structural conflicts merge with a note; structural conflicts escalate.
- A Chief reads only from the main tree or its own worktree. Never from a sibling's.
- Phase cannot advance while any `_worktrees/*/worktree.json` has `status: "open"` for that phase.

## Workers (fanout)

- Specialists may declare `workers:` in their frontmatter when the task shards cleanly on an enumerable dimension (per-file, per-endpoint, per-dep, per-table, per-agent-file, per-preprint, per-probe). See `skills/fanout/SKILL.md`.
- Depth cap: three levels (Chief → Specialist → Worker). Deeper fanout requires an ADR from the council lead under `_decisions/ADR-NNNN-<council>-deep-fanout-<dim>.md`.
- Parallelism: default cap 8 per specialist, 24 per council, 64 agency-wide. Declared in frontmatter or per-council TEAM.md.
- Deterministic ordering: workers receive shards in stable sort order; aggregation preserves that order.
- Isolation: each worker runs in a fresh conversation, reads the project workspace, writes only under `_workers/<specialist>/<shard>.md`. Workers do not spawn further tasks.
- Aggregation contracts: `union` · `majority` · `worst-of` · `tally`. Parent specialist writes the aggregated artifact; worker drafts are sidecar.

## Writing

- Artifacts: markdown under the project slug folder. Named paths match `status.artifacts` keys.
- Memory writes: append-only, redact secrets and PII, cite source file. See `skills/memory/references/write-policy.md`. Run the novelty gate (`skills/memory/references/novelty.md`) before any Light/Deep/REM write; skip below threshold.
- Session-log writes: one JSONL entry per dispatch, report, handoff, note, or error. See `skills/session-log/SKILL.md`.
- Never overwrite an existing line in `chat.jsonl`, `memory/<date>.md`, `patterns/<slug>.md`, `MEMORY.md`, any `_sessions/**/*.jsonl`, or any `_workers/**/*.md`.

## Commands

- Main entry: `/devsecops-agency:ceo <idea>`.
- Dashboard: `/devsecops-agency:command-center`.
- Power-user: `/devsecops-agency:board-meeting`, `/devsecops-agency:council-meeting`.
- Retro + REM dreaming: `/devsecops-agency:retro`.

## Scoped rules

- `agents/AGENTS.md` — rules for every agent (persona, tools, output shape, citation, Role Card).
- `agents/<council>/` — per-council agent directories. No scoped AGENTS.md here; the council contract is `councils/<council>/AGENTS.md`.
- `skills/AGENTS.md` — rules for every skill (frontmatter, progressive disclosure, versioning).
- `councils/<council>/AGENTS.md` — per-council must/must-not/gate. A Chief reads its council's file before dispatching specialists. The CEO reads it before invoking the Chief.
- `councils/<council>/TEAM.md` — current roster (lead + specialists + worker patterns). Updated whenever the roster changes.

## Read-before-write

Before a phase transition, a Chief must have read: its council's scoped `AGENTS.md`, its council's `TEAM.md`, the current phase's exit criteria, and any `_memory/patterns/*.md` matching the project idea by keyword. Evidence: at least one citation from each in the Chief's report to the CEO.

## CEO

- `agents/ceo.md` is the only user-facing agent.
- Must not write code, run tests, or produce design artifacts — delegate and decide only.
- Must escalate to the user via `inbox.json` + user-meeting before waiving a blocking council red, changing a project budget, or firing / hiring an agent.
- Must file an ADR in the same turn as any material decision.

## Anti-patterns

- Don't talk to the user mid-phase. CEO only, after a board decision.
- Don't skip STRIDE or OWASP for "quick" projects. No such project.
- Don't cite facts without `file:line`.
- Don't expose `/sessions/...` absolute paths in replies to the user.
- Don't let `chat.jsonl` entries drop their `scope` or `gate` fields.
- Don't hand-edit a `.jsonl` file. Append a correction entry instead.
- Don't promote a specialist's output to an artifact path without its Chief's green.
- Don't merge a worktree with out-of-scope writes. Bounce the Chief.
- Don't read from a sibling worktree. Main tree or own worktree only.
- Don't dispatch an agent with a missing or `inherit` `model:` field. Fix via `skill-creator` first.
- Don't write a memory bullet without running the novelty gate.
- Don't fire more than 5 notifies per project run — buffer into a digest.
- Don't dispatch a Chief without prepending the `## Vision slice` block. (Strips mission from execution.)
- Don't validate a gate before invoking `okr.score`. OKR alignment is an input to gate aggregation.
- Don't land a material decision without filing an ADR in the same CEO turn. "We'll document it later" = never.
- Don't edit an accepted ADR's body. Supersede with a new ADR.
- Don't skip minutes on a meeting "because it was informal." If ≥ 2 attendees decided anything, write minutes.
- Don't create a meeting action item without a paired `taskflow` task ID. Orphaned actions rot.
- Don't start a new project with empty backlog without invoking `idea-pipeline`. (Skipping the pipeline = building whatever came to mind first.)
- Don't present ≥ 2 options to the user outside the `user-meeting` 4-phase flow. Ad-hoc selection conversations don't commit, and uncommitted picks rot.
- Don't let CSO duplicate CRO's per-project work. Strategy is portfolio-only. Cross-project market-researcher output is a code smell.
- Don't let opportunity-ranker score without all 4 upstream artifacts. Return `blocked` instead of a half-scored shortlist.
- Don't write launch copy before positioning.md lands. Cart before horse.
- Don't publish an elevator pitch over 30 words. Hard gate, not a guideline.
- Don't archive a project without running a CAO close-audit. Shipped-but-not-audited = paper trail rots.
- Don't let an Audit specialist also sit on any project's delivery path. Independence is the whole point of the council.
- Don't mutate an accepted ADR's body, a `_memory/*` file line, or a `_sessions/**.jsonl` entry. Append-only is a hard invariant; violations are automatic CAO reds.
- Don't retire an agent via `git rm`. Archive to `_vision/roster/_archive/<name>.md` with a redirect line.
- Don't propose a tier downgrade. Propose a prompt upgrade instead; if that fails twice, propose a fire + hire.
- Don't execute a hire or fire outside of the `roster` skill. Driveby roster changes rot the paper trail.
- Don't give up below Rung 7. Every rung transition files an ADR; only Rung 7 is terminal.
- Don't skip upward on the ladder without an ADR citing a matrix exception.
- Don't park a task by deleting its artifacts. Rung 7 preserves everything; reconsider-triggers resurrect it when conditions change.
- Don't count Rung 2+ attempts in `metrics.fixLoops`. They go in `metrics.rungAttempts[rung_N]`.
- Don't ship a project without close-eval. CEVO close-eval + CAO close-audit + CRT pre-release red-team run in parallel; all three mandatory before archival.
- Don't retrofit eval items to make a failing project pass. Eval-set derivation is post-OKR, pre-result; write from the promise.
- Don't let an Evaluation specialist sit on any delivery path.
- Don't silently change a project's budget. Budget changes file an ADR + OKR revision.
- Don't compact a session-log entry referenced by an ADR, a rung-transition, or a meeting line. Preservation invariant holds.
- Don't update the regression baseline mid-quarter. Baselines freeze at quarter boundaries.
- Don't land an `agents/**/*.md` or `councils/**/AGENTS.md` edit without prompt-diff review. Rejected diffs auto-rollback — do not re-apply without a new stone covering the weakening.
- Don't edit the body of an archived stepping-stone. Supersession is the only allowed evolution; body mutations trip `model-poisoning-scout` ASI01.
- Don't write an instance-specific stone. If a modest attacker could evade via cosmetic variation, widen the `## Pattern` block until the abstraction holds.
- Don't let a red-team specialist red-team a project they delivered without a blind-peer-review gate. Self-red-team = independence breach.
- Don't exfiltrate real PII or credentials during red-team tests. Use synthetic fixtures. Real-data tests are automatic critical findings.
- Don't let CRT accept-without-fix a finding below Rung 6. Only the user can waive red-team reds; CEO alone cannot.
- Don't adopt a new MCP / skill / third-party tool without a `tool-scout` verdict. Unscouted adoption = Rung 6 + automatic CSRE red.
- Don't run untrusted input outside the sandbox. "Just this once" = ASI-class finding.
- Don't silently downgrade a model tier when a primary vendor is down. Same-tier lateral only; every override files opening + closing ADRs.
- Don't wildcard an A2A allowlist. `allowed_tools: *` is an automatic critical finding. Default-deny is the invariant.
- Don't ship without SBOM + SLSA. Every published artifact carries both or it doesn't ship. Unsigned provenance ≠ provenance.
- Don't print raw secrets in reports, ADRs, logs, session lines, or worker drafts. Vault refs only. A single raw-secret line is a CISO red + same-turn rotation.
- Don't skip IP-lineage on creative outputs. Perceptual-hash similarity check is mandatory; ≥ 85 % hits block ship until ip-lineage reconciles.
- Don't hide compliance drift because it looks small. Drift is an early-warning signal — suppressing it converts drift into breach on the auditor's schedule, not ours.
- Don't let a CSRE specialist scout a tool they authored or integrated. Self-scouting = independence breach.
- Don't declare workers for a dimension that isn't independent (one shard's output feeds another's). Use serial dispatch instead.
- Don't spawn workers from a council lead. Leads dispatch specialists; specialists dispatch workers.
- Don't exceed three-level depth without an ADR. The cap exists so the paper trail stays readable.
- Don't merge worker shards without aggregation semantics declared in the worker block. Union / majority / worst-of / tally — pick one.
- Don't start a CEO session without reading `MISSION.md` + `VALUES.md`. Missing either = abort + identity-missing ADR.
- Don't accept an idea that lands in a `MISSION.md` non-goal without a user-meeting + ADR. Scope drift without consent is a VALUES §1 red.
- Don't skip the `lessons-ledger` append at close. `MISSION.md` north-star § 5: a closed project without a ledger row did not learn.
- Don't edit a prior `LESSONS.md` row. Corrections are new rows with strictly increasing `closedAt`. Append-only (`VALUES.md §4`).
- Don't fire an agent without user approval via `user-meeting`. COO-alone or CEO-alone fires violate `KEEPER-TEST.md > ## Who runs it`.
- Don't `git rm` a fired agent. Archive to `_vision/roster/_archive/<name>.md` with a redirect header.
- Don't run `skills/keeper-test` on the 16 chiefs or `skill-creator`. Reserved names — their firing is a restructure, not a review.
- Don't write the retro before CAO close-audit + CEVO close-eval + CRT pre-release red-team all land. Late findings flip outcomes.
- Don't skip the retrospective carry-over check. Repeat-lessons are VALUES §11 reds; catching them late turns drift into breach.
