---
name: idea-pipeline
description: >
  This skill should be used when the agency needs to generate, screen, rank,
  and shortlist new product ideas for the workspace — not for a single in-flight
  project. The CEO invokes this skill on four triggers: (1) user asks "what
  should we build next"; (2) quarter roll-up shows slack capacity; (3) REM
  dreaming surfaces ≥ 2 adjacent-market opportunities; (4) an active project
  closes and no successor is queued. Runs a 4-stage gated pipeline from raw
  ideas → screened → ranked → top-5. Top-5 feeds directly into the
  `user-meeting` skill. Trigger phrases: "what should we build next",
  "refresh the idea pipeline", "run the opportunity pipeline", "top-5 ideas
  for review", "pipeline readout".
metadata:
  version: "0.3.0-alpha.2"
---

# idea-pipeline — portfolio ideation flow

4-stage gated pipeline owned by the CEO with CSO + CMO councils doing the work. Output is the shortlist that powers the top-5 user-meeting.

## When to invoke

| Trigger | Where | Who invokes |
| ------- | ----- | ----------- |
| User asks "what next" | CEO chat | CEO |
| Quarter roll-up: slack capacity ≥ 1 project | `_vision/strategy/thesis-review-<q>.md` | CEO |
| REM dreaming: ≥ 2 adjacent-market signals | `_memory/MEMORY.md > ## Open questions` | CEO |
| Project closes with empty backlog | Phase 7 retro | CEO |

## Pipeline stages

### Stage 1 — Ideation (divergent)

- CSO dispatches `trend-scout` + `competitive-analyst` — emerging signals + moving competitors.
- CEO + `skill-creator` (optional) surface org-level strategic bets.
- User-suggested ideas injected here from inbox.
- Output: raw list of ≥ 15, ≤ 40 candidates in `_vision/strategy/_pipeline/raw-<date>.md`.

### Stage 2 — Screening (convergent to ~10)

- Apply screen filters (see `references/screening-filters.md`):
  - Legal feasibility (kill list for regulatory showstoppers)
  - Mission fit (≥ 1 link to `_vision/VISION.md > ## Mission` or flagged `[mission-stretch]`)
  - Existing-incumbent moat check (unless clear wedge)
  - Stack adjacency (reuses ≥ 1 proven-stack capability)
- Output: ≤ 10 screened candidates in `_vision/strategy/_pipeline/screened-<date>.md`.

### Stage 3 — Deep ranking (ranked ≤ 10)

- CSO dispatches `market-sizer` + `opportunity-ranker` — TAM/SAM/SOM + RICE scoring.
- CMO dispatches `positioning-strategist` + `comms-writer` + `growth-analyst` in pipeline-mode — narrative + growth potential scores.
- `opportunity-ranker` merges scores per `references/ranking-matrix.md`.
- Output: `_vision/strategy/opportunity-scorecard.md` + `_vision/strategy/_pipeline/pipeline-readout.md`.

### Stage 4 — Top-5 shortlist

- `opportunity-ranker` recommends top-5.
- CEO reviews. May override with reason (captured as ADR).
- Final top-5 written to `_vision/strategy/_pipeline/top-5.md` with one-page-per-idea format (see `references/shortlist-template.md`).
- Hands off to `user-meeting` skill.

## Gate flow

- Stage 1 → 2: ≥ 15 candidates, trend-radar + competitive-map both present.
- Stage 2 → 3: ≤ 10 survivors, ≥ 1 kill list reason for every drop.
- Stage 3 → 4: composite scores computed for all, ≥ 3 with composite ≥ 3.5.
- Stage 4 → user-meeting: top-5 one-pagers written, ADR filed if CEO overrode ranker.

## ADR triggers

- CEO overrides `opportunity-ranker` top-5 → ADR (category: pivot-class).
- Screening kills an existing-thesis candidate → ADR (category: thesis retirement).
- Idea admitted despite failing mission-fit screen → ADR with `[mission-stretch]` rationale.

## Meeting-minutes triggers

- Stage 4 → user-meeting handoff is a `user` meeting kind → minutes required.
- CEO override = material decision, captured both as ADR and in the user-meeting minutes.

## Artifacts

```
_vision/strategy/
├── trend-radar.md
├── competitive-map.md
├── market-sizes.md
├── opportunity-scorecard.md
└── _pipeline/
    ├── raw-<date>.md
    ├── screened-<date>.md
    ├── pipeline-readout.md
    └── top-5.md
```

## Progressive disclosure

- `references/screening-filters.md` — stage-2 filter definitions + kill list rules
- `references/ranking-matrix.md` — RICE + narrative weighting formulas, tie-break order
- `references/shortlist-template.md` — top-5 one-pager skeleton
