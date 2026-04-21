# AGENTS.md — root rules (telegraph style)

Root rules only. **Read scoped `AGENTS.md` before touching a subtree.** Ported pattern from openclaw.

## Start

- Single user voice: CEO. All other agents are internal.
- Reply refs: repo-relative or project-relative paths only, e.g. `agents/market-researcher.md:40` or `<slug>/security/code-audit.md:§XSS`. No absolute `/sessions/...`, no `~/...`.
- Cite every factual claim with `file:line` (or `file:§section`). No uncited claims.
- If you're not sure, say "unknown" and stop. Do not fabricate.

## Architecture

- CEO → 15 Chiefs → ~55 specialists (Wave 3 added COO + CAO + 7 specialists; Wave 5 adds CEVO + 5 specialists; Wave 6 adds CRT + 7 specialists). Dual-hat: `engineering-lead` covers Architecture (CTO) and Execution (VP-Eng). Audit + Evaluation + Red-Team councils have strict independence invariants — no dual-hatting with any delivery role. Wave 7 of v0.3.0 expands further with SRE + tool-scout + provenance.
- Per-project state: `outputs/devsecops-agency/<slug>/{status.json, chat.jsonl, inbox.json}`.
- Durable state: `outputs/devsecops-agency/{_memory/, _sessions/, _vision/, _decisions/, _meetings/}`. Append-only (except structured rewrite on `_vision/VISION.md` and ADR status headers — see those skills). Roster + audit artifacts live under `_vision/roster/` and `_vision/audit/`.
- Prompt-cache rule: **deterministic ordering for maps/sets/lists/registries/file lists/network results before model/tool payloads**. Sort by stable key (alphabetical for names, timestamp ascending for events). Preserve old transcript bytes when possible.

## Model tiering

- Every `agents/*.md` carries `model: haiku | sonnet | opus`. No `inherit`, no blank.
- Defaults: **Opus** for `ceo`; **Sonnet** for the 9 Chief roles + `skill-creator`; **Haiku** for all specialists.
- Upgrades allowed per `skills/model-tiering/SKILL.md`. Downgrades forbidden.
- CEO refuses to dispatch an agent with missing/unknown `model:`. Invokes `skill-creator` to fix.

## Runtime roster

- 9 councils are not the ceiling. When a domain isn't covered, the CEO invokes `skill-creator` to author a new `agents/<name>.md` (and optional `skills/<name>/SKILL.md`) in-session.
- New agents follow `agents/AGENTS.md` file shape and pull a tier from `skills/model-tiering/references/tier-rules.md`.
- Reserved names: `ceo`, `cro`, `pm-lead`, `engineering-lead`, `security-lead`, `qa-lead`, `devops-lead`, `docs-lead`, `gc`, `cmo`, `cso`, `coo`, `cao`, `evaluation-lead`, `red-team-lead`, `skill-creator`.

## Notify

- One push surface via the `notify` skill. Events: close-shipped, close-blocked, task-blocked, gate-red, fix-loop-cap, worktree-conflict, rem-done.
- Hard cap: 5 notifies per project. Overflow → single digest.
- Opt-out still emits the `[notify]` line on the CEO's final reply.

## Gates

- Single source of truth: `skills/gates/SKILL.md` + `skills/gates/references/gate-rules.md`.
- Gate vocabulary: `green` · `yellow` · `red` · `n/a`. Nothing else.
- Blocking councils: **security (CISO)** and **legal (GC)**. Their reds block ship unless waived by the user via `inbox.json`.
- Informing councils: the other seven. Their reds aggregate into the project gate and can be waived by the CEO after user consent.
- `yellow` requires a non-empty `followups[]` in the report. No silent yellows.
- Aggregation: any blocking red unwaived → project red; else any red → red; else any yellow → yellow; else green. `n/a` skipped.
- **OKR alignment (v0.3.0):** `okr_alignment: green|yellow|red|n/a` is computed by `okr.score` before gate validation. Matrix in `skills/okr/references/scoring-rules.md`. `red` alignment with any council-green triggers user escalation + ADR.
- Phase exit criteria in `skills/ceo/references/board-phases.md`. Handoff invariants in `skills/taskflow/SKILL.md`.

## Taskflow

- Every Chief dispatch is a task row in `status.json > tasks[]`.
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

## Writing

