# `architecture` council — TEAM

> Living team card. Updated whenever the roster changes. Paired with [`AGENTS.md`](./AGENTS.md) which declares the council's contract.

## Remit

System shape before subsystem build — components, data flow, trust boundaries, tech-stack choice.

## Convened when

Every project after research+product strategy; shared lead with execution.

## Lead

- **`engineering-lead`** — sonnet — Use this agent for the Architecture and Build phases of a DevSecOps Agency project.

## Specialists

| Agent | Tier | Purpose |
| --- | --- | --- |
| `system-architect` | `haiku` | CTO (engineering-lead) needs the top-level system architecture — components, data flow, trust boundaries — before subsystem design begins. |
| `api-designer` | `haiku` | Engineering Lead needs the API surface designed — endpoints, request/response schemas, auth requirements, and error codes — derived from the functional spec and threat model. |
| `data-architect` | `haiku` | CTO (engineering-lead) needs the data model — entities, relationships, indexes, retention, PII classification. |
| `infra-architect` | `haiku` | CTO (engineering-lead) needs the infrastructure shape — where things run, how they scale, what the dependency surface looks like — tuned to the chosen deployment target. |

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
