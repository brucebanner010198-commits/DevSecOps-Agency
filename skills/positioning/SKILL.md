---
name: positioning
description: >
  This skill should be used when any agent (CMO, positioning-strategist,
  CEO drafting top-5 one-pagers) needs to produce or consume a positioning
  artifact with a consistent shape. Standardises the messaging canvas
  (audience · promise · proof · wedge · category · elevator pitch) and the
  pipeline-mode narrative score rubric so opportunity-ranker can consume
  it deterministically. Trigger phrases: "positioning format",
  "messaging canvas", "elevator pitch rubric", "score narrative", or
  internal invocation by cmo when dispatching positioning-strategist.
metadata:
  version: "0.3.0-alpha.2"
---

# positioning — messaging canvas shape + narrative scoring

One file, one shape per context. Downstream consumers (CEO top-5 one-pagers, idea-pipeline ranker, landing-copy generators) parse by section.

## Canonical shape — per-project

File: `<slug>/marketing/positioning.md`. Produced by `positioning-strategist`.

Fixed sections (order matters):

1. `# Positioning — <project>`
2. `## Audience (who, one segment)` — primary + optional secondary
3. `## Promise (one line)` — measurable benefit, no hedges
4. `## Proof (≥ 2, cited)` — bulleted, each line cites source
5. `## Wedge (why us, one sentence)` — the credible narrow reason
6. `## Category` — chosen frame + alternatives considered
7. `## Elevator pitch (≤ 30 words)` — "for X who Y, our product is Z that delivers W, unlike V"
8. `## Messaging hierarchy` — H1 · H2 · 3 value props

## Canonical shape — pipeline score

Appended under `<slug>` header in `<project-or-workspace>/marketing/pipeline-readout.md`:

```markdown
### <Idea slug>
- Narrative clarity: 1–5
- Wedge strength: 1–5
- Category fit: 1–5
- Composite: avg · rounded to 0.5
- One-sentence elevator: "<≤30 words>"
```

## Rubric

### Narrative clarity (1–5)

- 5 — elevator ≤ 30 words, no jargon, category crystal clear, a non-expert gets it in one read
- 4 — elevator ≤ 30 words, minor jargon acceptable in target audience, category clear
- 3 — elevator 30–50 words, some jargon required, category needs short explainer
- 2 — elevator 50+ words or needs category education first
- 1 — cannot write a single-sentence elevator

### Wedge strength (1–5)

- 5 — wedge is a segment + capability + pricing-model flip that incumbent cannot copy in 12mo
- 4 — wedge is 2 of those 3 dimensions
- 3 — wedge is 1 dimension with visible durability
- 2 — wedge exists but incumbent can copy in 6mo
- 1 — no wedge

### Category fit (1–5)

- 5 — established category with room at the top (top 3 players all weak on our axis)
- 4 — established category, crowded, but wedge holds
- 3 — adjacent category that users will map from with one sentence
- 2 — new category that requires education but the term exists
- 1 — new category, need to coin the term

## Disallowed

- Superlatives without citation: "fastest", "best", "easiest" — unless cited to `research/market.md:<line>`
- Comparative claims naming real companies in the audience-facing positioning (different for pipeline-mode internal analysis)
- Elevator pitches > 30 words
- Missing `## Audience` section — no audience = no positioning

## Downstream parsers

- `opportunity-ranker` reads `composite` and `one-sentence elevator` from pipeline mode.
- `idea-pipeline > shortlist-template` reads `## Elevator pitch` for the top-5 one-pager card.
- `comms-writer` reads `## Messaging hierarchy > H1` as the seed for `marketing/launch-copy.md > Landing hero`.
- `brand-guardian` reads `## Category` and flags if the chosen category is already owned by a prior project with different positioning.

## Versioning

- Current: `positioning@0.3`.
- Section removal = major bump. Section reordering = major bump (readers parse positionally).

## Progressive disclosure

- `references/canvas-template.md` — filled example (per-project) + pipeline-mode example
- `references/elevator-rules.md` — 30-word checklist, worked passes and fails
