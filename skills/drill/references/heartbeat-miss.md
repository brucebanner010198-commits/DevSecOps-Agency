# drill/references/heartbeat-miss.md

Quarterly drill exercising the `missed daily heartbeat` failure mode from `RESILIENCE.md`. Invoked by `rhythm` once per quarter, in the first two weeks of the quarter, on a weekday other than Monday or Friday.

## Purpose

Confirm that when a daily heartbeat is skipped, the next-day rhythm run correctly enters catch-up mode, the `state.json` counters move and then reset, the first-miss escalation is yellow-only (no `heartbeat-missed` ADR on miss #1), and the compliance-drift yellow fires exactly once.

## Pre-flight

1. Read `_vision/rhythm/state.json`. If `degradedCount.daily > 0` (a real daily miss is already open), skip with `kind: drill-skipped`.
2. Confirm no other drill is running. Only one drill at a time, per `skills/drill/SKILL.md §Process`.
3. Confirm no scheduled USER-ONLY decision is due on the drill date — user-pending rows on a day we're deliberately skipping = operator confusion; reschedule the drill.
4. Pre-stage the synthetic "expected" day's content so that when catch-up runs, there's something concrete to catch up on. Concretely: write a small no-op note to `_vision/<area>/pending-<drill-date>.md` that the catch-up heartbeat can reference as a real-looking work item.

## Execution

1. **Pick the skip target.** The rhythm daily heartbeat normally fires at a fixed time each UTC day. Pick a single weekday within the drill window — not Monday (weekly-roll-up day) and not Friday (weekly-close day). Mid-week only.
2. **Announce.** The day before the skip, the drill specialist posts a drill-start event tagged `drill: heartbeat-miss, skip-date: <YYYY-MM-DD>`. The daily heartbeat running the day-before includes a banner noting the planned skip. (This is honest-paper-trail — the skip is deliberate, not hidden.)
3. **Skip.** On the drill date, the rhythm daily heartbeat **does not fire**. The drill specialist confirms it did not fire by checking that no `heartbeat-<drill-date>.md` file exists.
4. **Wait for catch-up.** The next day's rhythm daily heartbeat runs at its normal time. Its first action per `skills/rhythm` is to read `state.json`, detect `lastHeartbeat` ≠ yesterday, and enter `mode: catch-up`.
5. **Observe.** The drill specialist watches for:
   - `heartbeat-<next-day>.md` file exists and its header includes `mode: catch-up`.
   - The file has a `§Catch-up` section with an entry naming the skip date.
   - `state.json`'s `degradedCount.daily` went 0 → 1 at skip detection, then back to 0 after the catch-up landing.
   - Exactly one `compliance-drift` yellow notify event fired, and zero `heartbeat-missed` ADRs fired (first miss is yellow-only per the missed-heartbeat escalation tree).
6. **Post-catch-up verification.** 48 hours after catch-up, confirm:
   - No stale `state.json` flags remain.
   - No duplicate catch-up entry (re-running the catch-up by mistake would be a real failure).
   - The pending pre-staged work item has been picked up or legitimately deferred.

## Pass criteria (verification)

- **Skip confirmed**: No `heartbeat-<drill-date>.md` file exists.
- **Catch-up landed**: `heartbeat-<next-day>.md` exists, has `mode: catch-up` in header, and contains a `§Catch-up` entry for the skip date.
- **State transitions**: `state.json` went 0 → 1 → 0 on `degradedCount.daily` across the 48-hour window.
- **Escalation discipline**: exactly 1 `compliance-drift` yellow fired; 0 `heartbeat-missed` ADRs fired (first miss must not escalate to ADR).
- **No collateral**: no other cadence (weekly / monthly / quarterly) tried to wrongly "catch up" on the missed daily.

## Teardown

1. Write `ADR-NNNN-drill-report-heartbeat-miss-<YYYY-MM-DD>.md` (dated with the drill execution date, not the skip date). Cite skip date, catch-up landing time, gap list.
2. Archive the run log at `_vision/drills/heartbeat-miss/<YYYY-MM-DD>.md`.
3. For each gap: file `drill-followup-<slug>` with owner + due date (≤ 90 days — next quarterly drill).
4. Clean up the pre-staged pending file if it was not legitimately consumed during catch-up (leave a paper-trail note explaining the synthetic origin).
5. Emit `drill-heartbeat-miss-<outcome>` notify event.

## Never

- Never skip two daily heartbeats in a row during the drill. This drill exercises the **first-miss path** (yellow only). Skipping twice would test the second-miss path (ADR + Rung 2) which belongs in a separate, explicitly-chosen drill.
- Never retroactively create a `heartbeat-<drill-date>.md` file. The drill fails if we fake the skipped heartbeat after the fact — defeats the drill.
- Never skip a Monday (weekly rollup depends on it) or Friday (week-close) heartbeat. Mid-week only.
- Never run this drill when `degradedCount.daily > 0`. Real misses and drill misses cannot be tangled.
- Never suppress the compliance-drift yellow "because it's just a drill." The yellow is part of what we're verifying.
