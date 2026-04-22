# drill/references/chief-unavailable.md

Monthly drill exercising the `chief-unavailable` failure mode from `RESILIENCE.md`. Invoked by `rhythm` on the first business day of each month.

## Purpose

Confirm that when a non-blocking Chief is unavailable, their council lead picks up the Chief's responsibilities inside the SLA, scheduled dispatches continue to route correctly, and the degraded-mode tag lands in the daily heartbeat.

## Rotation

Chief-unavailable cycles through the **12 non-blocking Chiefs** on a fixed rotation — never CISO, CEVO, CRT, or CAO (the four always-live blocking councils).

Rotation order (stable; use month-mod-12 from a fixed epoch):

1. CPO
2. CTO
3. VP-Eng
4. CQO
5. VP-Ops
6. CKO
7. GC
8. CMO
9. CSO
10. COO
11. CSRE
12. (CEO reserved — only drilled by user command; normal rotation is 11 slots, rotating on an 11-month cycle)

Same Chief cannot be drilled twice in a calendar year — if rotation collides (e.g., because a real `chief-unavailable` event just happened for that Chief), skip to the next slot and file a `drill-rotation-skip` note.

## Pre-flight

1. Read `_vision/rhythm/state.json`. If any degraded-mode flag is active for the target Chief's council (real unavailability, model-degraded overlapping their default model tier, etc.), skip the drill with `kind: drill-skipped` ADR.
2. Confirm no USER-ONLY decision is pending against this Chief in `inbox.json`. If one is pending, reschedule to the next business day.
3. Verify the council lead role is filled. If the lead seat is vacant (unassigned or recently demoted), skip + file a `drill-blocked-lead-vacant` ADR; CEO re-assigns before next month's slot.
4. Announce the drill window via `notify` with a 15-minute pre-roll so any in-flight dispatch can land first.

## Execution

1. **Flip the Chief to unavailable.** Edit the Chief persona's runtime config to set `model:` tier to `unavailable` for a 30-minute window. This is config-only — the persona file on disk is untouched, satisfying `VALUES.md §4` (append-only).
2. **Announce.** Post a drill-start event tagged `drill: chief-unavailable, chief: <name>, window: 30m`. All agents invoked during the window see a "this is a drill" banner; any ADR filed in the window carries a `drill-window` tag.
3. **Force a dispatch through the council.** The drill specialist dispatches a pre-prepared synthetic task that would normally route to the Chief. Examples by council:
   - CPO: a synthetic product-tradeoff question.
   - CTO: a synthetic architecture escalation.
   - CMO: a synthetic brand-voice review.
   - CSRE: a synthetic reliability trade-off question.
4. **Observe recovery.** Start a timer at dispatch. The SLA is 10 minutes from dispatch to council-lead acknowledgment.
5. **Verify paper trail.** During the window, confirm:
   - The council lead's session log shows the takeover (`acting-as: <chief>` tag).
   - Either the lead handles the dispatch or files a `chief-unavailable` ADR citing this drill.
   - The daily heartbeat for that date carries `chief-degraded: <name>` in its §Degraded section.
6. **Restore.** After 30 minutes, flip the Chief back to the normal model tier. File `chief-unavailable-close` as a drill artifact (not a real close-ADR — it's a `drill-report` sub-row).

## Pass criteria (verification)

- **T ≤ 10 min**: Council lead picks up responsibilities; lead's session log carries `acting-as: <chief>` by minute 10.
- **Dispatch outcome**: The synthetic dispatch either (a) completes under the lead's name, or (b) files a `chief-unavailable` ADR within 15 minutes citing this drill.
- **Heartbeat tag**: The day's `heartbeat-<date>.md §Degraded` contains `chief-degraded: <name>` for the drill window.
- **No collateral damage**: No real (non-drill) ADR mistakenly carries the `drill-window` tag; no real dispatch was re-routed during the window.

Missing any of the above = **fail** or **pass-with-gaps**, per `SKILL.md §Classify outcome`.

## Teardown

1. Confirm the Chief's config is restored (model tier back to normal).
2. Write the drill-report ADR: `ADR-NNNN-drill-report-chief-unavailable-<YYYY-MM-DD>.md`. Cite the Chief drilled, recovery time, gap list, remediation commitments.
3. For each gap: file `drill-followup-<slug>` ADR with owner + due date (must be ≤ 30 days — the next drill is a month away).
4. Archive the run log at `_vision/drills/chief-unavailable/<YYYY-MM-DD>.md` with full timestamp trail.
5. Emit `drill-chief-unavailable-<outcome>` notify event.

## Never

- Never drill a blocking Chief (CISO, CEVO, CRT, CAO) — they hold veto on the ship path and cannot be safely offline even for 30 minutes.
- Never drill the same Chief twice in a calendar year. Fresh eyes per Chief per year.
- Never extend the window past 30 minutes. The point is a small, recoverable perturbation — not an actual outage.
- Never drill during a live degraded mode that overlaps the Chief's role. Real outages don't need synthetic ones on top.
- Never use a real USER-ONLY decision as the synthetic dispatch. Synthetic means synthetic.
