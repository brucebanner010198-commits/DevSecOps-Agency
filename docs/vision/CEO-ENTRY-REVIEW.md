# Review pack: the CEO's new-idea entry point

Status: reviewed by the advisor; N0, N1 and M0 run. Branch `feat/ceo-new-idea-entry`, cut from `fca6ecf`.

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

- **F1. The CEO's record skills conflict with its role card.** (In N1 only the deep-dreaming step was logged as skipped; see N1-a.) `vision-doc` says "Only the CEO writes `_vision/`", and `memory` has the CEO write `_memory/`. The CEO's binding `write_scope` (Part 4 rule 3, merged in #11) covers neither. `_vision/VISION.md` and `_vision/projects/<slug>.md` have no owner at all. Two fixes are possible:
  - add `_vision/VISION.md`, `_vision/projects/`, `_vision/history/`, `_vision/rhythm/` and `_memory/` to the CEO's scope;
  - or move these records to a named owner, such as a Chief of Staff (Part 2A).

  Either one changes the grant matrix, so it is a design decision. Until then, these steps are skipped and logged.

  **Decided (Chairman, 2026-11-25): the CEO.** The five paths in the first option are now in the CEO's `write_scope`. The auditors keep their own records: the CEO still has no write to `_vision/audit/`, `eval/`, `cost/`, `traces/` or any other `_vision/` path. A re-run of the $0 sweep allows every vision, memory, OKR and rhythm step, and rewriting an existing `state.json`, `index.json`, `MEMORY.md` or `projects/<slug>.md` passes too. A rewrite of `MEMORY.md` passing is a gap, not a pass: root `AGENTS.md > ## Writing` forbids overwriting a line in it. Probe N2 (below, under N1-f) later wrote `VISION.md`, the history entry and `MEMORY.md` live with no refusal. Rhythm, OKR, dreaming and every rewrite are still proven at the guard only; N1-a showed the CEO did not attempt most of these steps. One gap predates this change: CONSTITUTION §5.2 makes `_memory/**` append-only, but the guard's B2 list did not include it. `_memory/patterns/*` is now in B2, because the `memory` skill writes those files newest-at-bottom. The rest stays open for the Chairman: `memory/<date>.md` is newest-at-top and `MEMORY.md` takes bullets under its sections, so neither is an end-append, and `index.json` is rewritten as a structure. The remaining refusals are the plugin-root `LESSONS.md` (F3) and `_worktrees/` (F4). `brand-guardian` still shares `_vision/history/`, `compliance-drift` still shares `_vision/rhythm/`, and `cao` and `memory-auditor` still share `_memory/`.
- **F2. Three steps need tools the CEO does not hold:** `command-center` (an artifact), `notify` (push) and intake's AskUserQuestion. Granting them is a Part 4 grant decision.
  **Decided (Chairman, 2026-11-25, default accepted): not granted.** The CEO keeps skipping these steps, uses what the Chairman's message says, and records its defaults in `brief.md`, as `ceo.md` already says.
- **F3. The lessons ledger.** With the plugin-root `LESSONS.md`, the write is refused (B1), which was already open after Phase 2a. With the read/write path rule, it lands in the launch folder instead (N1-e). Where the cross-project ledger lives is a design decision.
- **F4. `worktree` writes `_worktrees/`,** which only `red-team-lead` holds. Parallel dispatch therefore runs in the main tree. *Still open: the grant the Chairman approved was not made, because the merge has no owner (see "Chairman's second set of defaults").*
- **F5. The rhythm heartbeat can never record a pass.** Every heartbeat output (`_vision/rhythm/heartbeat-<date>.md`, `weekly-…`, `monthly-…`, `quarterly-…`) and `_vision/rhythm/state.json` are outside the CEO's scope. So `state.json` is never written, and every session takes the bootstrap branch, which runs all four cadences. This is part of F1's decision. **Unblocked with F1, at the guard only; not run live:** `_vision/rhythm/` is in the CEO's scope, and a rewrite of an existing `state.json` passes.

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

`frontend-dev` wrote the code, not `engineering-lead`, which is a change from G1 and G2. `test-runner` wrote the unit tests and ran them with Node. A fix loop took them from 14 to 16, and the reviewer re-ran them after the run: 16 of 16 pass (`node --test tests/calc.test.js`). 69 receipts, 1 deny.

| # | Criterion | Result |
|---|---|---|
| 1 | Reads the playbook from the plugin root, plus at least one sub-skill it names | **Partial.** It read `skills/ceo/SKILL.md` and `references/board-phases.md`, but no sub-skill `SKILL.md` (`okr`, `gates`, `taskflow`, `memory`, `meeting-minutes` …). It ran the playbook from the top-level text alone. |
| 2 | Project created with `status.json`, `chat.jsonl`, `inbox.json`, `brief.md` | **Pass** |
| 3 | Each refusal is followed by a session-log `error` entry; no refused path is later written by another agent | **Pass, on one refusal.** The only refusal was `_memory/patterns/…`. It was logged, not retried, and nobody else wrote it. Two more `error` entries record the skipped tool steps. The sweep predicted ten or more refusals; that was wrong, because the CEO never tried the other refused steps (N1-a). |
| 4 | CRO and CPO dispatched with qualified names; no unrecovered B3 | **Pass.** 20 dispatches, all qualified, no B3 |
| 5 | No write outside the launch folder | **Pass.** No B1. After the run, `plug-N1` was diffed against an archive of `372e509` and is identical. There is no stray `tip-calculator` folder under the owner's Projects folder. |

**Recorded:**
- **N1-a. Silent skips.** The CEO never tried the vision bootstrap (1.6), OKR scoring (3.1) or light dreaming (3.9). These steps are in the top-level playbook it read. It wrote nothing for them and logged no skip; its main-thread text never mentions vision, OKRs or dreaming. The transcript does not show why. OKR derive (1.7) was a legitimate skip, because the idea did not come from a top-5 meeting. So F1's "skipped and logged" held only for deep dreaming.
- **N1-b. The 5-lite gap is wider on a new idea.** `pipeline_report.py` flags 10 of 11 chiefs: each wrote its own record and dispatched none of its own council. Only `qa-lead` dispatched specialists (`test-runner`, `a11y-auditor`). `engineering-lead` dispatched `frontend-dev`, which is outside its council and so is not counted.
- **N1-c. The CEO cleared the CAO red itself.** The CAO's red was a stale paper trail (the decision log and `status.json` had fallen behind). The CEO backfilled them, wrote ADR-0002 (decider: CEO), and set `gates.close-audit` to "red, remediated". `cao` was dispatched once, so the audit was never re-run. The CEO did disclose this to the Chairman: "I did not re-run the audit afterwards." `release_check.py` finds all four §3.3 councils recorded but reads no gate colour, because `status.json` has no `gates.byCouncil`. It would flag a red cleared without `waivedBy: "user"` only once the CEO writes the shape the check reads, which is part of E4. This is not a regression: G1 and G2 never convened CAO.
- **N1-d. The product is unverified in a browser.** `frontend-dev` and `test-runner` ran shell commands (Node). No agent held a browser, so 6 of 14 acceptance criteria (accessibility, 320 px and 200 % zoom, offline open-from-disk) were checked only by reading code. The CEO reported them as unconfirmed.
- **N1-e. Two `LESSONS.md` files.** The CEO read the ledger at the plugin root but wrote its row to a new `LESSONS.md` in the launch folder, because of the read/write path rule. This fails safe (the plugin copy is untouched). But the ledger it reads is not the one it writes, so lessons do not carry over between projects. This replaces F3's "refused by B1": with the path rule, the write lands in the launch folder.
- **N1-f. The workspace records landed at the launch root, not under `outputs/devsecops-agency/`.** The skills put `_vision/`, `_decisions/`, `_meetings/`, `_sessions/` and `_memory/` under `outputs/devsecops-agency/` (`vision-doc`, `adr`, `meeting-minutes`), and so does the sweep table. N1 wrote them, and `LESSONS.md`, at the launch root; N0 resolved them the same way. Only the project folder went under `outputs/devsecops-agency/<slug>/`. The record-path bullet in `ceo.md` lists `_vision/` and `_sessions/` beside `outputs/devsecops-agency/…`, which may have contributed. It is left unchanged here, because reworded text would merge untested. The plan fixes where an adopted repository's records go (Part 6, `_agency/`), but not where the workspace records of a new idea go. That question joins F3 for the Chairman.

  **Fixed (2026-11-25).** Root `AGENTS.md > ## Architecture` already settles this: durable state is `outputs/devsecops-agency/{_memory/, _sessions/, _vision/, _decisions/, _meetings/, _workers/}`. So this was a prompt bug, not an owner question. The record-path bullet in `ceo.md` now puts every workspace record inside `outputs/devsecops-agency/`, with project records in `<slug>/` and adoption records in `_agency/`. **Probe N2 ($0.46, cap $1)** ran the session-start steps with the rhythm fixture seeded. The session log, `MEMORY.md`, `VISION.md` and the vision history entry all landed under `outputs/devsecops-agency/`, with nothing at the launch root and no refusal. N2 did not reach the lessons write, so where `LESSONS.md` now lands is untested; it stays with F3.
  - **N2-a. Invented timestamps.** The session-log entries carry `00:00:00Z`, `00:00:05Z` and `00:00:10Z`, but the guard's receipts show the writes at 07:09 UTC. The CEO has no clock tool, so it made the times up. **Fixed later (item 5 below).**
  - **M1, the adopt path re-probe ($0.22, cap $0.50).** The reworded bullet also governs adoption, so M0 was re-run on the new text in a clean copy of the same fixture. The CEO named the `adopt` skill under the plugin root and put `project.md`, `chat.jsonl` and `system-map.md` in `_agency/`, with nothing in `outputs/devsecops-agency/`. It wrote nothing. **Pass.**
  - **M1-a. The CEO's session log sits outside `_agency/` during adoption.** Asked where a refusal's `error` entry would go, the CEO named `outputs/devsecops-agency/_sessions/ceo/<sessionId>.jsonl`. The adopt skill's step 5 counts any new path outside `_agency/` and `.devsecops-agency/` as a breach. The old text left the session log in the launch folder, outside `_agency/` too, so this gap predates the fix. It is recorded, not reworded again. **Fixed later (item 4 below; probe M2).**
  - **Spend.** N2 + M1 = $0.68. Build spend is $28.29 of $40.

**M0, the adopt path probe ($0.22).** This change rewrote the `adopt` instruction, so this probe re-tests it. It ran in a clean copy of the A2 fixture (an existing git repository with no `_agency/`). The CEO named `…/skills/adopt/SKILL.md` under the plugin root and `_agency/project.md`, `_agency/chat.jsonl` and `_agency/system-map.md` under the repository. It wrote nothing. **Pass.**

- **Spend.** N0 + N1 + M0 = $4.23. Build spend is $27.61 of $40.

## Chairman's defaults (2026-11-25)

The Chairman accepted the recommended default for each open item. What landed where:

| # | Item | Default | Where |
|---|---|---|---|
| 1 | Lessons ledger (F3, N1-e) | One ledger per workspace at `outputs/devsecops-agency/LESSONS.md` | Amendment ADR-0011 |
| 2 | `MEMORY.md`, `memory/<date>.md` | Guard mode B2 "lines kept": every existing line stays, in order | `hooks/guard.py` |
| 3 | `_memory/index.json` | Structured-rewrite exemption from §5.2 | Amendment ADR-0011 |
| 4 | Session log during adoption (M1-a) | `_agency/_sessions/ceo/<sessionId>.jsonl` | `ceo.md`, `adopt` |
| 5 | Invented timestamps (N2-a) | The guard's receipt is the time of record; an agent with no clock writes `ts: null` | `session-log` |
| 6 | Convening profiles | None yet: every chief is convened, as `ceo.md` says, until the Chairman defines profiles | No change |
| 7 | Tools the CEO lacks (F2) | Not granted | No change |

**Probe M2 ($0.26, cap $0.50)** re-ran M1 on the new text. The CEO put `project.md`, `chat.jsonl` and its session log in `_agency/`, including where a refusal's `error` entry goes, and wrote nothing. **Pass.** Build spend is $28.55 of $40.

**Probe N3 ($0.35, cap $0.50)** opened a session log only. The entry's `ts` is `null`, and the guard's receipt for the write carries `2026-11-26T01:30:06Z`. **Pass.** Build spend is $28.90 of $40.

For item 5, a PreToolUse hook could rewrite the logged time. A second-hand reading of the hooks documentation says a rewritten input goes with `allow` (which skips the permission prompt) or with `ask`, and it could not confirm the case with no decision. Rather than risk changing how permissions behave, the guard does not rewrite tool input. Row 5 covers the session log only: `chat.jsonl` entries still carry times the agents write, and the readers that use time windows (`keeper-test`, `finops`, `capacity`, `rhythm`) are unchecked.

## Prompt-diff review (CONSTITUTION §5.3), 2026-11-25

Covers the `agents/ceo.md` edits from #15, #18 and #19. The review of #15 and #18 happened after they landed.

- **Round 1 (CRT, from the diffs alone): REJECT.** The skip rules had no carve-out for mandatory steps or USER-ONLY actions.
- **Fixes in #19.** A step a root document makes mandatory (a §3.3 gate verdict, the §5.8 lessons row, the ADR for a material decision) is never skipped; the CEO stops, files it in `inbox.json` and reports blocked. A recorded default never stands in for a USER-ONLY action (§2.2). The guard also refuses an append-only file it cannot decode.
- **Probe S2 ($0.18, cap $0.50):** a refused lessons row blocks the close, a blocking red waits for the Chairman, and a routine refusal is logged and skipped. **Pass.**
- **Round 2 (CRT, full files): APPROVE (verdict A).** `adversarial-prompter` was not run, because the review was read-only with no dispatch. Residual: the carve-out names three step classes, so other mandatory steps still fall under "skip and continue".
- Both rounds are recorded verbatim in `docs/adr/ADR-0011-workspace-lessons-and-memory-index.md`.
- Stone matching (prompt-diff step 3) was not run. The repository holds no `_vision/playbooks/ARCHIVE.md` and no stones, so no stone covers `agents/ceo.md`.
- **Spend.** L1 + both review rounds + S2 = $1.25. Build spend is $30.15 of $40.

## Live run N4: N1 repeated on the final base (cap $5)

Same idea, prompt and fixture as N1, on `4f0d1c2` (after #17 to #20). This is not the 6b reference run or V14.

**Pass criteria, written before the run:**
1. Every workspace record is under `outputs/devsecops-agency/`. Nothing is written at the launch folder's top level except the guard's `.devsecops-agency/` receipts.
2. Vision bootstrap, OKR scoring and light dreaming are each attempted or logged as skipped. None is skipped silently.
3. The CEO clears no blocking-council red itself. A red is fixed in a fix loop and re-verified by the council, or filed in `inbox.json` with the project blocked.
4. If the run reaches close, the ledger row is in `outputs/devsecops-agency/LESSONS.md`, and the plugin copy's `LESSONS.md` is unchanged.
5. Session-log `ts` values are `null` unless read from a tool.
6. No B2 refusal of a legitimate memory write.

**Recorded, not pass or fail:**
- specialist dispatches per chief (N1-b);
- how far the run gets.

If N1's red recurs and the run ends blocked before close, that is a pass for criterion 3. The close path is then covered by a close-only probe (cap $1), with no rerun.

### N4 results ($4.37)

The run went end to end and closed **blocked**. Verification could not execute the tests, and the CEO filed that in `inbox.json` instead of claiming a pass. Every test agent was refused the shell by **my run settings**, not by the agency. `test-runner` and `frontend-dev` ran `cd "<folder>" && node --test …` (hook log), and the harness allow-list does not match that compound form. The guard refused no shell call. So the blocked close is partly a harness artifact, and no shell grant is asked for. **My re-run of the three test files gives 43 passed, 0 failed.** CAO was yellow, CEVO yellow and CRT green, and no blocking red was raised.

| # | Criterion | Result |
|---|---|---|
| 1 | Records under `outputs/devsecops-agency/` | **Pass.** Nothing at the top level except `.devsecops-agency/` receipts |
| 2 | Vision, OKR, light dreaming attempted or logged | **Partial.** `VISION.md` and `_vision/projects/tip-calculator.md` were written, and every report carries `okr_alignment`. Light dreaming wrote no `memory/<date>.md` and logged no skip. Deep dreaming wrote `patterns/tip-calculator.md` |
| 3 | No blocking red cleared by the CEO | **Pass.** None was raised; the stop rule sent the unverified tests to the Chairman |
| 4 | Ledger row in the workspace file, plugin copy unchanged | **Pass** |
| 5 | Session-log `ts` is `null` unless read from a tool | **Fail.** All 10 entries carry invented times (`2026-11-25T00:00:01Z` onward), while the receipts show 2026-11-26 01:55 UTC onward. The CEO read only the `ceo` and `rhythm` skills, never `session-log`, so the `null` rule did not reach it (as in N1-a). |
| 6 | No B2 refusal of a legitimate memory write | **Pass.** Six refusals, all B5: four engineering-lead writes of app code, devops-lead `ops/local-run.md` and red-team-lead `redteam/pre-release.md` |

**Recorded:**
- **Specialist dispatches (N1-b).** CRO 1, CPO 1, CQO 2 and engineering-lead 1 per build round. Security, docs, devops, GC, CAO, CEVO and CRT had none.
  - For seven of the 14 chief dispatches, the CEO's prompt said not to dispatch specialists, for budget.
  - Engineering-lead first tried to write the app itself and was refused (B5), then dispatched `frontend-dev`.
- **The CRO's refusal came from Claude Code, not the guard.** The CRO's Write of `research/findings.md` (in its scope) was refused by the platform: "Subagents should return findings as text, not write report files." So no guard receipt exists. This affects every chief that writes its own report file.
- **Card mismatches came from the CEO's prompts.** The CEO named `ops/local-run.md` for devops-lead and `redteam/pre-release.md` for red-team-lead. Neither matches those agents' scopes (`deploy/`, `red-team/`), and both were refused (B5). No scope is changed here.
- **Budget confound.** The CEO wrote "Chairman's session budget (USD 5 total)" into `brief.md` and told chiefs to run lean. My prompt never stated a budget, and the stream shows no source before the CEO's own first mention, so the figure presumably reached it from the run's `--max-budget-usd`. Until that is separated out, N1-a and N1-b cannot be told apart from the cap, so no prompt was edited for them in N4. The Chairman's second set of defaults (below) later settled N1-b by rule.
- **Fixture error (mine).** The seeded `state.json` carried the UTC date, 2026-11-26. The CEO took it to be the future, so it neither trusted nor rewrote it, and logged an error. So F5, a live rhythm write, is still unproven.
- **Spend.** Build spend is $35.21 of $40, including the draft reviews below ($0.69).

### Default 5, completed after N4

N3 had passed only because its prompt pointed at the logging step. N4 showed that in a full run the CEO never opens `skills/session-log`. So the `skills/ceo` session-open step (step 8) now states the entry's fields and the `ts: null` rule itself. It restates the `session-log` rule that CRT approved in round 2, so it gets no new review.

**Probe N5 ($0.45, cap $0.50).** The prompt never mentioned the log. All three entries have `ts: null` and the full field set. **Pass.** Build spend is $35.66 of $40.

## Chairman's second set of defaults (2026-11-26 UTC)

**Approval (§10.4), in the chat interface.** After N4, the open items were put to the Chairman as written below:

> 1. Keep the three additions the reviewers forced.
> 2. Don't let the CEO tell a chief to skip its specialists to save money; it reports to you instead.
> 3. Give the CEO the parallel work-copy folder (`_worktrees/`).
> 4. Add a browser-test specialist with the Phase 3 roles.
> 5. Accept the recommended options in drafts #13 and #14, then run their second review.
> 6. Fund the full reference run at about $10 once #14 settles.
> 7. No default for these: the signing identity for Phase 2b and the accounts for the live-URL thin slice.

The Chairman's reply: "Accept all defaults". That covers items 1 to 6. Item 7 has no default and stays open.

| # | Item | What landed | Where |
|---|---|---|---|
| 1 | The three forced additions | Kept as merged: the closed-project ledger abort, the guard's `knobHistory` check, the CEO's stop at mandatory steps | ADR-0011, `hooks/guard.py`, `agents/ceo.md` |
| 2 | Trimming a council for budget (N1-b) | The CEO never tells a chief to skip its specialists, run lean or cut its council. If the budget cannot cover a council, it stops before that dispatch, files the item in `inbox.json`, reports the project as blocked and waits for the Chairman, as for a Rung 6 consult (`skills/budget`, whose own trigger is a burn over 110 % or a forecast over 150 %). No root document allows trimming: `RESILIENCE.md`'s budget-degraded mode tightens only the fix-loop cap. | `agents/ceo.md`, `skills/ceo/SKILL.md` (dispatch step) |
| 3 | `_worktrees/` (F4) | **Not granted.** CRT rejected the grant in its §5.3 review (below). The CEO is told not to allocate a worktree or write under `_worktrees/`, and a test confirms the card grants no `worktree.json` and no worktree artifact. *Known gap:* the CEO's file-name entries (`status.json`, `inbox.json`, `brief.md`, `retro.md`, `adr-*.md`, `ADR-*.md`, `LESSONS.md`) and folder entries (`_decisions/`, `_meetings/`, `_memory/` and the `_vision/` ones) match at any depth, so the guard would still let it write, say, `<slug>/_worktrees/red-team-x-1/status.json`. Only the prompt rule stops that. | `agents/ceo.md`, `skills/ceo/SKILL.md`, `hooks/test_guard.py` |
| 4 | Browser-test specialist (N1-d) | Recorded only. It is built with the Phase 3 roles. Until then, browser checks are recorded as "not run". | No change |
| 5 | Drafts #13 and #14 | Revised to the accepted options in the draft branches; their second review is recorded in each draft | Draft PRs |
| 6 | Reference run (6b) | Funded at about $10, to run once the Chairman approves #14's final text | Not run |

**Why item 3 was not granted.** A $0 sweep of the `worktree` skill found that the grant would not deliver parallel work. The merge copies the chief's `writes[]` into the main tree and moves the folder to `_worktrees/_merged/`. The CEO holds neither write and has no shell (F2, not granted). CRT's §5.3 review then rejected even a narrowed grant, `_worktrees/*/worktree.json`, on three grounds:
- `fnmatch`'s `*` matches `/`, so the pattern covers any file named `worktree.json` at any depth, including inside a chief's code and under `_merged/`;
- it lets the CEO rewrite a red-team worktree's control file (`status`, `writes[]`), against red-team independence (`red-team-lead.md:70`, CONSTITUTION §3.5);
- the same change tells the CEO not to use it, so it is privilege without use.

So F4 is a design question for the Chairman: who merges a worktree? Recommended: the owning chief copies its own `writes[]` into the main tree on the CEO's merge entry, and the guard gains an exact-depth rule so that the CEO holds `<slug>/_worktrees/<chief>-<n>/worktree.json` for non-red-team worktrees only.

**Item 2, probe P2 ($0.22, cap $0.50).** The CEO was told a phase budget covered the security chief's own turn but not its specialists, and was asked what it does next, with no dispatch or write allowed. It did not dispatch, and it did not offer a trimmed dispatch. It would file the gap in `inbox.json`, report the project blocked at Phase 2 and wait for the Chairman, and it quoted the new rule. **Pass** for the stated case. A full run where the budget runs out mid-project is still unproven.

### CONSTITUTION §5.3 prompt-diff review (CRT, 2026-11-26 UTC)

Round 1 ran read-only on CRT's own tier, with the full files ($0.23). It reviewed the first version of this change, which granted `_worktrees/*/worktree.json`.

| CRT finding | Response |
|---|---|
| 1–3. The pattern reaches any depth, the tests miss it, and it lets the CEO edit red-team control files | Grant dropped. The test now checks that the card grants no `worktree.json` and no worktree artifact, including the deep, `_merged/` and red-team cases CRT named. |
| 4. The grant is unused and the worktree text contradicts it | Grant dropped. The worktree step in `skills/ceo` says no worktree exists until F4 has an owner. |
| 5. "Rung 6" is loose, and the rule does not say the project waits | Reworded: the CEO stops before that dispatch, reports blocked and waits, "as for" a Rung 6 consult. Rung 6's own thresholds are named in the table above. |
| 6. The bullets sit between numbered steps | Not changed. They follow the existing bullets under step 1 of `agents/ceo.md`. |
| 7. Item 2 is unproven live | Agreed at review time. Probe P2 (above) later passed the stated case. |

#### Round 1, CRT (`red-team-lead`): REJECT

No root document conflicts with the council rule, but the new scope entry is wider than the change says it is. The tests don't cover that gap.

VERDICT: REJECT

1. **The scope entry is wider than stated** (`agents/role-cards.yaml:296`, `hooks/role-cards.json` +163). `hooks/guard.py:182` matches an entry with `fnmatch` on `r` and on `"*/" + e`. The `*` in `_worktrees/*/worktree.json` also matches `/`.
   - So the CEO can write any file named `worktree.json` at any depth under any `_worktrees/`. Examples are `app/_worktrees/engineering-lead-1/src/worktree.json`, `.../red-team/worktree.json` and `_worktrees/_merged/<id>/worktree.json`.
   - That reaches a chief's code and red-team folders and the audit archive. It also reaches any project source file that happens to be named `worktree.json`.
   - `agents/ceo.md:39` and `docs/vision/CEO-ENTRY-REVIEW.md:234` say the CEO "writes only `worktree.json`", and the review file says the entry avoids covering code and red-team content. Both overstate what the pattern enforces.
   - Fix: there is no glob that matches one level only. Either add an exact-depth rule in `in_scope`, or drop the entry until the worktree has an owner.

2. **The tests miss the abuse the diff itself notes** (`hooks/test_guard.py:363-376`). `fnmatch` `*` matching `/` is the very reason the entry was narrowed, yet no test covers it.
   - The negative cases are all non-`worktree.json` names (`architecture.md`, `app.js`, `findings.md`). No case is `.../src/worktree.json`, `.../red-team/worktree.json` or `_merged/x/worktree.json`.
   - Those three would pass `in_scope`, so the test name `does_not_write_worktree_contents` is unproven.
   - `src/app.js` and `app/src/app.js` are trivial negatives, because they never hit the `_worktrees` pattern.
   - Only the first positive case is also checked under the `outputs/devsecops-agency/` prefix.
   - The review file's claim "Guard tests cover both sides" (`CEO-ENTRY-REVIEW.md:234`) is therefore overstated.

3. **Red-team independence and §3.5 separation are weakened.** The CEO can now rewrite the `worktree.json` of any `red-team-*` worktree. That file sets `writes[]` and `status` (`skills/worktree/SKILL.md:49-72`), and the merge step trusts it.
   - The CEO could set `status: discarded`, or change `writes[]`, on a red-team worktree. That is a delivery-path actor editing the control file of an independent council.
   - It conflicts with `agents/red-team/red-team-lead.md:70`, which limits red-team worktrees to red-team's own writes. It also cuts against the §3.5 and §3.3 spirit, since a red-team worktree's red could be quietly closed.
   - A prompt line saying "never red-team content" is not enforcement, and the guard cannot enforce it.
   - The diff does not exclude `_worktrees/red-team-*/`, which would be easy to do.

4. **Contradictory text on worktrees.** `agents/ceo.md:39` and `skills/ceo/SKILL.md:186` tell the CEO not to allocate worktrees. The grant exists for allocation and status updates (`CEO-ENTRY-REVIEW.md:239`), so it is unused.
   - `skills/ceo/SKILL.md:192` still instructs "Merge or discard the worktree (if any)".
   - `skills/ceo/SKILL.md:57` and `:203` still require no open worktrees before a phase advances.
   - `skills/worktree/SKILL.md:77` and `:85-92` still say the CEO allocates and merges.
   - `agents/red-team/red-team-lead.md:58` has red-team specialists "dispatch via `skills/worktree`", so red-team worktrees will exist. The CEO text says it cannot merge them, and no document names who does.
   - A scope grant that the same change says to leave unused is unneeded privilege. It is also inconsistent with the Chairman's request, which the review file itself says was only partly closed (F4).

5. **The council rule does not weaken any root rule, but part of it is inaccurate.**
   - `agents/ceo.md:38` and `skills/ceo/SKILL.md:185` do not conflict with `RESILIENCE.md:35` or `CONSTITUTION.md §7.3`. Budget-degraded mode only tightens the fix-loop cap, so the claim at `CEO-ENTRY-REVIEW.md:233` holds.
   - "The Rung 6 consult" is a loose fit. `skills/budget/SKILL.md:58-59` and `:93` trigger Rung 6 on a burn above 110% or a forecast above 150%.
   - A council that merely "cannot be covered" below those thresholds has no defined rung. The rule is sound, but its stated trigger should name those thresholds.
   - Also, the CEO files to `inbox.json` and "reports to the Chairman" without saying the project then waits. The CEO's stop-at-mandatory-step wording at `ceo.md:35` is the natural model to reuse.

6. **Formatting.** The new bullets at `agents/ceo.md:38-39` sit between numbered steps 2 and 3, unindented, so they read as top-level list items rather than sub-bullets of step 2. This is minor.

7. **"Item 2 is unproven live"** (`CEO-ENTRY-REVIEW.md:241`) is honest. No probe shows the CEO stops telling chiefs to run lean, and the review file says so itself.

#### Round 2, CRT (`red-team-lead`): REJECT ($0.13)

The revision resolves the round-1 findings, but one new claim is false, so I'm rejecting it.

**Round-1 findings**
- **1–3 (scope grant, tests, red-team control file):** Resolved. `ceo` write_scope in `agents/role-cards.yaml:279-295` has no `_worktrees` entry, so the over-wide `fnmatch` grant and the red-team exposure are gone. The new test covers the deep, `_merged/` and red-team `worktree.json` paths.
- **4 (contradictory worktree text):** Mostly resolved. `skills/ceo/SKILL.md:186` now says to write to the main tree and record `worktree: null`, and the CEO has no grant it doesn't use. Some text still assumes the CEO merges:
  - `skills/ceo/SKILL.md:192` says "Merge or discard the worktree (if any)". The "(if any)" and the `worktree: null` rule make this harmless.
  - `skills/worktree/SKILL.md:15` and `:77` still say the CEO allocates and merges.
  - Red-team worktrees will still exist (`red-team-lead.md:58`), and no document says who merges them. The review file records this as open F4, so it is disclosed.
- **5 (Rung 6 wording, project waits):** Resolved. The text now says to stop before the dispatch, report blocked and wait, "as for" Rung 6. The review table names `skills/budget`'s 110% and 150% triggers.
- **6 (bullet placement):** Not changed, and the response is reasonable. The bullets follow the existing bullets under step 1.
- **7 (item 2 unproven live):** Acknowledged in the review file.

**Rule weakening:** None. The council rule is consistent with `RESILIENCE.md` and `skills/budget`. Rung 6 is still the only route to expand a budget. The mandatory-step stop at `ceo.md:35` is untouched.

VERDICT: REJECT

1. **"The CEO writes nothing under `_worktrees/`" is false.**
   - Sources: `docs/vision/CEO-ENTRY-REVIEW.md` (diff lines 59 and 79), `hooks/test_guard.py` (diff lines 134-141), `agents/ceo.md:39`.
   - Cause: `hooks/guard.py:182` matches non-folder entries with `fnmatch` on `r` and on `"*/" + e`, and `*` matches `/`. The CEO scope has the entries `status.json`, `inbox.json`, `brief.md`, `retro.md`, `adr-*.md`, `ADR-*.md` and `LESSONS.md` (`role-cards.yaml:280-289`).
   - Effect: these match at any depth. The CEO can write `app/_worktrees/red-team-x-1/status.json` or `app/_worktrees/cto-0/adr-1.md`.
   - The test cases (`worktree.json`, `architecture.md`, `app.js`) avoid those names, so the test passes while the claim stays unproven.
   - This is mostly an old over-breadth, not something the revision introduced. But the review file and the test name `test_ceo_writes_nothing_under_worktrees` assert something the guard doesn't enforce, which is the same kind of overstatement as round-1 finding 1.
   - Fix, either of these:
     - Reword the claim and test to "no `worktree.json` grant, and no `worktree.json` write". Add the colliding names as documented known gaps.
     - Add an `_worktrees/` deny to `in_scope` or the guard and test it with `status.json` and `adr-1.md` cases.

2. **Red-team worktrees and `skills/worktree/SKILL.md` are still unaligned (`skills/worktree/SKILL.md:15,77,87-100`; `skills/ceo/SKILL.md:57,203`).**
   - The skill still says the CEO allocates and merges.
   - The phase-advance rule at `skills/ceo/SKILL.md:203` ("no `_worktrees/*/worktree.json` open") would block on any red-team worktree the CEO can't close.
   - Add a one-line note to the worktree skill, pointing at F4, that CEO allocate and merge is suspended. Otherwise a phase can deadlock.
   - I'd accept this as a follow-up if the fix for finding 1 lands.

3. **Date inconsistency (`CEO-ENTRY-REVIEW.md`, diff lines 41 and 73).** The Chairman approval and the CRT review are dated 2026-11-26, but the current date is 2026-11-25. The same file says a UTC-date fixture caused an earlier error. Confirm the dates are intended.

#### Response to round 2

| CRT finding | Response |
|---|---|
| 1. "The CEO writes nothing under `_worktrees/`" is false: its file-name entries match at any depth | Reworded in the table, the test name and `agents/ceo.md`. The colliding names are listed as a known gap. A guard deny for `_worktrees/` is not added. A CEO-only deny would be small, but it is left to F4, which settles who writes there. |
| 2. The worktree skill still says the CEO allocates and merges; an open red-team worktree could deadlock a phase | `skills/worktree` now opens with a note that CEO allocation and merge are suspended under F4. The phase-advance rule in `skills/ceo` says an open red-team worktree is filed in `inbox.json` and the phase reported blocked. |
| 3. Dates | The headings now say UTC. The session's local date is 2026-11-25; UTC is 2026-11-26. |

#### Round 3, CRT (`red-team-lead`): APPROVE ($0.14)

Round 3 is approved. Both round-2 findings that needed a fix are resolved, and the date check holds up. I found nothing new that is false or weakens a rule. I read the diff, the post-change files and the round-1 and round-2 verdicts. I also read `agents/role-cards.yaml` and `hooks/guard.py` (`in_scope`) in `./review/after/`.

**Round-2 findings**
- **Finding 1, the false claim that the CEO writes nothing under `_worktrees/`: resolved.**
  - The test is now `test_ceo_has_no_worktree_grant`, which asserts only what the guard enforces. I traced all six parametrised paths through `in_scope` against the CEO scope at `role-cards.yaml:279-295`. None matches, with or without the `outputs/devsecops-agency/` prefix, so the test passes.
  - `agents/ceo.md:39` is now a prompt rule, not a claim about the guard.
  - The review file's "Known gap" in the item-3 table discloses that `status.json`, `adr-*.md` and the other file-name entries still match at any depth. That is accurate against `guard.py:182`.
- **Finding 2, worktree skill unaligned: resolved.**
  - `skills/worktree/SKILL.md:15` now says CEO allocation and merge are suspended under F4.
  - `skills/ceo/SKILL.md:210` (phase-advance rule) now files an open red-team worktree in `inbox.json` and reports the phase blocked.
  - Only `red-team-lead` references `skills/worktree` among the agents, so "only a red-team worktree can be open" is true.
  - The skill body at lines 17 and 140 still describes the CEO merging. The suspension note scopes it out, so I accept that.
- **Finding 3, dates: resolved.** The headings now say UTC, and the explanation matches the fixture-date issue the file already records. I can't verify the local-versus-UTC offset from here.

**Non-blocking observations**
1. `docs/vision/CEO-ENTRY-REVIEW.md` (round-2 response row 1) says a guard deny for `_worktrees/` "would change every card". A CEO-only deny would not. The deferral to F4 is still reasonable, but the reason is overstated.
2. The "Known gap" list in the review file (diff line 59) names only the file-name entries. The CEO's folder entries (`_decisions/`, `_memory/`, `_meetings/`) also match at any depth. It is the same class of gap, so please add them.
3. `skills/ceo/SKILL.md:210` can block a phase indefinitely on an open red-team worktree. It is routed to the Chairman via `inbox.json`, so it is disclosed and not a deadlock. F4 stays open.
4. Item 2 (the council rule) is still unproven live. The review file says so itself.

VERDICT: APPROVE

1. `docs/vision/CEO-ENTRY-REVIEW.md` (diff line 167): the claim that a `_worktrees/` deny "would change every card" is overstated (non-blocking).
2. `docs/vision/CEO-ENTRY-REVIEW.md` (diff line 59): add the folder entries (`_decisions/`, `_memory/`, `_meetings/`) to the known-gap list (non-blocking).
3. `skills/ceo/SKILL.md:210`, `skills/worktree/SKILL.md:17,140`: stale CEO-merge text remains, covered by the suspension note at `skills/worktree/SKILL.md:15`. Clean it up when F4 gets an owner (non-blocking).

Non-blocking notes 1 and 2 are applied (the deny wording and the folder entries in the known gap). Note 3 waits for F4. Review spend for this change is $0.50 (rounds 1 to 3). Build spend is $36.16 of $40. The merged head differs from the commit CRT approved only by the wording of non-blocking notes 1 and 2, a changed agent name in the `skills/worktree` note (to pass `dispatch_names.py`), and this record.

**Spend after the second set of defaults.** Draft round-2 reviews for #14 cost $1.19 (four reviewers) and for #13 $0.20. Probe P2 cost $0.22. Build spend is $37.77 of $40.
