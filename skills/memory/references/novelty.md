# novelty.md — conditional-write gate

Skip memory writes that add no new information. Every tier runs this gate before persisting.

## Knobs

| Knob                     | Light | Deep  | REM   |
| ------------------------ | ----- | ----- | ----- |
| `dedupe_similarity`      | 0.85  | 0.85  | 0.85  |
| `min_new_bullets`        | 1     | 2     | 3     |
| `corpus_lookback_days`   | 7     | ∞     | ∞     |
| `max_candidate_bullets`  | 7     | n/a   | 12    |

Knobs live here, not in the SKILL.md body. Override only with a cited reason in the project's `status.json > memory` section.

## Tokenisation

- Lowercase.
- Strip punctuation except `-` (hyphen preserves compound tokens: `csrf-double-submit`).
- Split on whitespace.
- Drop stopwords from `_memory/stopwords.txt` if present; otherwise use the built-in list: the, a, an, and, or, of, to, in, for, is, are, was, were, be, with, on, by.
- Keep acronyms uppercase in the bullet text, lowercase only for the similarity comparison.

## Jaccard similarity

```
sim(a, b) = |tokens(a) ∩ tokens(b)| / |tokens(a) ∪ tokens(b)|
```

- `sim ≥ dedupe_similarity` → candidate is a duplicate; drop it.
- `sim < dedupe_similarity` → candidate is novel; include it in the write set.
- Ties: include the candidate with more specific citations.

## Worked examples

### Example 1 — Light, clear duplicate

Existing: `- [pattern] Stripe webhook replay requires idempotency key in custom metadata (security/pentest-report.md:42)`

Candidate: `- [pattern] Stripe webhooks need idempotency keys in custom metadata`

Tokens overlap on: stripe, webhook(s), idempotency, key(s), custom, metadata. Jaccard ≈ 0.88 → drop.

### Example 2 — Light, near-miss that should pass

Existing: `- [risk] Stripe charge-off dispute window is 120 days, not 60`

Candidate: `- [pattern] Stripe webhook replay requires idempotency key in custom metadata`

Tokens overlap on: stripe. Jaccard ≈ 0.10 → write.

### Example 3 — Deep, entire section duplicate

Candidate Deep pattern for project `invoice-splitter-v2` with an existing `patterns/invoice-splitter.md`:

- Compare section by section.
- If **≥ 4 of 5 sections** fail novelty (each section's bullets collectively), the whole write is aborted; log note `skipped — overlaps patterns/invoice-splitter.md`.
- If **< 4 of 5 sections** fail, write the full new file; citation inside keeps traceability.

### Example 4 — REM, small corpus

With `|MEMORY.md bullets| < 10`, treat every candidate as novel unless `sim ≥ 0.95` (very strict). Rationale: early-stage memory should accumulate fast.

## When to tune knobs

- Raise `dedupe_similarity` to 0.90 if memory is pruning real novelty (false positives).
- Lower `min_new_bullets` to 0 only for a one-off corpus bootstrap, never in steady state.
- Shrink `corpus_lookback_days` for Light if the agency is running a very high project volume (daily files get very long).

Every tuning event appends to `_memory/index.json > knobHistory[]`. Never edit a prior entry.
