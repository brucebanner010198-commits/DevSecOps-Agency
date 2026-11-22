# Phase 1a review pack: the enforced contract

Status: **for the Chairman's prompt-diff review.** The changes are committed on the local branch `feat/phase-1a-enforced-contract`, which is not pushed or merged.

## Merge condition

**Phase 1a must not merge ahead of Phase 2a's write guard.** Removing Edit leaves `Write`, which replaces a whole file. Twelve agents that lost Edit are told to append to files they share with others, so they can now append only by rewriting:
- `qa-lead` and `security-lead` add entries to `chat.jsonl`;
- four red-team testers add to `findings.md`;
- `code-auditor` adds a section to `threat-model.md`;
- `panel-chair` adds rows to its rotation log and the cost CSV;
- `dlp-scanner` and `mcp-defender` add to append-only JSONL;
- `cao` adds correction lines;
- `token-compactor` adds roll-ups.

The guard planned as 2a's first rule: on any path the repo calls append-only, a `Write` to an existing file passes only if the new content starts with the current content, and a write outside the caller's scope is refused.

**The alternative for you:** restore Edit to those twelve agents until 2a lands, accepting that they can then change what they review.

## What changes

The single source for each agent's enforced fields is now `agents/role-cards.yaml`. `scripts/role_cards.py write` puts `tools`, `effort` and `maxTurns` into each agent file. `check` runs in CI and fails on:
- drift between a card and its agent file;
- an orchestrator holding Bash;
- web access together with a shell;
- a CEO holding Edit or Bash;
- an unknown tool;
- a held grant;
- an example left in a description;
- a model line that differs from the card.

Model lines are never written, because tier changes are the Chairman's.

Commits, each reviewable alone:

1. **Removals** (52 agents). Part 14's "remove" items. `Task` is spelled `Agent`; it stays a runtime alias. `TodoWrite` is dropped, because it is not a live tool.
2. **Like-for-like additions** (2 agents): Write for `code-auditor`, and Grep and Glob for `panel-chair`.
3. **Web access** (7 agents). The one place 1a widens reach: WebSearch and WebFetch for the research and strategy specialists on Haiku. You can refuse this commit on its own.
4. **Limits** (93 agents). `effort` and `maxTurns`. The mapping is my reading of plan Part 2B, Stage 2:
   - mechanical specialists: low effort, 20 turns;
   - judgment specialists: medium, 25. That covers the architects, the engineers, `code-auditor`, `threat-modeler`, `pen-tester`, `test-designer` and every Sonnet specialist, a list I chose;
   - chiefs and leads: medium, 30. The plan gives executives 15, but here the chiefs both decide and run their councils;
   - board director: high, 20;
   - CEO: no limit.

   Both keys were probed live: `maxTurns: 2` stopped a Haiku agent after two calls, and Haiku accepted `effort: low`.
5. **Examples moved** from 87 descriptions into the body, word for word. Descriptions go from about 19,250 to about 7,600 tokens, under Part 2B's 8,000 target.
6. **Role cards, lint, launcher, CI and tests.** `scripts/agency.sh` and `agency.ps1` start a session as the CEO agent. A project `.claude/settings.json` with `{"agent": "devsecops-agency:ceo"}` does the same; this was probed, and the session got exactly the CEO's new grant.

## Evidence: D3 with the CEO started as an agent (D3a)

D3a ran on a scratch plugin where **only `ceo.md` changed**: Read, Grep, Glob, Agent and Write. Every chief and specialist kept its old grant, so the other removals were not tested live by D3a; the regression run tests them. D3a also changed two things at once: `--agent` and the smaller CEO grant. The pipeline engaged with both. The run does not show which one caused it. Cost **$6.78** (Opus $2.55, Sonnet $3.90, Haiku $0.34); 33 minutes.

- **Dispatches:** 29 in total, counted from the stream.
  - 11 distinct chiefs: `cro`, `pm-lead`, `engineering-lead` (×4), `security-lead` (×2), `qa-lead`, `devops-lead` (×3), `docs-lead`, `gc`, `cao`, `evaluation-lead` and `red-team-lead`.
  - 12 distinct specialists.
  - The built-in `web-fetch` agent, once.
  - Baseline D3, recounted from its stream, had 1 dispatch.
