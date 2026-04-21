# rollup-rubric — quarter aggregation rules

Applied by `okr.rollup` at quarter boundary or when user says "wrap the quarter". Runs once; idempotent per quarter.

## Input corpus

- All `_vision/projects/*.md` whose `## Closed > Date` falls within the quarter.
- All in-flight projects' most recent `## Score log` entries (to surface red flags early).

## Per-workspace-KR aggregation

For each KR in `_vision/VISION.md > ## Active OKRs`:

1. **Find traced project-KRs.** Search every `projects/*.md > ## Project OKRs` for `_traces_ ← [KR<n.n>]` lines matching this KR.
2. **Pull final scores.** For each traced project-KR, read the `## Closed > Final scores:` line (or, for in-flight projects, the last `## Score log` entry).
3. **Count outcomes:**
   - `green_count` — final score green or last-entry green.
   - `yellow_count` — final score yellow.
   - `red_count` — final score red.
   - `na_count` — final score n/a or PKR never scored.
4. **Apply the rubric:**

   | Evidence                                              | Workspace-KR color |
   | ----------------------------------------------------- | ------------------ |
   | `green_count >= 2` AND `red_count == 0`               | green              |
   | `green_count >= 1` AND `red_count == 0`               | yellow             |
   | `green_count == 0` AND `yellow_count >= 1`            | yellow             |
   | `red_count >= 1` (regardless of greens)               | red                |
   | No traced projects shipped this quarter               | red (no evidence)  |

5. **Quantitative override.** If the KR carries a number (e.g. `≥ $100 MRR`, `3 patterns cited`), and that number is directly measurable from the quarter's artifacts, override the rubric with the measurement:
   - Measured value ≥ target → **green**.
   - Measured value at 50–99% of target → **yellow**.
   - Measured value < 50% or not measurable from any shipped artifact → **red**.

## Output block shape

Appended to `_vision/VISION.md` immediately above `## Last updated`:

```markdown
## Q<n> 2026 progress (as of YYYY-MM-DD)
- [KR1.1] green — Product A hit $120 MRR in 28 days (measured: projects/product-a.md:closed)
- [KR1.2] red — Product B never shipped (project blocked at build)
- [KR1.3] yellow — median time-to-launch = 25 days, above 21-day target
- [KR2.1] green — 3 of 3 launches had clean CISO second-pass (projects/*.md)
- [KR2.2] yellow — red-team ran on 2 of 3 launches (1 waiver documented in ADR-0018)
- [KR3.1] green — avg 4.2 patterns cited per new project brief
- [KR3.2] green — REM dreaming ran after every retro
```

## Edge cases

### Mid-quarter OKR amendments

If an OKR was amended mid-quarter (via an ADR + `history/` entry), roll up **against the most recent definition**. The `history/` trail preserves the original — roll-up reflects what the agency was actually steering toward at close.

### Spanning-quarter projects

A project that opened in Q1 and closed in Q2 counts toward **Q2 roll-up only**. In-flight scoring happens during its active quarter (red flags surface in Q1's roll-up as "in-flight"), but the final score is Q2's.

### No shipped projects this quarter

Workspace KR defaults to **red (no evidence)**. The retro surfaces this prominently — a quarter with no shipped projects is itself a roll-up signal.

### KR not traceable to any project

If a workspace KR has zero `_traces_` references across all projects this quarter, mark it **red (not attempted)** and flag for the next user meeting as "retire or re-scope."

## Idempotence

- Running `okr.rollup` twice for the same quarter overwrites only the `## Q<n> progress` block. Everything else in `VISION.md` is preserved.
- The `history/` entry is append-only — a second run appends a new dated entry with the same content; do not dedupe (this is an audit trail).

## Never

- Retire an OKR automatically. (User decision, next meeting.)
- Score a KR green without a measurable claim when the KR carries a number.
- Roll up an in-flight project's partial scores as if it were closed.
- Omit the quantitative override — always measure where measurable.
