---
name: keeper-test
description: >
  This skill should be used when the COO needs to run the quarterly (or
  on-demand) performance review of the agency's roster using the "would we
  re-hire this agent today" criterion. Wraps `roster` and `performance-reviewer`
  into a single invocation and cites `KEEPER-TEST.md`. Trigger phrases:
  "run the Keeper Test", "quarterly performance review", "rate the roster",
  "would we keep <agent>", "time for a roster checkpoint", or any
  `/devsecops-agency:retro portfolio` that includes a roster axis. Also
  triggered by three consecutive red-team prompt-diff bouncebacks on the same
  agent (see `KEEPER-TEST.md > ## Cadence`).
metadata:
  version: "0.1.0"
---

# keeper-test — the fire-readily review

Read [`KEEPER-TEST.md`](../../KEEPER-TEST.md) before invoking. This skill is the machine-readable wrapper; the values doc is the authority.

## When to trigger

- **Quarterly** — on the quarter roll-up tick. Mandatory.
- **On CAO close-audit finding** — if CAO names a specific agent in the finding, run a mid-quarter mini-test for that agent only.
- **On three consecutive prompt-diff bouncebacks** — automatic. `red-team` raises the event; COO runs the test.
- **On user request** — via `user-meeting`, user can request a mid-quarter review of any specific agent.

## Inputs

Per `KEEPER-TEST.md > ## Inputs to the review`:

1. Agent session logs — `_sessions/<agent>/*.jsonl` in the review window.
2. Gate outcomes — `chat.jsonl` entries across all projects in the window.
3. Fix-loop attempts — `status.json > tasks[]` filtered by agent owner.
4. Audit findings — `_vision/audit/*.md` where the agent was cited.
5. Red-team findings — `_vision/playbooks/stones/*.md` where the agent was upstream.
6. Minutes — `_meetings/*.md` escalations involving the agent.

## Review window

| Trigger | Window |
| --- | --- |
| quarterly | last 90 days (same as quarter) |
| CAO finding | last 30 days |
| prompt-diff bouncebacks | last 30 days |
| user-requested | user chooses, default 30 days |

## Process

1. **Check trigger.** Confirm one of the 4 triggers fired. Log the trigger in the session log.
2. **Enumerate roster.** Read `_vision/roster/roster.md` (maintained by `roster-manager`) — or `status.json > team` if roster.md is empty. **Skip reserved names** per `KEEPER-TEST.md > ## Reserved agents` (16 chiefs + skill-creator).
3. **Dispatch `performance-reviewer`.** One dispatch per agent under review. Each returns a green / yellow / red per the 4 axes in `KEEPER-TEST.md > ## Scoring axes`.
4. **Aggregate.** Write `_vision/roster/performance-<YYYY-MM-DD>.md` with one row per agent: overall rating + per-axis.
5. **Hand off to `hiring-lead`.** The Keep / Upgrade / Fire-or-Repurpose actions get concrete proposals from `hiring-lead`.
6. **For every proposed action, the COO:**
   - **Keep:** no-op. Annotate performance file.
   - **Upgrade:** invoke `roster.prompt-upgrade` — commission the prompt-diff edit, run through `red-team` prompt-diff review, file ADR.
   - **Repurpose:** invoke `roster.repurpose` — move agent to different council, file ADR, update `councils/<council>/TEAM.md` + status-schema.
   - **Fire:** COO writes the proposal to `inbox.json`. CEO escalates to user via `user-meeting` — **fires require user approval per `KEEPER-TEST.md > ## Who runs it`**.
7. **File ADRs.** Every non-Keep action files an ADR via `skills/adr/SKILL.md`.
8. **Write minutes.** Via `meeting-minutes` kind `board` (if CEO attended) or `council` (people-ops alone).
9. **Notify.** If any Fire lands, `notify` event `role-closed`.

## Output

- `_vision/roster/performance-<YYYY-MM-DD>.md` — the performance table.
- `_decisions/ADR-NNNN-roster-<action>-<agent>.md` — one per non-Keep action.
- `_meetings/keeper-test-<YYYY-MM-DD>.md` — the review minutes.
- `_vision/roster/_archive/<agent>.md` — for fired agents, an archive copy of the last-live agent file, with a `## Redirect` header.

## Skill index entry

```
| `keeper-test` (v0.3.8) | Quarterly + on-demand performance review using the fire-readily criterion. Cites KEEPER-TEST.md. |
```

## Integration with `roster` and `performance-reviewer`

This skill is the **invocation wrapper** around the performance-review pipeline. The division of labour:

- `keeper-test` — when to run, what inputs, what to do with the output.
- `roster` — the hire / fire / repurpose / tier-change lifecycle (unchanged by v0.3.8).
- `performance-reviewer` — the agent that produces per-agent scores.
- `hiring-lead` — the agent that proposes concrete actions.

No new agents in v0.3.8. The wrapper is in the skill layer only.

## Anti-patterns

- **Don't run the test on reserved names** (16 chiefs + skill-creator). Firing a chief triggers council restructure — different flow.
- **Don't fire on a single red axis.** Red on one axis triggers fire-or-repurpose proposal; the COO picks one. Both options file an ADR.
- **Don't skip the user escalation on fires.** User has final vote. Violating this is a VALUES §1 red.
- **Don't `git rm` the agent file on fire.** Archive to `_vision/roster/_archive/` with a redirect. `VALUES.md §4` (append-only).
- **Don't run the test without evidence.** Every axis needs a citation. An unscored axis aborts the review.
- **Don't retest the same agent > 2 times in a quarter.** Noise. Mid-quarter retests are for CAO / prompt-diff / user triggers only.
- **Don't let a performance-reviewer rate an agent whose project they helped deliver.** Independence invariant — `VALUES.md §3`.

## Progressive disclosure

- `references/axes.md` — the 4 scoring axes with exact green / yellow / red thresholds (mirrors `KEEPER-TEST.md > ## Scoring axes` with examples).
- `references/actions.md` — the Keep / Upgrade / Repurpose / Fire decision tree.
- `references/bootstrap.md` — first-quarter rules when the review window has < 30 days of data.
