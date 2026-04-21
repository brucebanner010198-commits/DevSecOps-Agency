---
name: taskflow
description: >
  Internal skill. Defines the task state machine the CEO uses to track every
  unit of work the board has dispatched: state transitions, fix-loop caps,
  handoff invariants, dependency rules, and the `tasks[]` array in status.json.
  Invoked by the CEO on every dispatch, report, fix-loop, and escalation. Not a
  user-facing skill.
metadata:
  version: "0.2.3"
---

# taskflow — how work moves through the agency

A task is the smallest unit the CEO tracks. Every Chief dispatch creates one. Every Chief report closes or transitions one. This skill defines the states and the legal transitions between them.

Before this skill, task state lived implicitly in `chat.jsonl` (you reconstruct it by replaying events). After this skill, `status.json > tasks[]` is the materialised view — cheap to read, deterministic, source-of-truth for the command-center.

## The six states

```
               ┌─────────┐
               │ queued  │ ← CEO decided to dispatch, not yet sent
               └────┬────┘
                    │ dispatch
                    ▼
               ┌─────────────┐
               │ in-progress │ ← Chief working
               └─┬─────┬─────┘
        escalate │     │ report
                 │     ▼
                 │  ┌───────────────┐
                 │  │ needs-decision │ ← gate=red or gate=yellow-waivable
                 │  └──┬──────┬──────┘
                 │     │      │
                 │     │      │ fix-loop (≤ 2 attempts)
                 │     │      ▼
                 │     │  ┌─────────────┐
                 │     │  │ in-progress │
                 │     │  └─────────────┘
                 │     │
                 │     │ accept / waive
                 │     ▼
                 │  ┌──────┐
                 │  │ done │ (terminal)
                 │  └──────┘
                 ▼
              ┌─────────┐
              │ blocked │ ← user decision needed, parked in inbox.json
              └────┬────┘
                   │ user-response
                   ▼
              ┌─────────────┐
              │ in-progress │ or done
              └─────────────┘

              ┌───────────┐
              │ cancelled │ ← CEO or user killed it (terminal)
              └───────────┘
```

All six: `queued`, `in-progress`, `needs-decision`, `blocked`, `done`, `cancelled`.

## Task shape

Lives in `status.json > tasks[]`, append-then-update (never delete):

```json
{
  "id": "t-0007",
  "council": "security",
  "chief": "security-lead",
  "phase": "design",
  "kind": "chief-dispatch",
  "state": "in-progress",
  "createdAt": "<iso>",
  "updatedAt": "<iso>",
  "dispatchedAt": "<iso>",
  "finishedAt": null,
  "sessionRef": "_sessions/security-lead/77c19abf5d03.jsonl",
  "fixAttempts": 0,
  "gate": null,
  "artifacts": [],
  "inboxItem": null,
  "note": "STRIDE threat model on architecture v1"
}
```

Field notes:
- `id` is monotonic `t-NNNN`, zero-padded.
- `kind` ∈ `chief-dispatch | fix-loop | escalation-response | waiver-check`.
- `state` ∈ the six states above.
- `fixAttempts` caps at 2. On attempt 3 the task transitions to `blocked` (not another fix-loop).
- `sessionRef` is the `_sessions/...` file where detail lives; don't duplicate it here.
- `inboxItem` is set when state transitions to `blocked`, clears on resume.

## Legal transitions

```
queued          → in-progress | cancelled
in-progress     → needs-decision | blocked | cancelled
needs-decision  → in-progress (fix-loop) | done | blocked | cancelled
blocked         → in-progress | cancelled
done            → (terminal)
cancelled       → (terminal)
```

Any other transition is a bug. The CEO bounces it.

## Transition triggers

