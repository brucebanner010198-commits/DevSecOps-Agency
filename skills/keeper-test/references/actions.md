# keeper-test/references/actions.md

The decision tree after `performance-reviewer` returns a rating. Who acts, what ADR fires, what gets updated.

## Rating → action map

```
green   →  Keep          →  no-op + annotate performance file
yellow  →  Upgrade       →  prompt-upgrade via `roster` + `red-team` prompt-diff review + ADR
red     →  Repurpose OR  →  move to different council + ADR  (COO picks)
           Fire             →  inbox.json → user-meeting → archive + ADR (USER-ONLY)
```

## Keep

Zero file edits. One annotation:

- Append to `_vision/roster/performance-<YYYY-MM-DD>.md`:

  ```
  | <agent> | green | gate-hit-rate=<pct>, fix-loop=<pct>, audit=clean, values=clean | no action |
  ```

No ADR. No council roster update. No session-log write beyond the review's `report` entry.

## Upgrade (yellow)

### Preconditions

- Agent is not reserved (not one of the 16 chiefs, not skill-creator).
- This is the agent's first or second consecutive yellow. A third consecutive yellow escalates to red (per `KEEPER-TEST.md > ## Yellow → prompt upgrade`).

### Process

1. **Author the diff.** COO commissions a prompt edit targeting the specific axis that scored yellow (gate hit rate, fix-loop rate, values-citation). Typical changes:
   - Tighten `## Process` with more cited invariants.
   - Add a `## Must` rule that maps to the failing axis.
   - Add one anti-pattern to `## What you never do`.
2. **Run prompt-diff review.** The diff goes through `skills/red-team` + `skills/playbook` prompt-diff review per `VALUES.md §10`. Rejected diffs auto-rollback; reapplication requires a new stepping-stone.
3. **Merge on pass.** Update `agents/<council>/<agent>.md` with the landed diff.
4. **File ADR.** `_decisions/ADR-NNNN-roster-upgrade-<agent>.md`, kind `roster-upgrade`.
5. **Log.** Append to `_vision/roster/history.md` with the upgrade record.
6. **Track for re-review.** Next quarterly review scores this agent preferentially — if the yellow axis moved to green, the upgrade worked.

### Two-strike rule

If two consecutive quarters of yellow → upgrade fail to move the axis to green, **escalate to red** at the next review, even if rating still says yellow.

## Repurpose (red, option 1)

### When to pick repurpose over fire

- Agent's domain is no longer relevant to the current portfolio (e.g. we're no longer building mobile apps, so `mobile-dev` has low utilization).
- Agent performed well in a past window but axis scores dropped due to task-type mismatch.
- COO sees a fit in a different council where strengths apply.

### Process

1. **Propose target council.** COO consults `capacity` skill for under-utilized councils.
2. **Draft the repurposed role.** COO + `skill-creator` co-author the move: new `agents/<new-council>/<agent>.md` file (same name, different council + adjusted Role Card + adjusted Must/Must-not).
3. **File ADR.** `_decisions/ADR-NNNN-roster-repurpose-<agent>.md`, kind `roster-repurpose`. Cites the old council + new council.
4. **Move the file.** `git mv agents/<old-council>/<agent>.md agents/<new-council>/<agent>.md`. **Then** overwrite with the new content via `Write`.
5. **Update council TEAM.md files.** Both old and new `councils/<council>/TEAM.md`.
6. **Update status-schema.** `skills/ship-it/references/status-schema.md > team.<council>.specialists` for both councils.
7. **30-day probation.** Run the new role for 30 days. Mid-cycle review at day 30. If still red after 30 days, escalate to fire.

### Boundary

Repurpose does not change tier. Tier downgrades are forbidden (`VALUES.md §10`).

## Fire (red, option 2)

### Preconditions

- **USER approval required.** COO alone cannot fire. CEO alone cannot fire. See `KEEPER-TEST.md > ## Who runs it`.
- Either:
  - Repurpose was tried and failed (day-30 still red), OR
  - Agent's domain is gone (no repurposable council exists).

### Process

1. **COO drafts proposal.** `inbox.json` entry with kind `fire-proposal`, body cites the performance-<date>.md row + prior upgrade/repurpose ADRs.
2. **CEO escalates.** Next `user-meeting` includes the proposal in the 4-phase flow (brief → present → capture → commit).
3. **User decides.** If user says fire, proceed. If user says repurpose, return to the repurpose flow. If user says keep, the CEO files an ADR `kind: override-keeper-test` citing user rationale.
4. **Archive.** `git mv agents/<council>/<agent>.md _vision/roster/_archive/<agent>.md`.
5. **Add redirect header** to the archived file:

   ```markdown
   # <agent> (archived <YYYY-MM-DD>)

   > Role closed. Original location: `agents/<council>/<agent>.md`.
   > Decision: ADR-NNNN.
   > Last-live content preserved below.
   ```

6. **Update council TEAM.md.** Remove from roster.
7. **Update status-schema.** Remove from `team.<council>.specialists`.
8. **File ADR.** `_decisions/ADR-NNNN-roster-fire-<agent>.md`, kind `roster-fire`. Cites the user-meeting ID that approved.
9. **Log.** `_vision/roster/history.md` + a `note` entry in the archived agent's (final) session log: `"role closed, ADR-NNNN"`.
10. **Notify.** `notify` event `role-closed`.

### What never happens on fire

- `git rm` of the agent file. Forbidden by `VALUES.md §4`.
- Deletion of session logs. Preserved forever — future re-hires read them.
- Deletion of ADRs, stones, or any other paper trail related to the fired agent.

## Override-keeper-test (user says no)

If the user rejects a COO fire proposal and says keep:

- File `_decisions/ADR-NNNN-override-keeper-test-<agent>.md`, kind `override-keeper-test`.
- Body cites user's rationale (quoted from user-meeting minutes).
- Agent stays on roster.
- Next quarterly review runs as normal — override does not exempt the agent from future reviews.

## Summary

| Rating | Who decides | ADR kind | Roster change |
| --- | --- | --- | --- |
| green | COO | none | none |
| yellow | COO | roster-upgrade | prompt edit, no tier change |
| red → repurpose | COO | roster-repurpose | move council, no tier change |
| red → fire | **USER** | roster-fire | archive (no deletion) |
| red → user keeps | USER | override-keeper-test | none |
