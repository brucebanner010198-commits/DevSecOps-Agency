---
name: market-intel
description: >
  This skill should be used when any agent (CRO, CSO, or their specialists)
  needs to produce or consume market-intelligence artifacts with a
  consistent schema across the workspace. Standardises the shape of
  `research/market.md` (per-project, shallow) and `_vision/strategy/*.md`
  (portfolio, deep) so downstream agents (product-strategist,
  opportunity-ranker, CMO) can parse them deterministically. Trigger
  phrases: "market-intel format", "standardise this market analysis",
  "check market-intel schema", or internal invocation by cro / cso when
  dispatching market-researcher / market-sizer / competitive-analyst /
  trend-scout.
metadata:
  version: "0.3.0-alpha.2"
---

# market-intel — shared shape for all market-intelligence artifacts

Every market artifact in the workspace uses one of three canonical shapes. Downstream agents parse them by section header, so headers are normative, not suggestive.

## Canonical shapes

### Shape A — per-project wedge scan (CRO council)

Produced by `market-researcher`. File: `<slug>/research/market.md`.

Fixed sections (in this order):

1. `# Market — <project>`
2. `## Who wants this (and why)` — 1 paragraph
3. `## Direct competitors` — table: Product · Strength · Weakness · Why user might leave
4. `## Indirect alternatives` — 1 paragraph
5. `## Wedge` — 1 sentence
6. `## Non-target users` — bullets

### Shape B — portfolio market sizes (CSO council)

Produced by `market-sizer`. File: `_vision/strategy/market-sizes.md`.

Fixed sections:

1. `# Market Sizes — <YYYY-MM-DD>`
2. `## Method` — bullets: TAM · SAM · SOM method
3. `## Sizing table` — table: Candidate · TAM · SAM · SOM (3y) · Confidence · Basis
4. `## Low-confidence candidates` — bullets with "what evidence would raise"
5. `## High-confidence candidates` — bullets with citations

### Shape C — portfolio competitive map (CSO council)

Produced by `competitive-analyst`. File: `_vision/strategy/competitive-map.md`.

Fixed sections:

1. `# Competitive Map — <YYYY-MM-DD>`
2. `## Current markets (where we've shipped)` — table with defensibility column
3. `## Candidate markets (from shortlist)` — table
4. `## Notable moves (delta since last map)` — bullets
5. `## Retired competitors` — bullets
6. `## Flags for cso` — bullets

## Shared rules

- Every number cites a basis. Blank basis = material defect.
- Confidence always L/M/H — no 1-5 scales in market-intel (that's idea-pipeline's rubric domain).
- Every competitor named requires a source: URL, prior `_memory/patterns/*.md:<line>`, or `[user-knowledge]` tag.
- `[synthesised]` / `[hypothesis]` / `[user-knowledge]` tags used for non-cited claims — never leave uncited claims unflagged.
- Deterministic ordering inside tables: alphabetical by first column.

## Reader expectations

Downstream consumers (product-strategist, opportunity-ranker, CMO, CEO) parse by:

- `## Direct competitors` table columns → opportunity-ranker's defensibility axis
- `## Sizing table > SOM (3y)` → opportunity-ranker's Reach axis
- `## Wedge` → positioning-strategist's wedge seed
- `## Notable moves` → thesis-keeper drift check (Wave 3+)

If a section header is missing or renamed, the reader emits a parse error and sends back to the producer. No graceful degradation.

## Versioning

- Shapes A/B/C are `market-intel@0.3` — any column addition is a minor bump; any section removal is a major bump (breaks downstream readers).
- Old market artifacts from pre-v0.3 stay valid — readers fall back to the pre-v0.3 shape if they detect no `market-intel` version comment.

## Progressive disclosure

- `references/table-schemas.md` — exact column definitions, cell types, required vs optional
- `references/citation-rules.md` — what counts as a citation, when to use `[synthesised]` vs `[hypothesis]` vs `[user-knowledge]`
