# market-intel — table schemas

Exact column definitions. No variant headers allowed.

## Shape A — Direct competitors (per-project)

File: `<slug>/research/market.md > ## Direct competitors`

| Column | Type | Required | Notes |
| --- | --- | --- | --- |
| Product | string | yes | Real product or `[internal-only]` |
| Strength | string (≤ 80 chars) | yes | One capability they do well |
| Weakness | string (≤ 80 chars) | yes | One visible gap |
| Why user might leave | string (≤ 120 chars) | yes | Our wedge against them |

Rows alphabetised by Product. Max 10 rows — if more, group by segment.

## Shape B — Sizing table (portfolio)

File: `_vision/strategy/market-sizes.md > ## Sizing table`

| Column | Type | Required | Notes |
| --- | --- | --- | --- |
| Candidate | string | yes | Idea slug or market name |
| TAM | dollar range | yes | Format `$X-Y<B/M>` |
| SAM | dollar range | yes | Same format |
| SOM (3y) | dollar range | yes | Same format |
| Confidence | enum L/M/H | yes | No numeric |
| Basis | string | yes | Source reference |

Rows alphabetised by Candidate. Max 20 rows.

## Shape C — Current markets (portfolio)

File: `_vision/strategy/competitive-map.md > ## Current markets`

| Column | Type | Required | Notes |
| --- | --- | --- | --- |
| Market | string | yes | Market label matching VISION |
| Our position | enum (leader · challenger · niche · exiting) | yes | Stated rationale in adjacent cell? no — separate line under table |
| Top 3 competitors | string | yes | Comma-separated |
| Moves since last map | string (≤ 100 chars) | yes | Deltas only; "none" is valid |
| Our defensibility (1-5) | int | yes | Scale from `opportunity-ranker` rubric |

Rows alphabetised by Market. No row limit — but flag if > 10.

## Shape C (continued) — Candidate markets

File: `_vision/strategy/competitive-map.md > ## Candidate markets`

| Column | Type | Required | Notes |
| --- | --- | --- | --- |
| Market | string | yes | From shortlist |
| Incumbent | string | yes | Dominant player or `[fragmented]` |
| Gap we'd enter | string (≤ 100 chars) | yes | Wedge hypothesis |
| Incumbent mood | enum (quiet · active · aggressive) | yes | Mood inferred from Moves-since-last-map |

## Cell type definitions

- **string**: plain text, no pipe characters (escape as `\|`)
- **dollar range**: `$X-Y<suffix>` where suffix ∈ {K, M, B} or blank for unitless
- **enum**: exact match from the stated set — no synonyms
- **int**: integer 1-5

## Parse errors

Reader emits parse error and sends back to producer if:

- Column count mismatch
- Column header not in canonical list
- Required column blank
- Enum value not in allowed set
- Number outside scale
- Row count exceeds the stated max without a "split for readability" comment above the table
