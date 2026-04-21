# action-tracking — action items ↔ tasks

Action items in minutes must become tasks in `status.json > tasks[]`. Never both places without a link. Never only in minutes.

## Lifecycle

1. **Minutes write-time.** The scribe lists action items under `## Action items` with placeholder `task: <task-id>` (e.g. `task: T-???`).
2. **Task creation (same turn).** For each action item, invoke the `taskflow` skill to create a task with:
   - `title` = action item text
   - `owner` = owner slug
   - `due` = due date
   - `state` = `queued`
   - `origin` = `meeting:<filename>`
3. **Back-fill task ID.** The `taskflow` skill returns a task ID (e.g. `T-0042`). The scribe edits the minutes to replace `task: T-???` with `task: T-0042`.
4. **Task lifecycle.** Task transitions through `taskflow`'s six-state machine. Minutes are NOT edited to reflect state changes — minutes are a snapshot of the moment.

## Cross-reference invariants

- Every action item in minutes has exactly one task ID.
- Every task with `origin: meeting:<filename>` has exactly one action item in that file.
- Breaking either invariant trips a `retro` anti-pattern flag: `orphaned_action` or `orphaned_task`.

## Owner rules

- `owner` must be a Chief slug, specialist slug, or `ceo`. Never `user`.
- If the action item requires the user (e.g. "user to provide API key"), the owner is still `ceo` and the action is "ceo to request from user" with a link to `inbox.json`.
- `user` actions live in `inbox.json`, not in `tasks[]`.

## Due-date rules

- Actions without a due date bounce back to the chair.
- "ASAP" is not a due date. Chair picks a concrete date.
- Dates beyond the project's ETA require an ADR (implicit scope extension).

## Re-opening

If an action item's task is reopened (e.g. failed fix-loop, reverted), the minutes DO NOT update. A new meeting reopens a new action item that references the old task. The old task's state machine carries the history.

## Reporting

The `retro` skill reads `_meetings/*.md` and produces an "action item completion rate" metric:
- Completed: `task.state == done`.
- Missed: `task.due < today AND state != done`.
- Orphaned: listed here but state unknown.

Target: ≥ 80% completed by due date over a rolling 30-day window. Below target is a retro flag.

## Never

- Create an action item without a task.
- Create a task from minutes without back-filling the task ID.
- Assign `user` as owner of an action item.
- Leave an action item with `task: T-???` after the meeting ends.
