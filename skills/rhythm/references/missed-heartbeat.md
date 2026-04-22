# rhythm/references/missed-heartbeat.md

Escalation tree when a heartbeat misses its window. Parsed by `skills/rhythm/SKILL.md` step 6.

## General rule

A heartbeat is **missed** when `today - lastX` exceeds that cadence's window by the escalation threshold:

| Cadence | Normal window | Escalation threshold |
| --- | --- | --- |
| Daily | 1 d | 2 d (1 d late) |
| Weekly | 7 d | 10 d (3 d late) |
| Monthly | 32 d | 35 d (3 d late) |
| Quarterly | 95 d | 100 d (5 d late) |

Being inside the window but not yet run is not a miss — it's just "not yet due today" or "will run on next CEO turn".

## Escalation tree

### First miss (threshold crossed once)

- Run the heartbeat immediately at the next CEO turn; do not skip.
- Append row to `_vision/rhythm/misses.md` with `cadence / window-end / ran-at / catch-up-or-skip-forward`.
- File `compliance-drift` row (**yellow**).
- No ADR yet.

### Second consecutive miss (same cadence)

- Run the heartbeat immediately.
- File ADR `kind: rhythm-miss-2x`, body cites the two missed windows.
- Escalate via `skills/ladder` to **Rung 2** (internal retry with tighter constraint: next heartbeat must run within its window or auto-escalate to Rung 3).
- CAO opens a finding (**medium**).

### Third consecutive miss

- File ADR `kind: rhythm-miss-3x` and escalate to **Rung 3** (blocking-council red).
- For **quarterly** specifically: this blocks all new-project acceptance until the heartbeat lands — the user is notified via `inbox.json` with `kind: quarterly-miss-blocking`.
- For other cadences: CAO red, internal work continues but all new project kick-offs require explicit CEO override-ADR.

### Fourth or more

- Escalate to **Rung 4+** via `skills/ladder`.
- User is notified every turn until caught up.
- Consider `skills/keeper-test` out-of-cycle on the CEO agent itself (CEO is reserved so this is a performance review, not a firing).

## Catch-up vs. skip-forward

When a heartbeat is missed, two modes exist:

**Catch-up.** Run the heartbeat *as if* it fired in its window. The inputs read are still "as of now", but the output file is named with the window's date, not today's. Pick catch-up for daily + weekly (their inputs don't invalidate quickly).

**Skip-forward.** File a placeholder for the missed window with body `skipped — caught up on <YYYY-MM-DD>` and run the current window's heartbeat fully. Pick skip-forward for monthly + quarterly (their inputs depend on "end-of-period snapshots" that cannot be reconstructed after the fact).

In both modes, `_vision/rhythm/misses.md` gets a row with the mode used.

## Degraded vs. missed

These are not the same:

- **Degraded** = the heartbeat *ran* but a required input was unavailable (file missing, malformed JSON, connector down). It does not update `lastX` and does increment `degradedCount`.
- **Missed** = the heartbeat did not run within its escalation window.

Two degraded in a row ≈ one miss, per escalation purposes.

## Never

- Don't backdate `state.json` to make a miss disappear. The invariant is append-only (`VALUES.md §4`).
- Don't delete a row from `_vision/rhythm/misses.md`. Correction is a new row citing the original.
- Don't re-file `compliance-drift` rows on every turn — one per miss, aged out per the compliance-drift skill's own rules.
- Don't escalate to Rung 5+ on rhythm alone. Rung 5 implies scope pivot; rhythm misses fix themselves by running the heartbeat, so the ceiling is Rung 4 (escalate to user awareness) unless something else is also broken.
