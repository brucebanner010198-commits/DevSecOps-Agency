# regression-thresholds — when a score delta matters

Authoritative table for `regression-detector`.

## Per-item thresholds (single eval item score delta)

| Delta (current − baseline)     | Classification     | Flag                     | ADR?  |
| ------------------------------ | ------------------ | ------------------------ | ----- |
| ≥ +5 pp                        | improvement        | `## Improvements` section| No    |
| +5 pp to −5 pp                 | noise              | no entry                 | No    |
| −5 pp to −10 pp (exclusive)    | minor regression   | yellow-flag              | Yes (yellow) |
| ≥ −10 pp (exclusive of −20)    | material regression| red-flag                 | Yes (red) |
| ≥ −20 pp or pass → fail flip   | severe regression  | red-flag + ladder Rung 3 | Yes (red)    |

## Aggregate thresholds (portfolio-wide pass-rate delta vs prior quarter)

| Aggregate delta                | Classification     | Action                                               |
| ------------------------------ | ------------------ | ---------------------------------------------------- |
| ≤ −2 pp                        | within noise       | log, no action                                       |
| −2 pp to −5 pp                 | yellow             | file ADR; assign follow-up to likely-cause council   |
| ≥ −5 pp                        | red                | file ADR; Rung 3 escalation; paired roster review    |

## Set-drift thresholds (new vs retired eval items)

| Set-drift ratio (new+retired / baseline size) | Classification | Action                                          |
| --------------------------------------------- | -------------- | ----------------------------------------------- |
| ≤ 10 %                                        | healthy        | log only                                        |
| 10–25 %                                       | yellow         | CEVO notes in quarter-roll-up report           |
| > 25 %                                        | red            | ADR: baseline churn too high; pause regression scoring for one quarter while baseline stabilises |

## Root-cause taxonomy

Regression-detector must tag each red with one of:

- `prompt-rot` — an agent prompt changed between the runs (check `git blame` on `agents/<name>.md`).
- `tier-drift` — model tier changed on a relevant agent (check `model:` frontmatter history).
- `skill-edit` — a skill's SKILL.md or references changed.
- `budget-squeeze` — early compaction triggered by tight budget; confirm via budget-ledger.
- `input-drift` — the eval item's input changed (spec change upstream).
- `baseline-defect` — the baseline item was wrong; proposes baseline revision at next quarter boundary.
- `unknown` — no plausible cause surfaced.

Every red ADR cites the root-cause tag.

## Anti-patterns

- Don't smooth a regression by re-running. First run counts.
- Don't re-normalise scores to match prior quarter. That's cheating the invariant.
- Don't silently retire a regressing item to remove it from the delta. Retirements go through quarter-boundary ADR.
- Don't escalate directly to Rung 6 on regression alone. Rung 3 (cross-council) comes first unless the regression root-cause is explicitly user-credential or user-judgment.