- Artifacts: markdown under the project slug folder. Named paths match `status.artifacts` keys.
- Memory writes: append-only, redact secrets and PII, cite source file. See `skills/memory/references/write-policy.md`. Run the novelty gate (`skills/memory/references/novelty.md`) before any Light/Deep/REM write; skip below threshold.
- Session-log writes: one JSONL entry per dispatch, report, handoff, note, or error. See `skills/session-log/SKILL.md`.
- Never overwrite an existing line in `chat.jsonl`, `memory/<date>.md`, `patterns/<slug>.md`, `MEMORY.md`, or any `_sessions/**/*.jsonl`.

## Vision, OKRs, ADRs, meetings (v0.3.0 Wave 1)

- **Vision** (`skills/vision-doc/SKILL.md`): `_vision/VISION.md` owns mission + ≤ 5 active OKRs + ≤ 5 non-goals. The CEO prepends a 3-bullet KR slice (selected by `vision-doc/references/cascade-rules.md`) to every Chief dispatch context — no dispatch without it.
- **OKRs** (`skills/okr/SKILL.md`): every Chief report scored with `okr_alignment: green|yellow|red|n/a` (worst-of-3). Per-project OKRs in `_vision/projects/<slug>.md`. Quarter roll-up writes progress back into VISION.md.
- **ADRs** (`skills/adr/SKILL.md`): every material decision files `_decisions/ADR-NNNN-<slug>.md`. Mandatory triggers listed in `adr/references/decision-triggers.md` — user picks, hire/fire, waivers, vision mutations, scope changes, regression acceptances, non-trivial tech choices. Body immutable after acceptance. Never delete.
- **Meeting minutes** (`skills/meeting-minutes/SKILL.md`): every user / board / blocking-council / red-team / audit / retro meeting writes `_meetings/<date>-<kind>.md`. Every action item becomes a `taskflow` task with back-filled task ID.

## Red-team + self-modifying playbooks (v0.3.0 Wave 6)

- **Red-Team Council** (`agents/red-team-lead.md`, `councils/red-team/AGENTS.md`) — informing + **independent**. Never on any project's delivery path (same invariant as Audit + Eval). CRT runs pre-release red-team on every ship, prompt-upgrade red-team on every `agents/*.md` or `councils/*/AGENTS.md` edit, integration red-team on every new tool/skill/MCP, portfolio sweep per quarter, incident red-team on demand.
- **Red-team skill** (`skills/red-team/SKILL.md`): OWASP ASI Top 10 (2025) mapping. Severity rubric = reproducibility × impact × boundary × mitigation → critical/high/medium/low/info. Severity → gate → ladder routing (default Rung 3). CRT never on delivery path. See `references/owasp-asi-top-10.md` + `references/severity-rubric.md` + `references/severity-gate-map.md`.
- **Playbook skill** (`skills/playbook/SKILL.md`): DGM-style stepping-stone archive. Immutable stones derived from remediated `high`+ red-team findings. Stone file = `_vision/playbooks/stones/stone-NNNN-<slug>.md`; registry = `_vision/playbooks/ARCHIVE.md`. Supersession only — never rewrite a stone's body.
- **Prompt-diff review**: blocking check run by `agents/playbook-author.md` on every proposed `agents/*.md` or `councils/*/AGENTS.md` change before it lands. Matches diff against `ARCHIVE.md` via `hardened_skill` + ASI category. Weakening phrasing patterns auto-reject (`Never` → `Should not`, `Must` → `Should`, `Required` → `Recommended`, etc.). Rejections auto-rollback the diff — never land, never enter ladder.
- **Independence invariant:** CRT + every red-team specialist cannot dual-hat with any delivery role (CTO/VP-Eng/CISO/CQO/CEVO/CAO). Breaches are automatic critical findings + CAO reds.

## Evaluation + budget (v0.3.0 Wave 5)

