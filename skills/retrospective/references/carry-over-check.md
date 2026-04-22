# retrospective/references/carry-over-check.md

The detector that catches "we wrote this down last time and did it again anyway."

## Why

`VALUES.md §11` says the agency learns in writing. A repeat-lesson is the agency failing to read its own ledger. This check makes repeat-lessons visible in the same turn they happen, so the CAO can red-gate the close instead of discovering the repeat a quarter later.

## Input

- Current project retro draft, section `## What we'd change`.
- Last 3 rows of `LESSONS.md`, field `what we'd change`.

Read order: current retro line vs. each prior-3 row's change bullets. N × M comparisons, where N = current bullets (≤ 3) and M = prior-3 change bullets (≤ 9 total).

## Tokenisation

Before comparing:

1. Lowercase.
2. Strip Markdown syntax (`- `, `*`, `_`, `` ` ``, backtick-fenced citations).
3. Drop citation fragments `(ADR-NNNN)`, `_meetings/...`, `:L<n>`, etc.
4. Tokenise on non-word boundaries.
5. Drop tokens in the stoplist: `the, a, an, and, or, but, to, of, for, on, at, in, by, from, we, should, would, will, could, can, might, need`.
6. Lemma-reduce agency-internal synonyms (minimal list — kept in `references/carry-over-check.md` only to make the check deterministic):
   - `specialist == agent`
   - `chief == lead`
   - `dispatch == invoke == call`
   - `bump == upgrade == tier-change` (for role changes only)
   - `add == wire == hook` (when the direct object is a skill or council)

## Comparator

Jaccard similarity `|A ∩ B| / |A ∪ B|` on token sets.

## Thresholds

| Similarity | Treatment |
| --- | --- |
| ≥ 0.80 | **Hard carry-over.** File ADR `kind: repeat-lesson`. CAO red on project close. Retro `## Carry-over check` block lists both rows verbatim with citations. |
| 0.50 – 0.79 | **Weak-positive.** Flag for CAO at next portfolio audit. Retro block lists both rows and similarity score. Not an automatic red. |
| < 0.50 | No match. Omit the pair. |

## Output

Emitted verbatim into the retro's `## Carry-over check` section:

```
## Carry-over check

- **Hard carry-over (0.83):** "Add a baseline perf run at Phase 3 entry, not Phase 4."
  - Prior: invoice-splitter (2026-04-15). `LESSONS.md > invoice-splitter:what-we'd-change:1`.
  - Now: calendar-joiner (2026-04-22). `_meetings/calendar-joiner-retro-2026-04-22.md:§What we'd change:1`.
  - Action: ADR-0047 `kind: repeat-lesson`. CAO red.
- Weak-positive (0.62): "CSRE should run tool-scout on every new MCP within 24h."
  - Prior: dorms-app-fi-a (2026-03-02). `LESSONS.md > dorms-app-fi-a:what-we'd-change:2`.
  - Now: calendar-joiner (2026-04-22). `_meetings/calendar-joiner-retro-2026-04-22.md:§What we'd change:2`.
  - Action: flagged for 2026-Q2 portfolio audit.
```

## Anti-patterns

- **Don't skip the check "because it's obviously different."** The comparator exists because humans and agents rationalise. Run the numbers.
- **Don't silently raise the 0.80 threshold to pass a close.** Threshold changes require an ADR + user consent — this is part of the Keeper Test for the skill itself.
- **Don't apply the check across all prior rows.** Only last-3. Older lessons belong in portfolio audit, not per-project retro.
- **Don't lemmatise past the published synonym list.** Over-lemmatisation hides distinct problems. If a new synonym needs adding, file an ADR.

## Bootstrap

Until `LESSONS.md` has 3 shipped-project rows, the check emits `"No carry-over check — ledger has < 3 rows."` The wave-retros and first 3 project-close retros skip the check but still emit the section with that line.
