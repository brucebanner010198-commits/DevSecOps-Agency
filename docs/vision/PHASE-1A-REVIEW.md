# Phase 1a review pack: the enforced contract

Status: **for the Chairman's prompt-diff review.** The changes are committed on the local branch `feat/phase-1a-enforced-contract`, which is not pushed or merged.

## What changes

The single source for each agent's enforced fields is now `agents/role-cards.yaml`. `scripts/role_cards.py write` puts `tools`, `effort` and `maxTurns` into each agent file. `check` fails CI on drift and on rule breaches:
- an orchestrator holding Bash;
- web access together with a shell;
- a CEO holding Edit or Bash;
- an unknown tool;
- a model line that differs from the card.

Model lines are never written, because tier changes are the Chairman's.

The work is split into commits so that each can be reviewed alone:

1. **Removals** (52 agents). Part 14's "remove" items. `Task` is spelled `Agent`; it stays a runtime alias. `TodoWrite` is dropped, because it is not a live tool.
2. **Additions** (11 agents). This is the one place 1a widens reach: WebSearch and WebFetch for the research and strategy specialists on Haiku, plus Grep and Glob for `panel-chair` and Write for `code-auditor`.
3. **Limits** (93 agents). `effort` and `maxTurns` per plan Part 2B, Stage 2. The CEO is left without a limit.
4. **Examples** moved out of the descriptions into the body, word for word.
5. **Sidecar, lint, launcher, CI and tests.**

## Evidence: D3 with the CEO started as an agent, on the new grant

The same prompt as baseline D3 was run with `--agent devsecops-agency:ceo` and the CEO granted only Read, Grep, Glob, Agent and Write. Cost **$6.78** (Opus $2.55, Sonnet $3.90, Haiku $0.34); 33 minutes.

- **The pipeline engaged.** The CEO dispatched 7 chiefs: `cro`, `pm-lead`, `engineering-lead` (design, then build), `security-lead` (threat model, then audit) and `qa-lead`. They dispatched 8 specialists: `tech-scout`, `spec-writer`, `system-architect`, `threat-modeler`, `frontend-dev`, `code-auditor`, `test-runner` and `a11y-auditor`. In baseline D3 the CEO dispatched only `frontend-dev`.
- **Tests:** 114 pass when run independently (`node --test`).
- **The CEO did not edit code.** It wrote the brief, the status, the inbox, the ADRs, the chat log and the retro.
- **Still wrong:**
  - The CEO wrote `red-team/findings.md` itself, which is a self-authored review.
  - The CEO wrote into the plugin's own `LESSONS.md`.
  - Both are outside its Part 14 write scope. Path scopes need Phase 2a hooks.
  - No legal, audit or evaluation chief was convened, yet `legal/`, `audit/` and `eval/` files exist, written by specialists or chiefs.
- **Confounder:** the session still read the user-level `CLAUDE.md`. Its final message quoted the "Projects/<owner>/<repo>" rule.

Removing Edit and Bash from the CEO did not stop it building. It made it delegate.

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
- `pm-lead`: the design search script is now run by `frontend-dev`, through dispatch.
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
