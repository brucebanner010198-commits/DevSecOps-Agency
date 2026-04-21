# councils/strategy — boundaries

## Output contract

- Lead: `cso`. Specialists: trend-scout, competitive-analyst, market-sizer, opportunity-ranker.
- Artifact root: `_vision/strategy/` (portfolio-level, NOT per-project).
- Consolidated shortlist: `_vision/strategy/opportunity-shortlist.md`.
- Informing council. Not blocking. Reds escalate to CEO, not user-blocking.

## Scope boundary

- Portfolio only. Per-project market scans, wedge validation, and tech stack selection are CRO's domain.
- Strategy council is convened on REM dreaming trigger, quarter roll-up, or user-initiated idea pipeline — never mid-project.

## Must

- Read last `_vision/strategy/*.md` iteration (if exists) before writing. Track deltas, not snapshots.
- Cite every movement claim. "<competitor> moved" requires a source.
- Use the shared RICE + narrative rubric from `skills/idea-pipeline/references/ranking-matrix.md`. No bespoke scoring.
- Every opportunity-shortlist entry must trace to ≥ 1 active workspace OKR or an explicit "new-thesis" flag.
- Retire signals that appear unmoved across 3 radars. No zombie signals.

## Must not

- Pick winners. CSO ranks; CEO selects top-5; user picks 1–2.
- Skip the adjacency check — every new candidate must have a plausible bridge from an existing proven stack or flagged `[greenfield]`.
- Carry a retired competitor forward without an audit trail line.
- Kill a thesis on 1 data point. Require ≥ 2 closed projects or ≥ 2 quarters of contradicting evidence.
- Size a market CRO has red-wedged.

## Gate heuristic

- `green`: top-5 with stated basis per candidate, all 4 artifacts present, CMO narrative score layered in.
- `yellow`: top-5 landed but ≥ 1 low-confidence sizing without identified next evidence.
- `red`: ranker failed to converge · missing upstream artifact · top-5 contradicts active OKRs with no thesis flag.

## OKR alignment hint

- If `opportunity-shortlist.md` Top-5 contains zero entries tracing to any active OKR, emit `okr_alignment: red` to CEO. This is an ADR-mandatory trigger (pivot-class).
