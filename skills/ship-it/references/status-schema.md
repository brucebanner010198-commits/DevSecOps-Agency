# status.json schema

Two shapes are supported. v0.2 is the default (9 councils, 7 phases, CEO orchestration). v0.1 (6 departments, 10 stages) still renders via a fallback in the command-center.

## v0.2 (recommended)

```json
{
  "schemaVersion": "0.2",
  "projectSlug": "invoice-splitter",
  "projectIdea": "a secure invoice-splitting web app for roommates",
  "createdAt": "<iso>",
  "lastUpdated": "<iso>",
  "phase": "discovery | design | build | verify | ship | document-legal | close | delivered | blocked",
  "completed": ["discovery"],
  "activeAgents": ["engineering-lead", "system-architect"],
  "team": {
    "research":     {"lead": "cro",              "specialists": ["market-researcher","tech-scout","literature-reviewer","user-researcher"]},
    "product":      {"lead": "pm-lead",          "specialists": ["spec-writer","product-strategist","roadmap-planner"]},
    "architecture": {"lead": "engineering-lead", "specialists": ["system-architect","api-designer","data-architect","infra-architect"]},
    "security":     {"lead": "security-lead",    "specialists": ["threat-modeler","code-auditor","pen-tester","compliance-officer"]},
    "execution":    {"lead": "engineering-lead", "specialists": ["backend-dev","frontend-dev","db-engineer","integrations-engineer"]},
    "quality":      {"lead": "qa-lead",          "specialists": ["test-designer","test-runner","performance-tester","a11y-auditor"]},
    "devops":       {"lead": "devops-lead",      "specialists": ["ci-engineer","deployment-engineer","observability-engineer"]},
    "docs":         {"lead": "docs-lead",        "specialists": ["api-documenter","readme-writer","tutorial-writer"]},
    "legal":        {"lead": "gc",               "specialists": ["license-checker","privacy-counsel"]}
  },
  "artifacts": {
    "brief":         "brief.md",
    "researchBrief": "research-brief.md",
    "productStrategy": "product/strategy.md",
    "productRoadmap":  "product/roadmap.md",
    "architecture":  "architecture.md",
    "dataModel":     "architecture/data-model.md",
    "infra":         "architecture/infra.md",
    "threatModel":   "threat-model.md",
    "compliance":    "security/compliance.md",
    "srcDir":        "src/",
    "testsDir":      "tests/",
    "qaReport":      "qa-report.md",
    "perfReport":    "qa/perf-report.md",
    "a11yReport":    "qa/a11y-report.md",
    "codeAudit":     "security/code-audit.md",
    "pentestReport": "security/pentest-report.md",
    "deployDir":     "deploy/",
    "observability": "deploy/observability.md",
    "docsDir":       "docs/",
    "tutorial":      "docs/tutorial/getting-started.md",
    "licenses":      "legal/licenses.md",
    "privacy":       "legal/privacy.md"
  },
  "blockers": [],
  "commandCenterArtifactId": null,
  "metrics": {
    "boardMeetings": 4,
    "councilMeetings": 18,
    "fixLoops": 1,
    "escalations": 0
  }
}
```

## v0.1 (legacy — still supported)

```json
{
  "projectSlug": "invoice-splitter",
  "projectIdea": "a secure invoice-splitting web app for roommates",
  "createdAt": "<iso>",
  "lastUpdated": "<iso>",
  "phase": "pm | security | architecture | build | qa | security2 | devops | docs | delivered | blocked",
  "completed": ["intake", "pm"],
  "activeAgents": ["security-lead", "threat-modeler"],
  "team": {
    "pm":          {"lead": "pm-lead",          "specialists": ["user-researcher", "spec-writer"]},
    "security":    {"lead": "security-lead",    "specialists": ["threat-modeler", "code-auditor"]},
    "engineering": {"lead": "engineering-lead", "specialists": ["api-designer", "backend-dev", "frontend-dev"]},
    "qa":          {"lead": "qa-lead",          "specialists": ["test-designer", "test-runner"]},
    "devops":      {"lead": "devops-lead",      "specialists": ["ci-engineer", "deployment-engineer"]},
    "docs":        {"lead": "docs-lead",        "specialists": ["api-documenter", "readme-writer"]}
  },
  "artifacts": { "...": "..." },
  "blockers": [],
  "metrics": { "handoffs": 12, "fixLoops": 1, "escalations": 0 }
}
```

## chat.jsonl schema (v0.2)

One JSON object per line. New fields: `scope`, `council`, `gate`, `artifacts` (array):

```json
{"ts":"<iso>","scope":"board","from":"ceo","to":"cro","type":"dispatch","phase":"discovery","note":"run the research council"}
{"ts":"<iso>","scope":"board","from":"cro","to":"ceo","type":"report","phase":"discovery","gate":"green","artifacts":["research-brief.md"],"note":"wedge: dorms"}
{"ts":"<iso>","scope":"council","council":"research","from":"cro","to":"market-researcher","type":"dispatch","artifact":"research/market.md"}
```

`type` vocabulary: `dispatch · report · handoff · board-decision · fix-loop · escalate · resume`.
`gate` vocabulary: `green · yellow · red · n/a`.
`scope` vocabulary: `board · council`.

## inbox.json schema

See `escalation-rules.md`. Unchanged between v0.1 and v0.2.
