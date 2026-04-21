# eval-set-rubric — per-tier item shapes

Authoritative rubric for `eval-designer` + `benchmark-runner`. Items that don't fit a tier are rejected.

## Tier: functional

- Question: "does feature X do Y under input Z?"
- Ground truth: a reproducible command, HTTP request, CLI invocation, or file diff check.
- Pass criteria: exact-match or within-tolerance for numerics (tolerance declared in item).
- Example:
  - **Q:** Does `POST /split` with `{members: 3, amount: 30}` return 3 equal shares?
  - **Truth:** `curl -X POST .../split -d '{...}'` returns `[10, 10, 10]` (± 0.01).
  - **Tier:** functional.

## Tier: ux

- Question: "can a new user complete task X in ≤ N steps / ≤ M seconds?"
- Ground truth: a scripted user session or a deterministic flow test producing a numeric result.
- Pass criteria: step count / duration within declared bound.
- Example:
  - **Q:** Can a new user create an account + split a bill in ≤ 5 clicks?
  - **Truth:** Playwright script counting clicks.
  - **Tier:** ux.

## Tier: promise

- Question: "does artifact X convey promise Y with sufficient clarity?"
- Ground truth: a 1–5 rubric declared in the item.
- Pass criteria: score ≥ 4.
- Example:
  - **Q:** Does the README land the core promise ("split bills without Venmo") in ≤ 30 seconds of skim?
  - **Rubric:**
    - 5 = promise in the first sentence, example in the first screenful
    - 4 = promise in the first screenful
    - 3 = promise requires scrolling
    - 2 = promise requires digging
    - 1 = promise is implied only
  - **Tier:** promise.

## Rejection patterns

Do not write items whose:

- Ground truth is "the Chief reported green." Gate color ≠ eval evidence.
- Ground truth depends on human judgment not captured in a rubric. Either add a rubric or promote to `tier: promise`.
- Ground truth requires data the agency does not hold. Only artifacts + public/provided inputs.
- Pass criteria is relative to the shipped artifact. Pass criteria is absolute, derived from the PKR.

## Coverage discipline

- ≤ 25 items total per project. Dilute if > 25; insufficient coverage if < 3 per PKR.
- ≥ 1 functional item per PKR where technically possible. Pure-`promise` PKRs are allowed but flagged to CPO for possible PKR revision.
- ≥ 1 `promise`-tier item on at least one PKR. Total promise-absence is a smell.

## Subjectivity budget

- Max 30 % of items in `tier: promise`. Beyond that, the project is measuring feels more than function.
- `promise` items must cite the PKR verbatim in the question. No paraphrase drift.

## Item lifecycle

- Items are authored per-project by `eval-designer`.
- Canonical items (reused across projects) are promoted to `_vision/eval/regression-baseline.md` at quarter boundary only, via ADR.
- Retired items (outdated, obsoleted by PKR change) are moved from the baseline in the same quarter-boundary ADR. Never silently dropped.
