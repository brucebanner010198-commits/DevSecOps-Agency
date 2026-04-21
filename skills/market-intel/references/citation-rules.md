# market-intel — citation rules

Uncited numbers are the #1 source of bad decisions. These rules are strict.

## What counts as a citation

In descending preference:

1. **External authoritative source**: URL to statistical body (census, industry association), regulator, financial filing, peer-reviewed paper. Must be ≤ 5 years old unless foundational.
2. **Primary research**: `research/interviews/*.md:<line>` or `research/usage-test-*.md:<line>` from the current or a prior project.
3. **Memory pattern**: `_memory/patterns/<slug>.md:<line>` — cite the specific line, not the file.
4. **Industry report (non-peer-reviewed)**: named analyst firm + report title + year. Flag as `[analyst-report]` — lower trust.
5. **User knowledge**: user told us this in a meeting. Cite as `_meetings/<date>-user-<slug>.md:<line>` and tag `[user-knowledge]`.
6. **Prior shipped project**: `_memory/patterns/<slug>.md` + cite the specific measured outcome.

## What does NOT count as a citation

- "Industry standard" with no source
- "Commonly known" with no source
- Another agent's synthesis without the upstream source it was based on
- A vendor's marketing page (use only for product features, never for market size)
- Speculation tagged as citation

## When a number cannot be cited

Use one of these explicit tags:

- `[synthesised]` — this number is derived by reasoning from cited primitives. Show the derivation.
- `[hypothesis]` — this is our best guess; we have no evidence. Use sparingly; flag as a risk.
- `[unknown]` — we have no basis. The number is blank; this tag appears in its place.
- `[user-knowledge]` — the user told us, no external citation. Tagged + sourced to meeting minutes.

Never leave a number bare. Bare numbers are treated as `[hypothesis]` at read time, and that's a yellow signal at minimum.

## Citation format examples

Good:
- `TAM $12-15B · basis: US Census 2024 · https://...`
- `retention W4 32% · basis: _memory/patterns/splitwise-clone.md:73`
- `CAC $8-12 · basis: [synthesised] from SEM rate $0.60 and conversion 6%, see market-sizes.md:42`
- `W1 churn 18% · basis: [user-knowledge], _meetings/2026-03-14-user-pricing.md:28`

Bad:
- `TAM $12B · basis: various reports`
- `W4 retention 32%` (no basis at all)
- `CAC $10 · basis: industry standard`

## Source freshness

- External statistics ≤ 5 years old; older requires `[foundational]` tag + rationale.
- Competitor moves ≤ 18 months old; older is not a "move", it's state.
- Memory patterns never expire — but flag `[stale-pattern]` if the pattern is > 2 years old and the market has moved since.

## Audit trail

Every market-intel artifact MUST end with a `## Sources` section listing every external URL + pattern reference cited in the body, deduplicated. This section is what the audit council (Wave 3) reviews.
