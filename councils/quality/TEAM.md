# `quality` council — TEAM

> Living team card. Updated whenever the roster changes. Paired with [`AGENTS.md`](./AGENTS.md) which declares the council's contract.

## Remit

Unit + integration + e2e, p50/p95/p99 perf, a11y axe-core + WCAG AA, threat-model mitigation tests.

## Convened when

Every project pre-release.

## Lead

- **`qa-lead`** — sonnet — Use this agent for the Quality Assurance phase of a DevSecOps Agency project.

## Specialists

| Agent | Tier | Purpose |
| --- | --- | --- |
| `test-designer` | `haiku` | QA Lead needs a test matrix derived from the acceptance criteria — what to test, at what level (unit/integration/e2e), and the priority order. |
| `test-runner` | `haiku` | QA Lead needs the test matrix implemented as actual tests and executed, with a per-criterion pass/fail report. |
| `performance-tester` | `haiku` | CQO (qa-lead) needs a basic performance probe — load test on the hot paths, p95 latency measurement, and a N+1 query check. |
| `a11y-auditor` | `haiku` | CQO (qa-lead) needs an accessibility check against WCAG 2. |

## Worker tier

Specialists may, when a task decomposes cleanly along a dimension (per-file, per-table, per-endpoint, per-dependency), spawn **workers** — a third tier below specialist. Workers inherit the parent specialist's tool set and model tier unless overridden. Default depth cap is three levels (Chief → Specialist → Worker); deeper fanout requires an ADR from the lead.

Worker declaration lives in the parent specialist's frontmatter:

```yaml
workers:
  - name: <slug>
    split: <dimension>    # e.g. per-file, per-endpoint, per-dep
    max_parallel: 8       # per-council cap, overrides optional
```

Fanout + aggregation is handled by `skills/fanout/` (see root README).

This council declares no worker patterns in v0.3.7. Extend here when one emerges.

## Council norms

The council's must / must-not contract is authoritative in [`AGENTS.md`](./AGENTS.md). This file only records who currently staffs the council.