| Trigger                                   | From            | To              | Side effect                                      |
| ----------------------------------------- | --------------- | --------------- | ------------------------------------------------ |
| CEO decides to dispatch Chief             | (new)           | `queued`        | append task row                                  |
| CEO emits `dispatch` to chat.jsonl        | `queued`        | `in-progress`   | `dispatchedAt = now`                             |
| Chief reports `gate: green`               | `in-progress`   | `done`          | `finishedAt = now`, increment `completed`        |
| Chief reports `gate: yellow` (with followups) | `in-progress` | `done`          | merge followups into `gates.followups`           |
| Chief reports `gate: red` (non-blocking)  | `in-progress`   | `needs-decision`| CEO decides: waive or fix-loop                   |
| Chief reports `gate: red` (blocking)      | `in-progress`   | `blocked`       | open inbox item, park                            |
| CEO issues fix-loop (attempt ≤ 2)         | `needs-decision`| `in-progress`   | `fixAttempts += 1`, new dispatch entry           |
| CEO accepts waiver                        | `needs-decision`| `done`          | write `waiver` entry to chat.jsonl               |
| Fix attempts reach 3                      | `needs-decision`| `blocked`       | open inbox, park                                 |
| User responds to inbox                    | `blocked`       | `in-progress` OR `done` OR `cancelled` | consume inbox item           |
| CEO kills the task                        | any non-terminal| `cancelled`     | write `board-decision` entry                     |

## Fix-loop cap

Per `(council, phase)` pair, the CEO dispatches a Chief at most **three times total**: the initial dispatch + 2 fix-loops. On attempt 3, the task is `blocked` and goes to the user with:

- What the Chief got right (1 bullet).
- What's still red (1 bullet).
- Three options: `fix-path-A`, `fix-path-B`, `ship-with-waiver`.
- CEO's recommendation.

`metrics.fixLoops` counts only the `in-progress → needs-decision → in-progress` round-trips. An initial dispatch is attempt 0.

## Handoff invariants

A handoff from phase N to phase N+1 is legal only when:

1. All tasks for phase N are `done` or `cancelled`.
2. No task for phase N is in `needs-decision` or `blocked` without a waiver.
3. `status.json > gates.byPhase[N]` is set to `green` or `yellow`.
4. If any `blocking-council` red was waived, `gates.waivers` has the entry and the user-consent `inboxItem` is closed.

If any invariant fails, the CEO refuses to advance the phase and emits a `board-decision` entry explaining which invariant tripped.

## Dependency rules

Some tasks cannot start until others complete:

| Phase N+1 task    | Requires phase N task(s) done                     |
| ----------------- | ------------------------------------------------- |
| Design (CTO)      | Discovery (CRO, CPO) both `done`                  |
| Design review (CISO) | Design (CTO) `done` with `gate in [green, yellow]` |
| Build (VP-Eng)    | Design (CTO) AND Design review (CISO) both `done` |
| Verify (CQO)      | Build (VP-Eng) `done`                             |
| Verify² (CISO)    | Build (VP-Eng) `done`                             |
| Ship (VP-Ops)     | Verify (CQO) AND Verify² (CISO) both `done`       |
| Docs (CKO)        | Ship (VP-Ops) `done`                              |
| Legal (GC)        | Build (VP-Eng) `done` (can run parallel to Docs)  |
| Close (CEO)       | All above `done`                                  |

Encoded in the CEO's playbook; the taskflow skill just checks that the state transition is legal when the dispatch is attempted.

## Command-center view

The command-center reads `status.json > tasks[]` and renders:

- A Kanban strip: `queued | in-progress | needs-decision | blocked | done | cancelled`.
- Per-Chief lane showing `fixAttempts` badges.
- A red dot next to any `blocked` task with a pointer to the `inboxItem`.

See `skills/command-center/references/panel-spec.md` for the rendering contract.

## Invocation points (for the CEO)

- On decision-to-dispatch → create task with `state: "queued"`.
- On `dispatch` entry written → transition to `in-progress`.
- On Chief report → call `gates` skill first, then transition per the matrix above.
- On fix-loop → check `fixAttempts < 2`, increment, transition back to `in-progress`. Else go `blocked`.
- On phase advance → run the handoff invariants check.

## Progressive disclosure

- `references/state-machine.md` — the six states with entry/exit conditions in detail.
- `references/fix-loop.md` — the 2-attempt cap, the escalation template, and the anti-pattern list.
