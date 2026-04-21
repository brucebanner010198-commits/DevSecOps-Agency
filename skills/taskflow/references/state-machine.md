# State machine — entry and exit conditions

Reference for each of the six states. If a task is in a state but the invariants don't hold, the CEO treats it as a bug and writes a `board-decision` entry noting the inconsistency.

## queued

**Entry:** CEO has decided to dispatch a Chief for `(council, phase)`, but has not yet written the `dispatch` entry to `chat.jsonl`.

**Invariants:**
- `dispatchedAt == null`
- `sessionRef == null`
- `fixAttempts == 0`
- `gate == null`

**Exits:**
- → `in-progress` when the CEO writes the `dispatch` entry.
- → `cancelled` if the phase is reshuffled before dispatch (rare).

## in-progress

**Entry:** `dispatch` entry written. Chief is working.

**Invariants:**
- `dispatchedAt != null`
- `sessionRef != null`
- `finishedAt == null`
- `gate == null`

**Exits:**
- → `done` if gate is `green` or `yellow`.
- → `needs-decision` if gate is `red` from a non-blocking council.
- → `blocked` if gate is `red` from a blocking council (security, legal).
- → `cancelled` if the CEO kills the task (user change of scope).

## needs-decision

**Entry:** Chief has reported `red` from a non-blocking council, or reported `yellow` with an unresolvable followup, or returned an escalation the CEO needs to choose between.

**Invariants:**
- `gate == "red"` OR (yellow with user-facing choice)
- `fixAttempts < 2`
- `inboxItem == null` (not yet user-parked)

**Exits:**
- → `in-progress` on fix-loop (CEO requests another attempt; `fixAttempts += 1`).
- → `done` on waiver acceptance (CEO writes `waiver` entry; user consent already logged for non-blocking councils; user consent required via `inbox.json` for blocking councils).
- → `blocked` if `fixAttempts == 2` and still red, OR if CEO decides the choice is irreducibly user-only.
- → `cancelled` if CEO kills the task.

**Anti-pattern:** a task that ping-pongs `needs-decision ↔ in-progress` more than twice. That's the fix-loop cap. Stop looping, escalate.

## blocked

**Entry:** Task requires a user decision. `inbox.json` has the item. Work on this task pauses.

**Invariants:**
- `inboxItem != null`
- `finishedAt == null`
- Phase cannot advance while any task is in this state (unless explicitly waived).

**Exits:**
- → `in-progress` when user response resolves the decision and the path forward needs another Chief run.
- → `done` when user response is a waiver or acceptance-as-is (no more Chief work needed).
- → `cancelled` when user aborts the path.

**Side effects on entry:** CEO writes `escalate` entry to `chat.jsonl`, opens `inbox.json` item with options + recommendation, sets `status.json > blockers` to include this item, refreshes command-center.

## done

**Entry:** Terminal success. Gate was accepted (green, yellow-with-followup, or waived-red).

**Invariants:**
- `finishedAt != null`
- `gate in ["green","yellow","red"]` (red only if waived)

**Exits:** None. Terminal.

A `done` task may still have open `followups` in `gates.followups`. Those are addressed in `/devsecops-agency:retro`, not by re-opening this task.

## cancelled

**Entry:** CEO or user killed the task before it produced an accepted artifact. Scope change, project pivoted, duplicate work, etc.

**Invariants:**
- `finishedAt != null`
- `gate == null`

**Exits:** None. Terminal.

## State rendering (command-center)

| State            | Color      | Icon           |
| ---------------- | ---------- | -------------- |
| queued           | slate      | ○              |
| in-progress      | blue       | ◐              |
| needs-decision   | orange     | ⚠              |
| blocked          | red        | ⛔             |
| done (green)     | green      | ●              |
| done (yellow)    | amber      | ●              |
| done (waived red)| amber+ring | ●◯             |
| cancelled        | grey       | ✕              |
