---
name: trust-scorecard
description: >
  Compute and publish the quarterly Trust Scorecard defined in TRUST.md §3,
  measuring each of the twelve public commitments against its target and
  assembling the evidence trail.  Run at the end of every quarter (first
  publish 2026-07-22) and on demand before any public announcement or
  external audit.  Trigger phrases include "publish trust scorecard",
  "run trust scorecard", "quarterly trust report", or any
  /devsecops-agency:trust-scorecard invocation.
metadata:
  version: "1.0.0"
---

# trust-scorecard — Quarterly Trust Scorecard

Authority: [`TRUST.md`](../../TRUST.md) §3 + [`GOVERNANCE.md`](../../GOVERNANCE.md)
Owner: CAO · Reviewer: CEO · Called by: `skills/rhythm` (quarterly cadence), on demand

## Purpose

Quantify each of the twelve public commitments in [`TRUST.md`](../../TRUST.md) §2 and publish the result. This is the single most important step we take to convert claims ("we do X") into evidence ("here is X, counted, sourced, dated").

## When to run

- **Required:** End of every calendar quarter (Jan 31, Apr 30, Jul 31, Oct 31).
- **Required:** Within 7 days of any Severity ≥ High incident closure.
- **On demand:** Before any external audit, public announcement, or major release.

## Inputs

1. All session logs from the measurement period.
2. All ADRs from the period.
3. All LESSONS rows from the period.
4. All waivers issued and their expiry dates.
5. Keeper Test results for the quarter (if any).
6. RCA files produced.
7. Git history on `main` for the period.

## Procedure

### Step 1 — Establish the measurement period

Default: the calendar quarter just ended. Override for incident-driven or on-demand runs; state the period at the top of the scorecard.

### Step 2 — For each commitment in TRUST.md §2.1 through §2.12, compute the metric

| # | Commitment | Metric | Target |
|---|---|---|---|
| 1 | Receipts ratio | decisions_logged / decisions_made | 100% |
| 2 | Append-only ledger | in-place modifications of append-only paths | 0 |
| 3 | Four blocking vetoes real | vetoes invoked vs. missed-veto audit findings | drift-flag if veto→0 |
| 4 | Ten USER-ONLY actions | agent-side attempts that bypassed | 0 unblocked |
| 5 | Security baseline | projects shipped w/o threat model, SBOM, license check | 0 |
| 6 | Prompt-diff review | persona/skill edits passing review / total | 100% |
| 7 | Runtime hooks | sessions without all 6 hooks present | 0 |
| 8 | Memory novelty gate | memory additions bypassing Jaccard 0.65 | 0 |
| 9 | Rhythm cadence | scheduled events missed without documented slip | 0 |
| 10 | Never-give-up ladder | Rung 7/8 reached without User notification | 0 |
| 11 | Reproducibility | commit→release→SBOM chain verifiable | 100% |
| 12 | Independence of CAO/CEVO/CRT/CSRE | their vetoes touched by delivery pressure | 0 |

Also compute:

- **Severity ≥ High incidents:** count.
- **Mean time to acknowledge (MTTA)** for reported vulnerabilities.
- **Mean time to patch (MTTP)** Critical.
- **Waiver inventory:** active count; expired-and-not-renewed count.
- **Veto invocation rate:** per quarter.

### Step 3 — Assemble evidence per row

For each commitment, list the evidence source (log path, commit SHA range, ADR ID, audit finding ID). A commitment without evidence is not reportable — state "evidence insufficient" rather than fabricate.

### Step 4 — Produce the scorecard document

Template:

```markdown
# Trust Scorecard — YYYY-Q[N]

**Period:** YYYY-MM-DD to YYYY-MM-DD
**Published:** YYYY-MM-DD
**Plugin version:** vX.Y.Z
**Prepared by:** CAO  · **Approved by:** CEO

## Summary

One paragraph: overall health.  Any targets missed?  Any trending-down metrics?

## Scorecard

| # | Commitment | Metric | Target | Actual | Status | Evidence |
|---|---|---|---|---|---|---|
| 1 | Receipts ratio | ... | 100% | 100% | PASS | sessions/*.log |
| ... | ... | ... | ... | ... | ... | ... |

## Incidents this period

| Severity | Count | MTTA (h) | MTTP (d) |
|---|---|---|---|
| Critical | ... | ... | ... |
| High | ... | ... | ... |

## Waiver inventory

Active: N.  Expired this period: M.  Unrenewed: K.

## Veto activity

Invoked: { CISO: n, CRT: n, CEVO: n, CAO: n }.
Missed-veto audit findings: N.
Drift flag: [yes/no].

## Drift signals

Any metric trending away from target across two consecutive quarters.

## Lessons learned

Paste / link the LESSONS rows added this quarter.

## Next quarter focus

Three to five areas of emphasis.
```

### Step 5 — Publish

1. Commit to `_meetings/trust-scorecard-YYYY-Q[N].md`.
2. Link from [`TRUST.md`](../../TRUST.md) §3.
3. If v0.6.0+ has a public dashboard, update it.
4. If a target was missed, a written explanation accompanies the scorecard (not excuses — plain analysis of cause and the corrective action).

### Step 6 — Post-publish actions

- If any commitment is **below target**, open an incident or corrective-action issue within 7 days.
- If any commitment shows **sustained drift** (below target 2 consecutive quarters), escalate to CEO with an ADR proposal.
- If veto invocations trend to zero without matching drop in findings, trigger an agreeableness-drift review per [`SWOT.md`](../../SWOT.md) T12.

## Anti-patterns

- **Narrative-only scorecard.** Without numbers, it is marketing.
- **Moving the target.** Targets are fixed per commitment; if one needs to change, amend [`TRUST.md`](../../TRUST.md) with an ADR — don't silently adjust here.
- **Hiding misses.** A missed target published honestly is more trustworthy than a near-miss dressed up. Publish misses prominently.
- **Skipping a quarter.** A skipped scorecard is itself a Trust commitment failure (§2.9).

## Outputs

- `_meetings/trust-scorecard-YYYY-Q[N].md` — the scorecard.
- One LESSONS row per sustained drift signal.
- Updated summary link in [`TRUST.md`](../../TRUST.md) §3.
- If miss → incident issue + corrective action in backlog.

## References

- [`TRUST.md`](../../TRUST.md) — the commitments.
- Google SRE Book — SLI/SLO/SLA framework.
- NIST CSF 2.0 — Measure function.
