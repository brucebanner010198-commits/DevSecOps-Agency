# `product` council — TEAM

> Living team card. Updated whenever the roster changes. Paired with [`AGENTS.md`](./AGENTS.md) which declares the council's contract.

## Remit

Strategy, Now/Next/Later/Never roadmap, acceptance criteria that QA can test.

## Convened when

Every project after research; updates at each phase gate.

## Lead

- **`pm-lead`** — sonnet — Use this agent for the Product Management phase of a DevSecOps Agency project.

## Specialists

| Agent | Tier | Purpose |
| --- | --- | --- |
| `spec-writer` | `haiku` | PM Lead needs a functional specification with testable acceptance criteria and measurable success metrics derived from the brief and personas. |
| `product-strategist` | `haiku` | CPO (pm-lead) needs a crisp strategic framing — positioning, wedge, what to cut, what to keep — before the spec is written. |
| `roadmap-planner` | `haiku` | CPO (pm-lead) needs a phased roadmap — v1 scope crystallised and v2+ parked with reasons. |

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
