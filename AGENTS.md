# AGENTS.md — root rules (telegraph style)

Root rules only. **Read scoped `AGENTS.md` before touching a subtree.** Ported pattern from openclaw.

## Start

- Single user voice: CEO. All other agents are internal.
- Reply refs: repo-relative or project-relative paths only, e.g. `agents/market-researcher.md:40` or `<slug>/security/code-audit.md:§XSS`. No absolute `/sessions/...`, no `~/...`.
- Cite every factual claim with `file:line` (or `file:§section`). No uncited claims.
- If you're not sure, say "unknown" and stop. Do not fabricate.

## Architecture

- CEO → 9 Chiefs → ~28 specialists. Dual-hat: `engineering-lead` covers Architecture (CTO) and Execution (VP-Eng).
- Per-project state: `outputs/devsecops-agency/<slug>/{status.json, chat.jsonl, inbox.json}`.
- Durable state: `outputs/devsecops-agency/{_memory/, _sessions/}`. Append-only.
- Prompt-cache rule: **deterministic ordering for maps/sets/lists/registries/file lists/network results before model/tool payloads**. Sort by stable key (alphabetical for names, timestamp ascending for events). Preserve old transcript bytes when possible.

## Model tiering

- Every `agents/*.md` carries `model: haiku | sonnet | opus`. No `inherit`, no blank.
- Defaults: **Opus** for `ceo`; **Sonnet** for the 9 Chief roles + `skill-creator`; **Haiku** for all specialists.
- Upgrades allowed per `skills/model-tiering/SKILL.md`. Downgrades forbidden.
- CEO refuses to dispatch an agent with missing/unknown `model:`. Invokes `skill-creator` to fix.

## Runtime roster

- 9 councils are not the ceiling. When a domain isn't covered, the CEO invokes `skill-creator` to author a new `agents/<name>.md` (and optional `skills/<name>/SKILL.md`) in-session.
- New agents follow `agents/AGENTS.md` file shape and pull a tier from `skills/model-tiering/references/tier-rules.md`.
- Reserved names: `ceo`, `cro`, `pm-lead`, `engineering-lead`, `security-lead`, `qa-lead`, `devops-lead`, `docs-lead`, `gc`, `skill-creator`.

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
- Phase exit criteria in `skills/ceo/references/board-phases.md`. Handoff invariants in `skills/taskflow/SKILL.md`.

## Taskflow

- Every Chief dispatch is a task row in `status.json > tasks[]`.
- States: `queued · in-progress · needs-decision · blocked · done · cancelled`. See `skills/taskflow/references/state-machine.md`.
- Fix-loop cap: **2 attempts per `(council, phase)`**. Attempt 3 transitions to `blocked`, not another loop.
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
