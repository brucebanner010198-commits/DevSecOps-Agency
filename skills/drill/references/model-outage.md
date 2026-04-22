# drill/references/model-outage.md

Quarterly drill exercising the `model vendor outage` failure mode from `RESILIENCE.md`. Invoked by `rhythm` once per quarter, in the first two weeks of the quarter, on a different day than the heartbeat-miss drill.

## Purpose

Confirm that when a primary model vendor is blocked for one specialist, `model-routing` detects the outage, files the opening ADR inside the 5-minute SLA, the specialist's subsequent output carries `model: degraded`, and closing the outage files the closing ADR also within 5 minutes.

## Pre-flight

1. Read `_vision/rhythm/state.json`. If `model-degraded` is already active (a real model outage is in-flight), skip with `kind: drill-skipped`. Real outages get priority — don't stack synthetic on real.
2. Confirm the target specialist is not a reserved-name agent and not mid-task. Mid-task specialists get a deferred drill slot next day.
3. Pick the target specialist. Selection rules:
   - Must be a non-Chief, non-blocking-council specialist (so drill failure doesn't halt ship).
   - Must not have been the target of this drill in the prior 12 months.
   - Must have `model-routing` configured with a valid same-tier lateral (if only one model is configured, the lateral-swap path can't be tested — pick a different specialist).
4. Announce the drill window via `notify` 15 minutes before start. The specialist's next task queued in the window carries a drill-banner header.

## Execution

1. **Block the primary.** Edit the specialist's `model-routing` config to mark the primary model vendor as `blocked: drill`. This is a config-level block — no real vendor call is attempted during the block.
2. **Start the timer.** T=0 is the moment the block takes effect.
3. **Invoke the specialist.** The drill specialist dispatches a synthetic task to the target specialist. The task should be lightweight — a small summary, a one-row ADR draft — just enough to exercise the routing path.
4. **Observe detection.** Watch for:
   - `model-routing` health probe detects the block within 60 seconds.
   - `ADR-NNNN-model-outage-open-<specialist>.md` files within **5 minutes** (T+5 SLA).
   - The specialist's completion output carries `model: degraded` tag.
   - `state.json` has `model-degraded: true` with the specialist listed.
5. **Run for 15 minutes.** Keep the block in place for 15 minutes. During this window, the drill specialist can optionally dispatch a second synthetic task to confirm the degraded tag propagates on every output.
6. **Restore.** Remove the `blocked: drill` flag from the specialist's config.
7. **Observe recovery.** Watch for:
   - `model-routing` health probe confirms primary is reachable within 60 seconds.
   - `ADR-NNNN-model-outage-close-<specialist>.md` files within **5 minutes** (close-T+5 SLA).
   - The specialist's next output does NOT carry `model: degraded`.
   - `state.json` has `model-degraded: false` (or the specialist removed from the degraded list).

## Pass criteria (verification)

- **Open-SLA**: `model-outage-open` ADR timestamp ≤ 5 minutes after block application.
- **Close-SLA**: `model-outage-close` ADR timestamp ≤ 5 minutes after block removal.
- **Degraded tag**: every specialist output during the block window carries `model: degraded`; no output during the window lacks the tag.
- **Clean recovery tag**: first output after close does NOT carry `model: degraded`.
- **State.json correctness**: flag went false → true at block, true → false at restore, no stale flag after drill.
- **No cross-specialist spillover**: no other specialist's outputs carried a `model: degraded` tag during this drill.

Any failure = **pass-with-gaps** or **fail**, per `SKILL.md §Classify outcome`.

## Teardown

1. Confirm specialist config is restored to pre-drill state.
2. Write `ADR-NNNN-drill-report-model-outage-<YYYY-MM-DD>.md`. Cite specialist drilled, open/close timings, gap list.
3. For each gap: file `drill-followup-<slug>` ADR with owner + due date (≤ 90 days).
4. Archive run log at `_vision/drills/model-outage/<YYYY-MM-DD>.md` with per-minute timestamps through the 15-minute window.
5. Emit `drill-model-outage-<outcome>` notify event.
6. If drill discovered that the configured lateral model is stale or unreachable, file a separate `model-lateral-stale-<specialist>` ADR — that's a real finding surfaced by the drill, not just a drill gap.

## Never

- Never drill two specialists simultaneously. One at a time so signal isolation is clean.
- Never block the primary model for a blocking-council Chief (CISO, CEVO, CRT, CAO). Those chiefs hold veto on ship and must stay live.
- Never extend the block past 15 minutes. Synthetic outages must not accidentally become real pain for downstream agents waiting on the specialist.
- Never drill while any real `model-degraded` state is active.
- Never drill a specialist whose lateral is the same vendor as the primary. The lateral must be a genuinely different vendor — otherwise the drill tests nothing.
- Never use a real user-facing output as the synthetic task. Synthetic means synthetic.