- **Tests:** 114 pass when run independently.
- **The CEO did not edit code.** Its writes were the brief, the status, the inbox, `chat.jsonl` (4 whole-file rewrites, each keeping every earlier line), five ADRs, the retro and `red-team/findings.md`.
- **`red-team/findings.md`:**
  - The CEO says `red-team-lead`'s own write was rejected; the cause is unverified.
  - The CEO then wrote a condensed version. The gate (yellow) and the counts (0 critical, 0 high, 2 medium, 3 low, 3 info) are unchanged. The detail sections are dropped: the info items, the workflow checks and the full repros.
- **`LESSONS.md`:** the CEO tried to `Write` the plugin's own `LESSONS.md` with the text `PLACEHOLDER`. Claude Code refused it as a sensitive file. The export was unchanged before and after. The run gives no reason for the attempt.
- **Attribution limit:** the stream does not carry nested specialists' messages. So the turn and write counts cover the CEO and the chiefs only, and a chief's writes cannot be separated from its specialists'. The regression run adds a hook that logs each call's `agent_type` and path.
- **Denials:** the shell (9) and WebFetch (5) denials came from the run's own allowlist, not from agent grants.
- **Turn limits:** no chief exceeded its planned `maxTurns`. The highest was `engineering-lead` at 21 of 30.
- **Confounder:** the session still read the user-level `CLAUDE.md`. Its final message quoted the "Projects/<owner>/<repo>" rule.
- **2a test fixture:** this stream. The four `chat.jsonl` rewrites must pass the append guard, and the findings rewrite must be refused. Part 14's CEO scope also omits `brief.md` and `_meetings/`, which the CEO wrote, so the scope list needs both.

## Decisions this pack needs

1. Accept the stage commits, or refuse any one of them. Commit 3, web access, is the natural one to consider.
2. Merge only after 2a's write guard, or restore Edit to the twelve appenders in the meantime.
3. `chaos-engineer`'s Bash: Part 14 adds it, but its body forbids it.
4. `pm-lead`'s design search now dispatches `frontend-dev`. That is a cross-council dispatch, which 2a's "own specialists" rule would refuse. Allow it as an exception, or give a product specialist a read-only shell.
5. The limits mapping above, especially chiefs at 30 turns rather than executives at 15.

## Conflicts between Part 14 and review A's F13 (not resolved in 1a)

| # | Conflict | What 1a does |
| --- | --- | --- |
| 1 | `deployment-engineer`, `ci-engineer` and `observability-engineer` keep a full shell on Haiku with deploy targets: all three legs of the Rule of Two | Keeps Part 14. The fix is a narrow deploy tool (E3), which is not approved |
| 2 | Engineers hold untrusted code, package egress and vault references | Keeps Part 14. No vault references exist yet |
| 3 | Reviewers with a shell (`code-auditor`, `pen-tester`) can change what they review through the shell | Keeps Part 14. Only an OS sandbox or a read-only checkout fixes this (E5) |
| 4 | "Own specialists only" for chiefs | Not enforceable by `tools:` in a subagent. Needs a dispatch hook (2a) |
| 5 | "Allowlisted egress" for researchers | No enforcer: the sandbox allowlist does not cover WebFetch. Needs a hook (2a) |
| 6 | `skill-creator` writes into `agents/` and `skills/` in the install folder, which an update replaces | Unchanged; flagged |
| 7 | `chaos-engineer`: Part 14 adds Bash, but its own instructions forbid Bash | **Held.** Not added; decide which wins |

## Instruction fixes made so that removals don't break agents

- `engineering-lead`: the build smoke check is now run by the specialist who built it.
- `pm-lead`: the design search script is now run by `frontend-dev`, through dispatch (decision 4).
- `readme-writer`: "Use Bash + Grep" becomes "Use Grep".

Stale but harmless: five reviewers' "Must not use Bash" lines still say "Read/Grep/Glob/Write/Edit cover every step".

## What 1a does not achieve

- **`Write` is unscoped until 2a.** So "readers of evidence cannot edit evidence" (rule 4) and "the CEO cannot change code" are not met yet.
- **"Sandboxed" and "read-only" shell are labels in the cards.** Native Windows has no sandbox (E5).
- **The minimum pipeline is still advisory.** Starting the CEO as an agent made it convene the pipeline in this run, but nothing enforces it.

## Agent-by-agent tool diff (Part 14 against the files at `96fe709`)

