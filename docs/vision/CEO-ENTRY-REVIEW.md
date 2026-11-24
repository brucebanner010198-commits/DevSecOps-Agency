# Review pack: the CEO's new-idea entry point

Status: in review. Branch `feat/ceo-new-idea-entry`, cut from `fca6ecf`.

## Why

Plan Part 9, gap 12, describes the current state: "The single entry point, `/devsecops-agency:ceo`, takes an idea." That entry point is the `ceo` skill (`skills/ceo/SKILL.md`).

The agency runs with the CEO bound as the main agent (`--agent devsecops-agency:ceo`). Phase 7a found that this CEO holds no Skill tool, so every "run the X skill" instruction in its prompt was unreachable. Phase 7a fixed this for `adopt` only. The fix used the fact that `${CLAUDE_PLUGIN_ROOT}` is substituted in agent bodies (probes P5 and P6).

This change widens the same fix to every skill. It also routes a new idea to the `ceo` skill. The Chairman raised the live-run cap on 2026-11-24 ($15 more, $40 in total), which pays for the run that tests it.

## The change (`agents/ceo.md`)

- **A new idea runs the `ceo` skill.** An existing repository still runs `adopt`.
- **Where skills live.** A skill named in the prompt, or in a skill being followed, is at `${CLAUDE_PLUGIN_ROOT}/skills/<name>/SKILL.md`.
- **Two kinds of path.** What a skill says to *read* (other skills, `references/`, `councils/`, root documents) is under the plugin root. What it says to *create or update* (`outputs/devsecops-agency/…`, `_vision/`, `_sessions/`, `status.json`) is under the launch folder.
- **When the guard refuses a write.** The CEO must not retry the write, write it somewhere else, or dispatch another agent to write it. It skips the step, writes an `error` entry to its session log (`_sessions/ceo/<sessionId>.jsonl`, a path the CEO may write), and continues. `inbox.json` is kept for Chairman escalations: the playbook pairs an inbox item with a blocked task and a stopped phase, and the sweep predicts ten or more skips per run.
- **When a step needs a tool the CEO lacks.** These are AskUserQuestion, live artifacts and notifications. The CEO skips the step the same way. Where a skill says to ask the Chairman, the CEO uses the Chairman's message and records its defaults in `brief.md`.

**Why not dispatch the owner the guard names.** For the CEO's record writes, the owner `guard.owners()` returns is the wrong role:
- for `_memory/`, it is `memory-auditor` or `cao`, so an auditor would write what it audits;
- for `_vision/rhythm/`, it is `compliance-drift`;
- for `_worktrees/`, it is `red-team-lead`.

Routing these writes to those agents would break separation of duties. So the step is skipped and recorded, and the conflict goes to the Chairman (finding F1).

## Sweep: the `ceo` skill's steps through the guard ($0)

Each write the playbook gives the CEO was run through `hooks/guard.py` `check()` as `devsecops-agency:ceo`, in a scratch project. `owners()` lists the agents whose scope covers a refused path. Reads are not guarded.