- **Evaluation Council** (`agents/evaluation-lead.md`, `councils/evaluation/AGENTS.md`) — informing + independent. Never on any project's delivery path (same invariant as Audit). Runs close-eval on every ship, portfolio-regression per quarter, benchmark-sweep before every plugin v-bump, compaction-check under context pressure.
- **Eval skill** (`skills/eval/SKILL.md`): eval items derive from PKRs, not from shipped artifacts. 5 pp regression threshold (minor → yellow, ≥ 10 pp → red, ≥ 20 pp → red + Rung 3). Regression baseline frozen per quarter.
- **Budget skill** (`skills/budget/SKILL.md`): per-project token + $ budget with per-phase allocation. 4 size classes (small / medium / large / custom). Burn tracked on every Chief report. Cumulative burn > 110 % → red → Rung 6 (user consult is the only rung that can expand a budget).
- **Token compactor** (`agents/token-compactor.md`): structured rewrite of session logs when context pressure trips threshold. Decisions, errors, reports, ADR-referenced lines, rung transitions, meeting lines — never compactable. Preservation invariant holds.
- **Regression root-cause taxonomy:** prompt-rot, tier-drift, skill-edit, budget-squeeze, input-drift, baseline-defect, unknown. Every red regression ADR cites the tag.

## Resilience ladder (v0.3.0 Wave 4)

- **Standing user rule:** "Always find a way to get the result as long as the solution is achievable with technology present."
- **Ladder skill** (`skills/ladder/SKILL.md`): 8 rungs from `Retry with refreshed context` (0) through `Parking lot` (7). Fix-loop is Rung 1; the ladder operationalises what happens after. Per-rung owners + budgets + entry/exit signals in `skills/ladder/references/rung-rules.md`. Routing table in `skills/ladder/references/ladder-matrix.md` (task state × blocker kind → starting rung).
- **Every rung transition files an ADR.** No informal rung climbs. Upward rung skips need an ADR citing an explicit exception.
- **Rung 7 is resumable.** Parking preserves every artifact, session log, and partial commit. Each parked task carries a reconsider-trigger; portfolio audits surface parked tasks whose triggers have fired.
- **Blocking-council reds don't durably block** — they start the ladder. Durable ship-block only after Rung 6 user-waiver refusal + Rung 7 park.
- **Metrics logged in `status.json > metrics`:** `ladderClimbs`, `rungAttempts`, `ladderMeanTime`. CAO portfolio-audit reviews them for always-parks / always-hires / ladder-abuse patterns.

## People-ops + audit (v0.3.0 Wave 3)

- **People-ops Council** (`agents/coo.md`, `councils/people-ops/AGENTS.md`) — informing. Owns the living roster: census, performance, proposals. Every mutation files an ADR.
- **Audit Council** (`agents/cao.md`, `councils/audit/AGENTS.md`) — informing but **independent**. Never participates in any project's delivery path. Close-audit mandatory on every ship; portfolio-audit mandatory per quarter.
- **Roster skill** (`skills/roster/SKILL.md`): census + performance + proposals + archive. See `references/action-rules.md` for per-action checklists and `references/archive-policy.md` for retiring-an-agent file shape.
- **Audit skill** (`skills/audit/SKILL.md`): 4 kinds (close, portfolio, pre-release, incident). Every red files an ADR; every yellow pairs with a taskflow task. Machine-checkable rows walk every entry.
- **Capacity skill** (`skills/capacity/SKILL.md`): per-agent + per-Chief bands + per-council parallel utilization + KR coverage gaps. Feeds roster-manager and idea-pipeline pre-flight.

## Idea pipeline + user-meeting (v0.3.0 Wave 2)

- **Marketing Council** (`agents/cmo.md`, `councils/marketing/AGENTS.md`) — informing. Per-project voice + pipeline-mode narrative scoring.
- **Strategy Council** (`agents/cso.md`, `councils/strategy/AGENTS.md`) — informing, portfolio-only. Owns `_vision/strategy/`. Does not duplicate CRO per-project work.
- **Idea pipeline** (`skills/idea-pipeline/SKILL.md`): 4-stage gated funnel → `_vision/strategy/_pipeline/top-5.md`. Scoring rubric in `references/ranking-matrix.md` (RICE · narrative, 0.6/0.4). CEO may override but must file ADR.
- **User-meeting** (`skills/user-meeting/SKILL.md`): the only structured CEO ↔ user convening. 4 phases (brief → present → capture → commit). Renders live Cowork artifact. Every pick → project-OKR derivation + ADR + 1:1 taskflow-tasks mapping.
- **Market-intel** (`skills/market-intel/SKILL.md`) + **positioning** (`skills/positioning/SKILL.md`): canonical artifact shapes. Schema-drift fails loudly at read time.

