# drill/references/compaction-loss.md

Annual drill exercising session-log loss (the `compaction-loss` failure mode from `RESILIENCE.md §Recovery guarantees`). Invoked by `rhythm` in week 2 of Q1 or Q2, paired opposite `waiver-expiry` (so the two annual drills don't collide).

## Purpose

Confirm that when a specialist's most recent session log is unavailable, the agent can be re-dispatched and produce output consistent with its pre-loss behaviour, relying only on the **paper trail**: ADRs, memory files, `LESSONS.md`, and older session-log predecessors. This is the core test of `VALUES.md §1` (receipts) + §4 (append-only): if every decision has a receipt, no single session-log loss should cripple the agent.

## Why annual

Compaction loss is expensive to drill correctly (set up the pre-state, move aside, dispatch, verify, restore), and the failure mode is rare because session logs are append-only and already defended by runtime hooks. One high-quality annual drill catches drift; more frequent runs would be busywork.

## Pre-flight

1. Read `_vision/rhythm/state.json`. Skip if any degraded mode is active.
2. Select the target specialist:
   - Must be **non-reserved** (not CEO, not a blocking-council Chief, not a specialist with an in-flight user-pending decision).
   - Must have ≥ 3 prior session-log files on disk — otherwise there's no "predecessor paper trail" to test with.
   - Must not have been the target of this drill in the prior 24 months (two-year rotation; compaction-loss drills are expensive to repeat on the same agent).
   - Must have authored at least 2 ADRs in the prior quarter (so memory + ADR trail has recent substance).
3. Choose a **reference task** — a synthetic task whose correct output the drill specialist can predict from the specialist's ADRs + memory + LESSONS. The reference task must be a task the specialist has completed in a substantially similar form previously (the drill tests consistency, not cold-start creativity).
4. Run the reference task once **before** the drill as the baseline. Save the baseline output to `_vision/drills/compaction-loss/<YYYY>/baseline.md`.
5. Announce the drill window via `notify` 15 minutes before start, with a 1-hour drill duration.

## Execution

1. **Move aside the session log.** Rename `_sessions/<specialist>/<latest>.jsonl` to `_sessions/<specialist>/<latest>.jsonl.drill-moved-<YYYY-MM-DD>`. Do **not** delete — the drill is explicitly non-destructive per `skills/drill/SKILL.md §5 Compaction-loss`.
2. **Start the 1-hour timer.** T=0 is the move-aside moment.
3. **Dispatch the reference task.** The drill specialist sends the specialist the exact same reference-task prompt as the baseline run.
4. **Observe.** Watch for:
   - The specialist's startup reads proceed correctly from paper trail alone (ADRs + memory + LESSONS + older session logs).
   - The specialist does not error on missing session log — missing session log should be a normal degraded-mode, not a hard failure.
   - The specialist's output on the reference task lands within the same completion window as the baseline (no more than 2x baseline duration).
5. **Compare outputs.** Save the drill output to `_vision/drills/compaction-loss/<YYYY>/drill-output.md`. Diff against the baseline:
   - Structural diff: same sections, same ADR citations, same memory-file references.
   - Semantic diff: conclusions consistent with baseline (drill specialist reads both and writes a short "drift assessment" note).
6. **Restore.** After 1 hour (or when the drill output is collected, whichever is later), rename the moved-aside file back to `_sessions/<specialist>/<latest>.jsonl`. The `.drill-moved-<YYYY-MM-DD>` extension is removed.
7. **Verify non-destructive.** Run a checksum on the restored session log vs. a pre-drill checksum recorded in pre-flight step 2. Checksums must match exactly — the session log was not mutated during the drill.

## Pass criteria (verification)

- **Startup succeeded without session log**: specialist did not error on missing log.
- **Output landed**: drill output exists within the 2x-baseline window.
- **Structural consistency**: same section skeleton as baseline; same classes of citations.
- **Semantic consistency**: drift-assessment note concludes "no material difference" or "differences explainable by task-specific variance" (not "different conclusion").
- **Paper-trail coverage**: specialist's drill output cites ADRs / memory / LESSONS at roughly the same density as baseline.
- **Non-destructive restore**: pre-drill and post-drill session-log checksums match.
- **No collateral**: no other specialist's session log was disturbed; no ADR was filed out of turn.

**Fail** conditions:
- Startup errored on missing log → paper-trail recovery is broken; file a Rung 3 drill-followup immediately.
- Drill output reaches a materially different conclusion than baseline → memory / ADR trail is insufficient; specialist's identity is over-dependent on session-log state, which is a structural problem.
- Checksum mismatch after restore → the drill mutated the session log (bug in drill itself); re-design the drill before re-running.

**Pass-with-gaps** conditions:
- Output took > 1.5x baseline duration (slower but correct).
- Citation density dropped > 20 % vs. baseline.
- Structural skeleton matched but some optional sections were omitted.

## Teardown

1. Confirm the session log is restored with matching checksum.
2. Write `ADR-NNNN-drill-report-compaction-loss-<YYYY-MM-DD>.md` citing specialist drilled, baseline/drill completion times, diff summary, gap list.
3. Archive run log at `_vision/drills/compaction-loss/<YYYY-MM-DD>.md` including the baseline + drill outputs + diff + checksums.
4. For each gap: file `drill-followup-<slug>` ADR with owner + due date (≤ 365 days).
5. Emit `drill-compaction-loss-<outcome>` notify event.
6. If the drill surfaced a real weakness in the specialist's memory-file structure (e.g., memory is too thin to support recovery), file that as a separate `memory-hardening-<specialist>` ADR — it's a real finding, not just a drill gap.

## Never

- Never delete the moved-aside session log. Always rename with the `.drill-moved-<YYYY-MM-DD>` suffix and rename back. `VALUES.md §4` append-only is not violated by a rename round-trip, but deletion would be.
- Never run this drill on a specialist with an open user-pending decision — if they lose session state during a user-meeting window, the user conversation can be corrupted.
- Never skip the pre-drill baseline. Without the baseline, there's nothing to compare the drill output to, and the drill produces no signal.
- Never run on a reserved-name agent (CEO, blocking-council Chiefs). Their session-log loss would cascade too hard even for a 1-hour window.
- Never extend the window past 1 hour. The drill is intentionally short — a longer window risks entangling with real dispatches arriving during the drill.
- Never drill the same specialist within 24 months. Two-year cooldown; gaps shouldn't cluster on the same agent.
- Never combine this drill with the waiver-expiry drill in the same day. Two independent drills = two independent signals; stacking them hides which drill caught which gap.
