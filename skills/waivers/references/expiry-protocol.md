# waivers/references/expiry-protocol.md

Exact flow for the expiry-day check. Invoked by step 8 of `skills/waivers/SKILL.md`, driven by the rhythm daily heartbeat.

## Precondition

`_vision/waivers/active.md` contains at least one row with `expiration: <today>`.

## Per-row procedure

For each row matching today's date:

1. **Locate the remediation target.** Read the row's `remediation plan:` steps. For each step, search `_decisions/` for an ADR whose body cites the finding id.
2. **Classify outcome:**
   - **Remediated** — every remediation-plan step has a matching ADR, AND the originating red has a closing row (e.g., `red-team/findings.md` marked `closed: yes`). The finding is genuinely fixed.
   - **Partial** — some steps have ADRs, others don't. The finding may or may not re-fire depending on whether the core fix landed. Independence rule: the judgment that "core fix landed" belongs to the originating chief, not the waiver owner.
   - **Unremediated** — no remediation ADRs, or the originating red still stands.
3. **File the expiry ADR.** Always file `ADR-NNNN-waiver-expiry-<slug>.md`:
   - On **remediated**: `outcome: remediated`; cite closing ADRs; mark active.md row for move.
   - On **partial**: `outcome: partial`; escalate to originating chief for a judgment; freeze active.md row pending judgment (expiration date does not auto-extend — this is an explicit exception requiring user re-approval for any extension).
   - On **unremediated**: `outcome: re-fired`; re-open the originating finding; mark active.md row for move + immediate notify.
4. **Move the active.md row to history.md** with the outcome appended.
5. **Notify.** Emit `waiver-expiry` event with finding id, slug, outcome, and (on re-fired) the Rung 3 ladder trigger.
6. **On re-fired, escalate.** The original blocking red is now live again. Invoke `skills/ladder` at Rung 3 (material decision → ADR). If the artifact is in production, the Rung 3 ADR proposes either (a) rollback, (b) emergency fix, or (c) a second waiver request — all of which go back through the USER-ONLY approval chain.

## On the day after expiry

The rhythm daily heartbeat that day re-checks active.md. Any row whose expiration was yesterday should already have moved to history.md. If one hasn't, that's a `skills/audit` red — the expiry protocol was not run. File `ADR-NNNN-expiry-missed-<slug>.md` and run the protocol retroactively.

## Extensions

A waiver's expiration can be extended **only via a new waiver request** (not by editing the existing one — `VALUES.md §4` append-only). The new request cites the prior grant ADR and justifies why the remediation plan slipped.

Extensions routinely denied if:

- The original remediation plan had zero steps complete.
- The reason-to-extend is the same reason as the original reason-to-waive (no new information).
- The finding is `critical` severity (extension here requires a formal incident-response review, not a new waiver).

## Multi-waiver interactions

If a project has ≥ 2 active waivers:

- Daily heartbeat adds a "multi-waiver degraded" tag to the project in `heartbeat-<date>.md`.
- On any expiry (regardless of outcome), the CEO must re-review the remaining waivers with the blocking chiefs and decide whether the project still has a viable close path.
- ≥ 4 active waivers on one project = automatic Rung 4 (replan) escalation.

## Never

- Never auto-extend a waiver. Extensions are user-only (see `GOVERNANCE.md` decision matrix).
- Never silently move a row from active.md to history.md without a matching expiry ADR.
- Never apply remediated-outcome without the originating chief's sign-off ADR.
- Never run the expiry protocol during an active incident affecting the same artifact. Pause, handle the incident, then resume.
