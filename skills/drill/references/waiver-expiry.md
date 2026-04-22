# drill/references/waiver-expiry.md

Annual drill exercising the `waiver-expiry` failure mode from `RESILIENCE.md` + `skills/waivers/references/expiry-protocol.md`. Invoked by `rhythm` in week 2 of Q1 (typical slot).

## Purpose

Confirm the end-to-end waiver-expiry flow works: a synthetic waiver with a 24-hour expiration gets granted, pre-remediated before expiry, and on the expiry day the rhythm heartbeat detects the row, files the `waiver-expiry` ADR with `outcome: remediated`, and moves the row from `active.md` to `history.md`.

## Why annual (not quarterly or monthly)

Waivers in the real system are rare (the user approves each one individually), and the expiry protocol is materially wired into `rhythm` + `audit` + `ladder` in ways that only exercise when a waiver is actually expiring. An annual drill is enough to catch drift between the skill and the wiring; more frequent runs would pollute `_vision/waivers/history.md` with synthetic entries without value.

## Pre-flight

1. Read `_vision/rhythm/state.json`. If any real waiver has `expiration: <within 7 days>`, skip the drill — we don't want the synthetic expiry entangling with a real one. Reschedule to a week with no real expirations pending.
2. Read `_vision/waivers/active.md`. If any real waiver is active, carry on — real and synthetic can coexist in active.md as long as their expiry dates differ.
3. Confirm user consent for the drill. This drill routes through the user-meeting flow for the synthetic grant (per the `skills/waivers` §Process). Because the real user is the synthetic approver, a pre-announcement is required ≥ 2 business days before the drill grant. The consent is for the drill itself, not a real waiver — the user-meeting capture records `drill: waiver-expiry, synthetic: true`.

## Execution

1. **Create a synthetic finding.** The drill specialist files a synthetic row in a sandboxed findings ledger (NOT in `_vision/red-team/findings.md` — use `_vision/drills/waiver-expiry/<YYYY>/synthetic-finding.md`). The finding is tagged `synthetic: true, drill: waiver-expiry` so it will never be confused for a real red.
2. **Pre-remediate.** Before the grant, the drill specialist files the remediation ADR — `ADR-NNNN-drill-waiver-expiry-remediation-<YYYY>.md` — showing the synthetic finding has been fixed. This pre-remediation ensures the expiry outcome will be `remediated`, not `re-fired`.
3. **Grant the synthetic waiver.** Route through `skills/waivers` with a 24-hour expiration:
   - Finding id: the synthetic id.
   - Artifact: `_vision/drills/waiver-expiry/<YYYY>/synthetic-artifact.md`.
   - Remediation plan: 1 step — "the pre-remediation ADR-NNNN covers the fix; verify at expiry".
   - Expiration: exactly 24 hours from the grant moment, at heartbeat time.
   - Every field in the request template carries `drill: waiver-expiry, synthetic: true`.
4. **User approval.** The user-meeting capture records drill approval. The grant ADR files normally into `_decisions/`, but carries `drill: waiver-expiry, synthetic: true` in the front matter.
5. **Row lands.** The drill specialist verifies the row appears in `_vision/waivers/active.md` with the 24h expiration.
6. **Wait for expiry-day heartbeat.** 24 hours later, the rhythm daily heartbeat invokes step 8 of `skills/waivers/SKILL.md`. The drill specialist observes:
   - The expiry-day heartbeat detects the row via `expiration: <today>`.
   - Per the expiry-protocol, the pre-remediation ADR is located via finding-id search.
   - Classification: `remediated` (because the pre-remediation ADR exists and the originating synthetic finding has `closed: yes`).
   - `ADR-NNNN-waiver-expiry-<synthetic-slug>.md` files with `outcome: remediated`, also carrying `drill: waiver-expiry, synthetic: true`.
   - The row moves from `active.md` to `history.md` with the outcome appended.
   - A `waiver-expiry` notify event emits.

## Pass criteria (verification)

- **Grant ADR filed**: present in `_decisions/` with `drill: waiver-expiry, synthetic: true`.
- **active.md populated**: synthetic row added with correct 24h expiration.
- **Expiry detection**: the day-of heartbeat identifies the row within its normal run window.
- **Outcome classification correct**: expiry ADR outcome is `remediated` (not `partial` or `re-fired`).
- **Expiry ADR filed**: present in `_decisions/` with `drill: waiver-expiry` tag.
- **Row moved**: `active.md` no longer contains the synthetic row; `history.md` contains it with outcome `remediated`.
- **Notify event**: one `waiver-expiry` event emitted, tagged drill.
- **No real-system pollution**: no entries in `_vision/red-team/findings.md`; no real-looking ADR without the drill tag.

## Teardown

1. Write `ADR-NNNN-drill-report-waiver-expiry-<YYYY-MM-DD>.md` citing outcome, timings, gap list.
2. Archive run log at `_vision/drills/waiver-expiry/<YYYY-MM-DD>.md`.
3. For each gap: file `drill-followup-<slug>` with owner + due date (≤ 365 days — next annual drill).
4. Leave the synthetic finding + pre-remediation ADR + grant ADR + expiry ADR in place — they are append-only. The drill-artifact tag is the audit mechanism for separating them from real rows.
5. Emit `drill-waiver-expiry-<outcome>` notify event.

## On failure classifications

If during the drill the outcome classifies as `re-fired` (the expiry protocol didn't find the pre-remediation ADR), that's a **fail**. The `skills/waivers/references/expiry-protocol.md` §Per-row procedure is broken — file a Rung 3 drill-followup immediately. Re-run the drill within 30 days with the fix landed.

If the outcome classifies as `partial`, something in the finding-id → remediation-ADR linkage is weak. **Pass-with-gaps**; drill-followup ADR must sharpen the linkage check before next year's drill.

## Never

- Never use a real red-team finding as the drill subject. The synthetic flag is mandatory; confusing real and synthetic reds is a CAO red on its own.
- Never grant the synthetic waiver through a side channel to save user-meeting overhead. The user-meeting flow is part of what we're drilling.
- Never extend the 24-hour expiration. A longer window wastes active.md real estate and a shorter window risks the grant and expiry landing in the same heartbeat (which would hide bugs).
- Never silently remove drill ADRs after the fact. They are append-only evidence of the drill.
- Never drill two waiver-expiries in the same year. One annual slot; if you need a second run (because the first failed), it's a re-drill and still counts as "one year's drill" for rotation purposes.