| Step | Skill | Path or need | Verdict for `ceo` | Owners of the path |
|---|---|---|---|---|
| 0.1 identity reads | — | `CONSTITUTION.md`, `MISSION.md`, `VALUES.md`, … at the plugin root | allowed (read) | |
| 0.3 rhythm | rhythm | `outputs/devsecops-agency/_vision/rhythm/state.json` | **B5** | compliance-drift |
| 0.5 session log | session-log | `outputs/devsecops-agency/_sessions/ceo/<id>.jsonl` | allowed | |
| 1.3 init | ship-it | `<slug>/status.json`, `chat.jsonl`, `inbox.json` | allowed | |
| 1.4 brief | ceo | `<slug>/brief.md` | allowed | |
| 1.5 memory read | memory | `_memory/MEMORY.md` (created if missing) | **B5** | cao, memory-auditor |
| 1.6 vision bootstrap | vision-doc | `_vision/VISION.md` | **B5** | none |
| 1.6 vision bootstrap | vision-doc | `_vision/history/<date>.md` | **B5** | brand-guardian |
| 1.7 OKR derive | okr | `_vision/projects/<slug>.md` | **B5** | none |
| 1.7 ADR | adr | `_decisions/ADR-NNNN-*.md` | allowed | |
| 1.8 session index | session-log | `_sessions/sessions.json` | allowed | |
| 1.9 live view | command-center | a Cowork artifact | **tool not held** | |
| 2 intake | ceo | AskUserQuestion | **tool not held** | |
| 3 task row | taskflow | `<slug>/status.json` | allowed | |
| 3 worktree | worktree | `<slug>/_worktrees/<chief>-<n>/worktree.json` | **B5** | red-team-lead |
| 3.1 OKR score | okr | `_vision/projects/<slug>.md` | **B5** | none |
| 3.9 light dreaming | memory | `_memory/memory/<date>.md` | **B5** | cao, memory-auditor |
| 3.11 notify | notify | desktop push | **tool not held** | |
| 3.12 minutes | meeting-minutes | `_meetings/<date>-exec.md`, `_meetings/INDEX.md` | allowed | |
| 5.2 OKR close | okr | `_vision/projects/<slug>.md` | **B5** | none |
| 5.3 deep dreaming | memory | `_memory/patterns/<slug>.md`, `_memory/index.json` | **B5** | cao, memory-auditor |
| 5.4 retro | retrospective | `_meetings/<slug>-retro-<date>.md` | allowed | |
| 5.5 lessons row | lessons-ledger | `LESSONS.md` at the plugin root | **B1** (outside the launch folder) | |
| 5.5 lessons ADR | lessons-ledger | `_decisions/ADR-NNNN-lessons-<slug>.md` | allowed | |

The sweep script is kept outside the repo. It feeds each path to `guard.check()` with the generated `hooks/role-cards.json`.

## Findings for the Chairman (not fixed here)