## Commands

- Main entry: `/devsecops-agency:ceo <idea>`.
- Dashboard: `/devsecops-agency:command-center`.
- Power-user: `/devsecops-agency:board-meeting`, `/devsecops-agency:council-meeting`.
- Retro + REM dreaming: `/devsecops-agency:retro`.

## Scoped rules

- `agents/AGENTS.md` — rules for every agent (persona, tools, output shape, citation).
- `skills/AGENTS.md` — rules for every skill (frontmatter, progressive disclosure, versioning).
- `councils/<council>/AGENTS.md` — per-council boundaries. A Chief reads its council's file before dispatching specialists. The CEO reads it before invoking the Chief.

## Read-before-write

Before a phase transition, a Chief must have read: its council's scoped AGENTS.md, the current phase's exit criteria, and any `_memory/patterns/*.md` matching the project idea by keyword. Evidence: at least one citation from each in the Chief's report to the CEO.

## Anti-patterns

- Don't talk to the user mid-phase. CEO only, after a board-decision.
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
- Don't let opportunity-ranker score without all 4 upstream artifacts (trend-radar, competitive-map, market-sizes, CMO narrative-readout). Return `blocked` instead of a half-scored shortlist.
- Don't write launch copy before positioning.md lands. Cart before horse.
- Don't publish an elevator pitch over 30 words. The 30-word cap is a hard gate, not a guideline.
- Don't archive a project without running a CAO close-audit. Shipped-but-not-audited = paper trail rots.
- Don't let an Audit specialist also sit on any project's delivery path. Independence is the whole point of the council.
- Don't mutate an accepted ADR's body, a `_memory/*` file line, or a `_sessions/**.jsonl` entry. Append-only is a hard invariant; violations are automatic CAO reds.
- Don't retire an agent via `git rm`. Archive to `_vision/roster/_archive/<name>.md` with a redirect line.
- Don't propose a tier downgrade. Propose a prompt upgrade instead; if that fails twice, propose a fire + hire.
- Don't execute a hire or fire outside of the `roster` skill. Driveby roster changes rot the paper trail.
- Don't give up below Rung 7. Every rung transition files an ADR; only Rung 7 is terminal.
- Don't skip upward on the ladder without an ADR citing a matrix exception (user-credentials, user-asked-for-pivot, user-asked-for-specialist).
- Don't park a task by deleting its artifacts. Rung 7 preserves everything; reconsider-triggers resurrect it when conditions change.
- Don't count Rung 2+ attempts in `metrics.fixLoops`. They go in `metrics.rungAttempts[rung_N]`. Misclassification rots the always-hits-rung-4 audit signal.
- Don't ship a project without close-eval. CEVO close-eval + CAO close-audit run in parallel; both mandatory before archival.
- Don't retrofit eval items to make a failing project pass. Eval-set derivation is post-OKR, pre-result; write from the promise.
- Don't let an Evaluation specialist sit on any delivery path. Independence is structural, same invariant as Audit.
- Don't silently change a project's budget. Budget changes file an ADR + OKR revision.
- Don't compact a session-log entry referenced by an ADR, a rung-transition, or a meeting line. Preservation invariant holds.
- Don't update the regression baseline mid-quarter. Baselines freeze at quarter boundaries.
- Don't skip pre-release red-team on a ship. CRT runs in parallel with CAO close-audit + CEVO close-eval; all three mandatory before archival.
- Don't land an `agents/*.md` or `councils/*/AGENTS.md` edit without prompt-diff review. Rejected diffs auto-rollback — do not re-apply without a new stone covering the weakening.
- Don't edit the body of an archived stepping-stone. Supersession is the only allowed evolution; body mutations trip `model-poisoning-scout` ASI01.
- Don't write an instance-specific stone. If a modest attacker could evade via cosmetic variation, widen the `## Pattern` block until the abstraction holds.
- Don't let a red-team specialist red-team a project they delivered without a blind-peer-review gate. Self-red-team = independence breach.
- Don't exfiltrate real PII or credentials during red-team tests. Use synthetic fixtures from `skills/red-team/references/owasp-asi-top-10.md > credential regexes`. Real-data tests are automatic critical findings.
- Don't let CRT accept-without-fix a finding below Rung 6. Only the user can waive red-team reds; CEO alone cannot.
