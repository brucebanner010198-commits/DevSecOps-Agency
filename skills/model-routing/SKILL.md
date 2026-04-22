---
name: model-routing
description: Emergency model-tier reroute protocol. Owned by model-routing-override. Applies time-boxed lateral moves (same tier, different vendor) during outages; never downgrades long-term. Every override files an opening ADR + a closing ADR and tags every session-log entry written under it.
metadata:
  version: 0.3.0
---

# model-routing

Vendor outages happen. The agency keeps shipping by crossing sideways, not down.

## When to use

- Vendor API returning persistent 5xx / 529 / rate-limit errors.
- Vendor status page confirms outage.
- A specific model family is unavailable for ≥ 15 min on the affected tier.

## Process (apply)

1. **Confirm** — status page + observed error rate. No override on rumor.
2. **Select fallback** — read `references/fallback-matrix.md`, pick the same-tier row.
3. **Cap the override** — default 2h, max 24h. Beyond 24h → Rung 6 user consult.
4. **Write override record** — `_vision/sre/<date>-override.md`.
5. **File opening ADR** — `override_applied`, affected agents, fallback, cap.
6. **Tag session logs** — every affected agent's session-log entry gets `[routing-override:<adr-id>]`.
7. **Notify** — Chiefs affected + CEO.

## Process (revert)

1. **Confirm recovery** — error rate back to baseline for ≥ 15 min.
2. **Restore** — original routing back in place.
3. **File closing ADR** — `override_reverted`, reference to opening ADR, duration.
4. **Spot check** — one affected agent, confirm it's back on its designated tier.

## Tier floor

- Opus tier → Opus only (or Opus-class from another vendor).
- Sonnet tier → Sonnet or Sonnet-class only.
- Haiku tier → Haiku or Haiku-class, OR temporary upgrade to Sonnet under override.

Downward crossings (Sonnet → Haiku) are **forbidden**, even during outages. Opus / Sonnet agents wait or escalate.

## ADR triggers

- Every opening.
- Every closing.
- Every renewal past the initial cap.
- Every fallback-matrix amendment.

## Invariants

- Every override is time-boxed.
- Every override has an opening + closing ADR. Orphans are a CAO red.
- Every session-log entry written under override is tagged.
- Downward crossings forbidden.
- New fallback targets require a scout report first.

## What never happens

- Silent downgrade to save budget.
- Override without status-page confirmation.
- Untagged session-log entries under override.
- Override outliving its cap without a renewal ADR.
- Crossing into a model family not on the matrix.
