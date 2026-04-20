# Command Center — panel specifications (v0.2)

## 1. Header strip

```
[ DevSecOps Agency · invoice-splitter ] [ phase: design ] [ 0 blockers ] [ updated 12s ago ]
```

Chip colors: `phase` blue (active) / green (delivered) / red (blocked); `blockers` red when > 0.

## 2. Organisation

A CEO node at the top, followed by 9 council cards in a 3-column grid.

```
                                ┌────────────────┐
                                │      CEO       │
                                │ single voice   │
                                └───────┬────────┘
      ┌─────────┬────────────┬─────────┼─────────┬─────────┬────────┬───────┐
      │         │            │         │         │         │        │       │
      ▼         ▼            ▼         ▼         ▼         ▼        ▼       ▼
   Research  Product  Architecture Security Execution Quality DevOps Docs  Legal
   (cro)    (pm-lead) (eng-lead) (sec-lead)(eng-lead)(qa-lead)(dev-l)(doc-l)(gc)
```

Each council card shows:
- Council label + Chief title (e.g., "CRO · Research")
- Lead agent name with tint matching the council function
- Specialist list — active ones pulse green

## 3. Phases

7-card horizontal strip:

```
[Phase 1 Discovery] [Phase 2 Design] [Phase 3 Build] [Phase 4 Verify] [Phase 5 Ship] [Phase 6 Document+Legal] [Phase 7 Close]
```

States: `pending` (grey border) · `in progress` (blue border + glow) · `blocked` (red border) · `done` (green border).

## 4. Meeting log

Scrollable, newest on top. Filter buttons: **All · Board · Council**.

Row format:
```
[HH:MM:SS]  [type]  from → to  [gate]  note · artifacts
```

Board entries have a blue left border; council entries have a subtle grey left border and lower background opacity.

Type badges:
| Badge              | Color       |
| ------------------ | ----------- |
| dispatch           | cyan        |
| report             | green       |
| handoff            | blue        |
| board-decision     | purple      |
| fix-loop           | orange      |
| escalate           | red         |
| resume             | green       |

Gate chips (when `m.gate` present): green / yellow / red.

## 5. Inbox + Artifacts

**Inbox** — open questions with red border at top. Each shows: raiser, stage, question text, options (if any), age. Resolved questions collapsed below with a small `→ answer` line.

**Artifacts** — linkable list of every file in `status.artifacts`. Click opens via `computer://` link.

## Data contract — status.json.team

For v0.2, use these council keys:

```json
{
  "team": {
    "research":     { "lead": "cro",              "specialists": ["market-researcher","tech-scout","literature-reviewer","user-researcher"] },
    "product":      { "lead": "pm-lead",          "specialists": ["spec-writer","product-strategist","roadmap-planner"] },
    "architecture": { "lead": "engineering-lead", "specialists": ["system-architect","api-designer","data-architect","infra-architect"] },
    "security":     { "lead": "security-lead",    "specialists": ["threat-modeler","code-auditor","pen-tester","compliance-officer"] },
    "execution":    { "lead": "engineering-lead", "specialists": ["backend-dev","frontend-dev","db-engineer","integrations-engineer"] },
    "quality":      { "lead": "qa-lead",          "specialists": ["test-designer","test-runner","performance-tester","a11y-auditor"] },
    "devops":       { "lead": "devops-lead",      "specialists": ["ci-engineer","deployment-engineer","observability-engineer"] },
    "docs":         { "lead": "docs-lead",        "specialists": ["api-documenter","readme-writer","tutorial-writer"] },
    "legal":        { "lead": "gc",               "specialists": ["license-checker","privacy-counsel"] }
  },
  "activeAgents": ["engineering-lead","system-architect"]
}
```

The renderer falls back to the v0.1 key shape (`team.pm / team.security / team.engineering / team.qa / team.devops / team.docs`) if the new keys are absent.
