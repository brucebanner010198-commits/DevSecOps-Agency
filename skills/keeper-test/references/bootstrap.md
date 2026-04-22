# keeper-test/references/bootstrap.md

First-quarter rules for the Keeper Test. Used until the review window has ≥ 30 days of real data.

## Why a bootstrap phase

The thresholds in `axes.md` assume:

- ≥ 5 reports per agent (for Axis 1).
- ≥ 5 tasks per agent (for Axis 2).
- ≥ 90 days of session logs, ADRs, audit findings.

At v0.3.8 ship-date, the agency has zero shipped end-user projects. The first 1–2 quarters will have insufficient data for full grading.

## Bootstrap rules

### Quarter 0 (window < 30 days or < 1 shipped project)

- **Skip the review.** Write `_vision/roster/performance-<date>.md` with a single line: `"bootstrap — roster under 30 days, no review this cycle."`
- File an ADR: `_decisions/ADR-NNNN-keeper-test-bootstrap-skip.md`, kind `keeper-test-bootstrap`.
- Next review: first quarter with ≥ 30 days of active roster use.

### Quarter 1 (window 30–90 days, < 3 shipped projects)

- **Run Axis 3 + Axis 4 only.** Audit findings and values compliance can score with thin data — a single violation is still a red.
- Skip Axis 1 + Axis 2 with `insufficient-sample`.
- Ratings:
  - Axis 3 + 4 both green → **preliminary green**. Keep.
  - Axis 3 or 4 yellow → **preliminary yellow**. Upgrade allowed but not mandatory.
  - Axis 3 or 4 red → **preliminary red**. Run full action flow (repurpose / fire per `actions.md`).
- Tag the performance row: `rating: preliminary-green` etc. Next review is the first full review.

### Quarter 2+

Full review per `axes.md`. No bootstrap rules.

## On-demand review during bootstrap

If a mid-quarter trigger fires (CAO finding, prompt-diff bouncebacks, user request):

- **Always run Axis 3 + Axis 4** regardless of window size.
- Axis 1 + Axis 2 run only if sample size crosses 5.
- Ratings tagged `mid-cycle-<axis-set>` to distinguish from quarterly.

## Writing the first performance file

Even with all-insufficient data, write the file. Its existence is the audit trail that the cadence is being respected.

```markdown
# performance-<YYYY-MM-DD>.md

- **Review kind:** quarterly / bootstrap / mid-cycle
- **Window:** YYYY-MM-DD → YYYY-MM-DD
- **Roster size:** <n> (excluding reserved)
- **Skipped this cycle:** bootstrap — <reason>

## Rated agents

| Agent | Rating | Axis 1 | Axis 2 | Axis 3 | Axis 4 | Action |
| --- | --- | --- | --- | --- | --- | --- |
| <none> | - | - | - | - | - | - |

## Notes

Bootstrap quarter — full review resumes <date>.
```

## Forbidden shortcuts

- **Don't backfill session logs or ADRs to make the window look full.** Append-only (`VALUES.md §4`); past can't be edited.
- **Don't promote preliminary-green to green.** They are different ratings. Readers of `_vision/roster/performance-*.md` must see the distinction.
- **Don't skip the ADR at bootstrap.** Even a skipped review files an ADR. Zero-ADR quarters are CAO reds.
- **Don't defer the review "until we have more data."** Run it on the cadence. Skip axes, not the review itself.