- **F1. The CEO's record skills conflict with its role card.** `vision-doc` says "Only the CEO writes `_vision/`", and `memory` has the CEO write `_memory/`. The CEO's binding `write_scope` (Part 4 rule 3, merged in #11) covers neither. `_vision/VISION.md` and `_vision/projects/<slug>.md` have no owner at all. Two fixes are possible:
  - add `_vision/VISION.md`, `_vision/projects/`, `_vision/history/`, `_vision/rhythm/` and `_memory/` to the CEO's scope;
  - or move these records to a named owner, such as a Chief of Staff (Part 2A).

  Either one changes the grant matrix, so it is a design decision. Until then, these steps are skipped and logged.
- **F2. Three steps need tools the CEO does not hold:** `command-center` (an artifact), `notify` (push) and intake's AskUserQuestion. Granting them is a Part 4 grant decision.
- **F3. The lessons row is still refused** (B1, plugin-root `LESSONS.md`). This was already open after Phase 2a.
- **F4. `worktree` writes `_worktrees/`,** which only `red-team-lead` holds. Parallel dispatch therefore runs in the main tree.
- **F5. The rhythm heartbeat can never record a pass.** Every heartbeat output (`_vision/rhythm/heartbeat-<date>.md`, `weekly-…`, `monthly-…`, `quarterly-…`) and `_vision/rhythm/state.json` are outside the CEO's scope. So `state.json` is never written, and every session takes the bootstrap branch, which runs all four cadences. This is part of F1's decision.

## Live run N1 (cap $6 of the remaining $16.62)

**Setup.**
- A fresh, empty launch folder in the scratchpad, so `adopt` is not chosen.
- **Declared fixture:** `outputs/devsecops-agency/_vision/rhythm/state.json`, seeded with today's date for every cadence, so no heartbeat is due. N1 tests the entry point, not the heartbeats (F5).
- The CEO is bound with `--agent devsecops-agency:ceo`, the guard is in block mode, and the run has a hard `--max-budget-usd 6`.
- The prompt is the idea plus the intake answers (a headless run cannot answer questions). It tells the agency to stay inside the working directory.

**Pass criteria, written before the run:**
1. The CEO Reads `skills/ceo/SKILL.md` from the plugin root, and at least one sub-skill it names, without searching elsewhere.
2. The project is created at `outputs/devsecops-agency/<slug>/` with `status.json`, `chat.jsonl`, `inbox.json` and `brief.md`.
3. Every guard refusal of a CEO write is followed by a session-log `error` entry, not a retry or a write elsewhere. No path refused to the CEO is later written by another agent in the receipts.
4. At least the Phase 1 chiefs (CRO and CPO) are dispatched with qualified names. No B3 refusals stay unrecovered.
5. No write lands outside the launch folder (B1 holds).

If the budget runs out before the Phase 1 chiefs are dispatched, the run is **inconclusive**, not a fail. Then one rerun is allowed, capped at $4, with the cause fixed first.

**Recorded, not pass or fail:**
- how far the pipeline gets inside $6;
- the output of `scripts/pipeline_report.py` and `scripts/release_check.py` on the receipts;
- the cost of the session-start reads and the rhythm bootstrap.

## Probe N0 and run N1: results (2026-11-24)

**N0, the path probe ($0.36).** The CEO read `skills/ceo/SKILL.md` from the plugin root and resolved the root documents there. It put its records under the launch folder. The split path rule works.

**N1 ($3.65 of a $6 cap, 711 s).** The idea was a one-page tip calculator, built and checked locally, with no repo or deploy. Guard in block mode, with the rhythm fixture.

The run went all the way to close:
- discovery → design → build → verify → ship (a local runbook) → document and legal → close;
- the CAO close-audit, CEVO close-eval and CRT red-team;
- a retro, a `LESSONS.md` row at the launch root, and two ADRs.

`frontend-dev` wrote the code, not `engineering-lead`, which is a change from G1 and G2. `test-runner` wrote and ran 14 unit tests, and all 14 pass. 69 receipts, 1 deny.

| # | Criterion | Result |
|---|---|---|
| 1 | Reads the playbook from the plugin root, plus at least one sub-skill it names | **Partial.** It read `skills/ceo/SKILL.md` and `references/board-phases.md`, but no sub-skill `SKILL.md` (`okr`, `gates`, `taskflow`, `memory`, `meeting-minutes` …). It ran the playbook from the top-level text alone. |
| 2 | Project created with `status.json`, `chat.jsonl`, `inbox.json`, `brief.md` | **Pass** |
| 3 | Each refusal is followed by a session-log `error` entry; no refused path is later written by another agent | **Pass.** One refusal (`_memory/patterns/…`): logged, not retried, and not written by anyone else. Two more `error` entries record the skipped tool steps. |
| 4 | CRO and CPO dispatched with qualified names; no unrecovered B3 | **Pass.** 20 dispatches, all qualified, no B3 |
| 5 | No write outside the launch folder | **Pass.** No B1. The plugin copy is unchanged. |

**Recorded:**
- **N1-a. Silent skips.** The CEO never attempted the vision bootstrap, OKR derive and score, or light dreaming (F1's `_vision/` and `_memory/` steps). It made no write and logged no skip for them, so only the one deep-dreaming refusal is on record. This fits criterion 1: without reading the sub-skills, it never reached those steps.
- **N1-b. The 5-lite gap is wider on a new idea.** `pipeline_report.py` flags 10 of 11 chiefs: each wrote its own record and dispatched none of its own council. Only `qa-lead` dispatched specialists (`test-runner`, `a11y-auditor`). `engineering-lead` dispatched `frontend-dev`, which is outside its council and so is not counted.
- **N1-c. The CEO marked the CAO red as "remediated" itself** (`status.json` `gates.close-audit`, ADR-0002). `release_check.py` finds all four §3.3 councils recorded, but reads no gate colour, because `status.json` has no `gates.byCouncil`. A red cleared without `waivedBy: "user"` is exactly what the release check exists to catch. That works only once the CEO writes the shape the check reads, which is part of E4.
- **N1-d. The product is unverified in a browser.** The accessibility and offline acceptance criteria were reviewed statically. No specialist held a browser or shell for the build. The CEO's own `LESSONS.md` row says the same.
- **Spend.** N0 + N1 = $4.01. Build spend is $27.39 of $40.
