# scoring-rules — green/yellow/red/n/a rubric

Applied by `okr.score` after every Chief report. Same matrix every phase. No freestyle.

## The four colors

### green — measurable advance

The phase produced an artifact or decision that **measurably** moved this KR forward.

Green requires:
- A **concrete artifact** (research file, design doc, test report, deploy log) that ties to the KR.
- A **one-line quantitative claim** in the report ("coverage rose from 0% to 72%", "time-to-first-deploy hit 19 days", "threat-model closed out 4 of 5 STRIDE categories").
- No regression on any other KR.

### yellow — neutral or tangential

The phase did not regress the KR but did not measurably advance it either. This is the **default** — phases that don't touch a KR score yellow.

Yellow includes:
- Phase was infrastructure (CI setup) while KR is user-facing (MRR).
- Phase output was partial (research done but wedge not confirmed).
- Phase shipped with caveats that don't regress the KR.

### red — regression

The phase made the KR **harder to achieve** or demonstrably backslid on it.

Red examples:
- Time-to-launch KR is 21 days; this phase pushed ETA to 28 days.
- MRR KR is $100 in 30 days; this phase added a paywall that testers say they'd avoid.
- Red-team-on-100%-of-launches KR; phase skipped red-team council with waiver.
- Non-goal was "no regulated industries"; phase proposed adding HIPAA feature.

Red requires the same level of evidence as green — a cite and a claim.

### n/a — not applicable

The KR genuinely does not apply to this phase. Use sparingly. If **all 3 selected KRs** score n/a for a phase, the selection is wrong — re-run `vision-doc > cascade-rules.md` with the pool expanded.

## Aggregation rule (per-phase)

Per-phase `okr_alignment` = worst of the 3 KR scores, with this precedence:

```
red  >  yellow  >  green  >  n/a
```

Any single `red` → phase `red`. No `red` but any `yellow` → phase `yellow`. All `green` (or `green + n/a` mix with ≥ 1 green) → phase `green`. All `n/a` → phase `n/a` (and flag the cascade selection as suspect).

## What counts as evidence

**Green** evidence:
- Artifact in the project folder.
- A number with a delta (before → after).
- A test report or metric file.

**Red** evidence:
- A decision documented in `chat.jsonl > board-decision`.
- A regression detected by QA or red-team.
- A cost / time / scope change that worsens the KR.

**Yellow** needs only a one-line rationale. No artifact required.

## Interaction with the `gates` skill

`okr_alignment` is additive to council gates. The combined signal follows `skills/gates/references/gate-rules.md` (extended in Wave 1 to include OKR alignment):

| Council gate | OKR alignment | Combined action                                  |
| ------------ | ------------- | ------------------------------------------------ |
| green        | green         | advance                                          |
| green        | yellow        | advance, note in board decision                  |
| green        | red           | **escalate to user (proceed-vs-halt decision)**  |
| yellow       | any non-red   | advance, note in board decision                  |
| yellow       | red           | **escalate to user + block phase until resolved**|
| red          | any           | block phase (council already blocks)             |
| n/a          | green/yellow  | advance                                          |
| n/a          | red           | **escalate to user**                             |

The CEO NEVER silently overrides a `red` OKR alignment. It's always an ADR + an inbox item.

## Examples

**CRO Discovery report, student expense tracker:**
- [PKR1.1] green — Market research identifies dorm wedge; cites `research/market.md:34`.
- [PKR1.3] green — CRO finished in 2 days, ahead of 3-day budget, keeps launch-time KR on track.
- [KR3.1] green — 3 patterns cited from `_memory/patterns/`.
- `okr_alignment: green`.

**VP-Eng Build report, same project, authentication chosen poorly:**
- [PKR1.1] yellow — Build shipped functional auth; no MRR impact yet.
- [PKR1.3] red — Build took 9 days vs 5-day budget, pushes launch ETA over the KR threshold.
- [KR2.1] yellow — CISO not yet re-engaged, so security KR not scored.
- `okr_alignment: red`.

**CKO Document report, infra project:**
- [KR3.1] n/a — no patterns apply at doc phase.
- [PKR2.1] n/a — doc phase not user-facing.
- [KR1.3] yellow — docs took 1 day, no launch impact either direction.
- `okr_alignment: yellow` (re-run cascade selection for next phase — 2 n/a signals the slice is wrong).

## Never

- Score green without a cite.
- Score yellow as a dumping ground — prefer n/a when genuinely non-applicable.
- Score red without an artifact or decision reference.
- Aggregate with a rule other than worst-of-three.
- Let `okr_alignment: red` pass without inbox escalation + ADR.
