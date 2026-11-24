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