| Agent | Model | Current | Target (Part 14) | Removed | Added | Body still mentions |
| --- | --- | --- | --- | --- | --- | --- |
| `engineering-lead` | sonnet | Read, Write, Edit, Bash, Grep, Glob, Agent | Read, Grep, Glob, Agent, Write, Edit | Bash | - | Bash:1 |
| `adr-auditor` | haiku | Read, Grep, Glob, Write, Edit, Bash | Read, Grep, Glob, Write, Bash (read-only) | Edit | - | Edit:1 |
| `agent-governance-reviewer` | sonnet | Read, Grep, Glob, Write, Edit | Read, Grep, Glob, Write | Edit | - | Edit:1 |
| `cao` | sonnet | Read, Write, Edit, Grep, Glob, Task | Read, Grep, Glob, Agent, Write | Edit | - | Edit:2 |
| `gate-auditor` | haiku | Read, Grep, Glob, Write, Edit | Read, Grep, Glob, Write | Edit | - | - |
| `memory-auditor` | haiku | Read, Grep, Glob, Write, Edit, Bash | Read, Grep, Glob, Write, Bash (read-only) | Edit | - | - |
| `okr-auditor` | haiku | Read, Grep, Glob, Write, Edit | Read, Grep, Glob, Write | Edit | - | - |
| `ceo` | opus | Read, Write, Edit, Bash, Grep, Glob, Task, TodoWrite | Read, Grep, Glob, Agent, Write | Edit, Bash, TodoWrite | - | - |
| `devops-lead` | sonnet | Read, Write, Edit, Bash, Grep, Glob, Agent | Read, Grep, Glob, Agent, Write, Edit | Bash | - | - |
| `docs-lead` | sonnet | Read, Write, Edit, Bash, Grep, Glob, Agent | Read, Grep, Glob, Agent, Write, Edit | Bash | - | - |
| `readme-writer` | haiku | Read, Write, Edit, Bash, Grep, Glob | Read, Grep, Glob, Write, Edit | Bash | - | Bash:4 |
| `benchmark-runner` | haiku | Read, Write, Edit, Grep, Glob, Bash | Read, Grep, Glob, Write, Bash (sandboxed) | Edit | - | - |
| `budget-monitor` | haiku | Read, Write, Edit, Grep, Glob | Read, Grep, Glob, Write | Edit | - | - |
| `eval-designer` | haiku | Read, Write, Edit, Grep, Glob | Read, Grep, Glob, Write | Edit | - | - |
| `evaluation-lead` | sonnet | Read, Write, Edit, Grep, Glob, Task, Bash | Read, Grep, Glob, Agent, Write | Edit, Bash | - | - |
| `finops-analyst` | sonnet | Read, Grep, Glob, Write, Edit | Read, Grep, Glob, Write | Edit | - | Edit:1 |
| `panel-chair` | sonnet | Read, Write, Edit, Bash, Task | Read, Grep, Glob, Agent, Write | Edit, Bash | Grep, Glob | - |
| `regression-detector` | haiku | Read, Write, Edit, Grep, Glob | Read, Grep, Glob, Write | Edit | - | - |
| `skill-evaluator` | sonnet | Read, Grep, Glob, Write, Edit | Read, Grep, Glob, Write | Edit | - | Edit:1 |
| `token-compactor` | haiku | Read, Write, Edit, Grep, Glob, Bash | Read, Grep, Glob, Write | Edit, Bash | - | - |
| `compliance-drift` | sonnet | Read, Write, Edit, Grep, WebFetch, Bash | Read, Grep, Write, WebFetch | Edit, Bash | - | - |
| `gc` | sonnet | Read, Write, Edit, Bash, Grep, Glob, Task | Read, Grep, Glob, Agent, Write | Edit, Bash | - | - |
| `ip-lineage` | haiku | Read, Write, Edit, Grep, WebFetch, Bash | Read, Grep, Write, WebFetch | Edit, Bash | - | - |
| `license-checker` | haiku | Read, Write, Edit, Bash, Grep, Glob | Read, Grep, Glob, Write, Bash (sandboxed) | Edit | - | - |
| `privacy-counsel` | haiku | Read, Write, Edit, Grep, Glob | Read, Grep, Glob, Write | Edit | - | - |
| `pm-lead` | sonnet | Read, Write, Edit, Bash, Grep, Glob, Agent | Read, Grep, Glob, Agent, Write, Edit | Bash | - | Bash:1 |
| `a11y-auditor` | haiku | Read, Write, Edit, Bash, Grep, Glob | Read, Grep, Glob, Write, Bash (sandboxed) | Edit | - | - |
| `performance-tester` | haiku | Read, Write, Edit, Bash, Grep, Glob | Read, Grep, Glob, Write, Bash (sandboxed) | Edit | - | - |
| `qa-lead` | sonnet | Read, Write, Edit, Bash, Grep, Glob, Agent | Read, Grep, Glob, Agent, Write | Edit, Bash | - | - |
| `adversarial-prompter` | haiku | Read, Write, Edit, Grep, Glob, Bash | Read, Grep, Glob, Write, Bash (sandboxed) | Edit | - | - |
| `chaos-engineer` | sonnet | Read, Grep, Glob, Write, Edit | Read, Grep, Glob, Write, Bash (sandboxed) | Edit | Bash | Edit:1 |
| `data-exfil-tester` | haiku | Read, Write, Edit, Grep, Glob, Bash | Read, Grep, Glob, Write, Bash (sandboxed) | Edit | - | - |
| `red-team-lead` | sonnet | Read, Write, Edit, Grep, Glob, Task, Bash | Read, Grep, Glob, Agent, Write | Edit, Bash | - | - |
| `social-engineering-tester` | haiku | Read, Write, Edit, Grep, Glob | Read, Grep, Glob, Write | Edit | - | - |
| `tool-abuse-tester` | haiku | Read, Write, Edit, Grep, Glob, Bash | Read, Grep, Glob, Write, Bash (sandboxed) | Edit | - | - |
| `literature-reviewer` | haiku | Read, Write, Edit, Grep, Glob | Read, Grep, Glob, WebSearch, WebFetch, Write, Edit | - | WebSearch, WebFetch | - |
| `market-researcher` | haiku | Read, Write, Edit, Grep, Glob | Read, Grep, Glob, WebSearch, WebFetch, Write, Edit | - | WebSearch, WebFetch | - |
| `tech-scout` | haiku | Read, Write, Edit, Grep, Glob | Read, Grep, Glob, WebSearch, WebFetch, Write, Edit | - | WebSearch, WebFetch | - |
| `user-researcher` | haiku | Read, Write, Edit, Grep, Glob | Read, Grep, Glob, WebSearch, WebFetch, Write, Edit | - | WebSearch, WebFetch | - |
| `code-auditor` | haiku | Read, Grep, Glob, Bash, Edit | Read, Grep, Glob, Write, Bash (sandboxed) | Edit | Write | - |
| `compliance-officer` | haiku | Read, Write, Edit, Grep, Glob | Read, Grep, Glob, Write | Edit | - | - |
| `dlp-scanner` | sonnet | Read, Grep, Glob, Write, Edit | Read, Grep, Glob, Write | Edit | - | Edit:1 |
| `mcp-defender` | sonnet | Read, Grep, Glob, Write, Edit | Read, Grep, Glob, Write | Edit | - | Edit:1 |
| `pen-tester` | haiku | Read, Bash, Write, Edit, Grep, Glob | Read, Grep, Glob, Write, Bash (sandboxed) | Edit | - | - |
| `sbom-slsa` | haiku | Read, Write, Edit, Grep, Bash | Read, Grep, Write, Bash (sandboxed) | Edit | - | - |
| `secrets-vault` | haiku | Read, Write, Edit, Grep, Bash | Read, Grep, Write, Bash (sandboxed) | Edit | - | - |
| `security-lead` | sonnet | Read, Write, Edit, Bash, Grep, Glob, Agent | Read, Grep, Glob, Agent, Write | Edit, Bash | - | - |
| `threat-modeler` | haiku | Read, Write, Edit, Grep, Glob | Read, Grep, Glob, Write | Edit | - | - |
| `mcp-registry-scout` | haiku | Read, Write, Grep, WebFetch, Bash | Read, Grep, Write, WebFetch | Bash | - | - |
| `model-routing-override` | haiku | Read, Write, Edit, Grep, Bash | Read, Grep, Write, Edit | Bash | - | - |
| `sre-lead` | sonnet | Read, Write, Edit, Grep, Glob, Task, Bash | Read, Grep, Glob, Agent, Write, Edit | Bash | - | - |
| `competitive-analyst` | haiku | Read, Write, Edit, Grep, Glob | Read, Grep, Glob, WebSearch, WebFetch, Write, Edit | - | WebSearch, WebFetch | - |
| `market-sizer` | haiku | Read, Write, Edit, Grep, Glob | Read, Grep, Glob, WebSearch, WebFetch, Write, Edit | - | WebSearch, WebFetch | - |
| `trend-scout` | haiku | Read, Write, Edit, Grep, Glob | Read, Grep, Glob, WebSearch, WebFetch, Write, Edit | - | WebSearch, WebFetch | - |
