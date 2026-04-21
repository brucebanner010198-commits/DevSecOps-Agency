---
name: ladder
description: This skill should be used when a task hits the 2-attempt fix-loop cap (per `skills/taskflow/references/fix-loop.md`), when a blocking-council red surfaces with no obvious waiver path, or whenever the user's standing rule "always find a way to get the result as long as the solution is achievable with technology present" applies. Trigger phrases include "never give up", "climb the ladder", "escalate the ladder", "stuck — next rung", "can we solve this differently", "we're blocked — options", "try harder", "we need this". The never-give-up ladder defines 8 rungs of progressively-more-aggressive remediation. Each rung transition files an ADR.
metadata:
  version: 0.3.0-alpha.4
---

# ladder — the never-give-up resilience ladder

The ladder is the agency's answer to "we're stuck". Instead of dying at the 2-attempt fix-loop cap, a blocked task climbs rungs until it reaches a terminal outcome: shipped, superseded, or documented-defer. Giving up is a terminal rung, not a default.

**Standing user rule:** "Always find a way to get the result as long as the solution is achievable with technology present." The ladder exists to operationalise that rule without the agency burning unbounded tokens.

## The 8 rungs

```
Rung 0  — Retry with refreshed context
Rung 1  — Fix-loop (existing 2-attempt cap)
Rung 2  — Alternate approach within scope
Rung 3  — Cross-council escalation
Rung 4  — Hire / repurpose a specialist (COO)
Rung 5  — Scope pivot (same mission, different path)
Rung 6  — User consult (irreducible)
Rung 7  — Parking lot (documented defer)
```

Each rung:
- Has **entry criteria** (why climb to it) in `references/rung-rules.md`.
- Has a **max attempt budget** (how many tries before the next rung).
- Emits a **rung-transition ADR** per `skills/adr/references/decision-triggers.md > Process`.
- Increments a `ladderRung` counter on the blocked task (stored in `status.json > tasks[].ladderRung`).

## When to trigger

- `taskflow` transitions a task to `blocked` for any reason except `cancelled`.
- Blocking-council (security / legal) red with no clean waiver path.
- Fix-loop attempt 3 would have been needed (per existing cap).
- User asks "can we get this done another way".
- A task has been `blocked` for > 48 hours with no progress.

## Process

1. **CEO identifies the blocked task** and reads `references/ladder-matrix.md` to find the starting rung.
2. **CEO dispatches the rung owner.** Rung 0-2 are owned by the Chief whose task is stuck. Rung 3 is cross-council (another Chief). Rung 4 is COO. Rung 5 is CPO + user-meeting. Rung 6 is the user. Rung 7 is CEO documentation.
3. **Attempt the rung.** Per-rung budget in `references/rung-rules.md`. If still blocked at budget exhausted, climb one rung.
4. **File an ADR per transition.** Each rung move is an ADR: `ADR-NNNN-ladder-<slug>-rung-<from>-to-<to>`.
5. **Terminal outcome** at Rung 7 (parking lot) with a reconsider-trigger written so the task can resurrect when conditions change. Parking-lot tasks are not failures; they're preserved optionality.

## Invariants

- **No rung skipping upward** without an ADR explicitly justifying the skip (e.g., obvious Rung 6 because it requires user credentials). Skipping downward ("we tried Rung 5 and are now retrying Rung 1") is allowed with an ADR.
- **Each rung attempts ≤ its budget** in `references/rung-rules.md`. Cannot loop within a single rung beyond budget.
- **Every rung transition files an ADR** in the same CEO turn. "Informally climbed" = never.
- **Rung 6 (user consult) is not unlimited.** User response timeout of 7 days auto-advances to Rung 7 parking.
- **Rung 7 (parking lot) preserves the work** — all artifacts, all session logs, all partial code stays. Parking is resumable.
- See `references/rung-rules.md` for per-rung owners, budgets, entry criteria, and exit signals.
- See `references/ladder-matrix.md` for the routing table (task state × blocker kind → starting rung).

## Integration with existing skills

- **`taskflow`** (v0.2.3) — the 2-attempt fix-loop cap becomes "Rung 1 budget exhausted → climb to Rung 2". Task stays in `blocked` state; `ladderRung` tracks the climb position.
- **`gates`** — blocking-council reds don't mean ship-blocked forever. They mean "start the ladder". Only after Rung 6+ does ship-blocked become durable.
- **`adr`** — every rung transition files an ADR. See extended triggers in `skills/adr/references/decision-triggers.md > Process`.
- **`roster`** — Rung 4 dispatches through COO + `hiring-lead`. New specialist hires are the standard Rung 4 action.
- **`meeting-minutes`** — Rung 6 user-consult writes minutes (`kind: user`).

## Metrics to log

Written to `status.json > metrics`:

- `ladderClimbs: { started, resolved_at_rung_N, parked }` — per-project rollup.
- `rungAttempts: { rung_N: count }` — to surface "always-hits-rung-4" patterns for portfolio audit.
- `ladderMeanTime`: median time-in-state per rung.

Portfolio audit (Wave 3 `cao`) reviews these metrics to flag:

- Agency-wide pattern of always parking at Rung 7 → process failure, ADR required.
- Agency-wide pattern of Rung 4 hires → consider roster expansion vs prompt-upgrade audit.
- Tasks that climbed > 2 rungs and still shipped → reusable playbook — promote to `_memory/patterns/<slug>-unblock-playbook.md`.

## What this skill is not

- Not a way to override blocking-council decisions. Security / legal reds still require user waiver at Rung 6. Ladder rungs 0-5 don't waive; they find alternate paths.
- Not a retry-forever loop. Budget per rung is capped. Rung 7 is a real terminal state.
- Not a replacement for fix-loop. Fix-loop is Rung 1; ladder is what happens after.
- Not automatic. Each rung transition is CEO-authored and ADR-backed.
