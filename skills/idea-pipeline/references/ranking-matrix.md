# idea-pipeline ranking matrix (stage 3)

Shared rubric for every scorer. No bespoke formulas. `opportunity-ranker` is the only agent that computes the composite.

## Axes and scales

| Axis | Scorer | Scale | Definition |
| --- | --- | --- | --- |
| Reach | market-sizer | 1–5 (SOM / max(SOM) · 5) | Reachable users in year 1 relative to biggest candidate |
| Impact | opportunity-ranker | 1–5 | Strategic fit to highest-priority active OKR |
| Confidence | market-sizer + competitive-analyst | 1–5 (avg) | sizing confidence + defensibility, halved |
| Effort | opportunity-ranker | 1–5 (inverse of weeks) | Lower weeks = higher score. ≤ 4w = 5, 5–8w = 4, 9–14w = 3, 15–24w = 2, > 24w = 1 |
| Narrative | CMO (merged positioning + comms + growth) | 1–5 (avg) | Narrative clarity, wedge strength, activation feasibility |

## Composite formula

```
RICE_raw       = (Reach · Impact · Confidence) / Effort
RICE_norm      = (RICE_raw / max(RICE_raw)) · 5
Composite      = (RICE_norm · 0.6) + (Narrative · 0.4)
```

- `RICE_norm` normalisation uses the max across current scorecard (per-batch, not all-time).
- 0.6 / 0.4 weighting reflects "financial reality ≥ story, but story is half the battle at pipeline stage".
- Override: CEO may adjust weights once per quarter with ADR — not per-pipeline.

## Tie-break order (when composites within 0.2)

1. Higher Confidence wins.
2. Stronger wedge (from `competitive-map.md`) wins.
3. Shorter effort wins.
4. Mission-fit strength (link depth to active OKRs) wins.
5. Coin flip — document in ADR as "tie-broken by chance" and mark for re-evaluation next quarter.

## Rubrics (shared language)

### Impact 1-5

- 5 — directly advances a KR for an active OKR this quarter
- 4 — advances an active OKR this or next quarter
- 3 — advances an active Objective (no specific KR trace)
- 2 — enables future OKRs (≥ 2 quarters out)
- 1 — no OKR trace, hypothesis stage

### Confidence 1-5

- 5 — ≥ 2 shipped comparable projects + sizing H + defensibility H
- 4 — 1 shipped comparable + sizing M + defensibility M or H
- 3 — analogue exists in adjacent market + sizing M
- 2 — sizing L but directionally plausible
- 1 — no precedent, pure hypothesis

### Narrative 1-5

- 5 — elevator ≤ 30 words, ≥ 2 cited proof points, clear category, zero-objection demo possible
- 4 — elevator crisp but 1 axis weak (category contested or proof thin)
- 3 — positioning viable, but 2 axes need work
- 2 — can position but narrative hinges on an unresolved claim
- 1 — cannot tell a clean story in the time available

## Disqualification rules

Even if composite is top, a candidate is disqualified if:

- Any hard-kill filter was waived without ADR (kickback to stage 2).
- `okr_alignment: red` (the Strategy council's own OKR scoring tagged red for this candidate).
- Any upstream artifact (trend, competitive, sizing, narrative) missing.

Disqualified candidates appear in `opportunity-scorecard.md > ## Disqualified` with the failing rule cited.
