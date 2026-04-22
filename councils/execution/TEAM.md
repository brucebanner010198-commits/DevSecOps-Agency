# `execution` council — TEAM

> Living team card. Updated whenever the roster changes. Paired with [`AGENTS.md`](./AGENTS.md) which declares the council's contract.

## Remit

Implementation against approved architecture + threat model. Parameterised queries, idempotent migrations, input validation.

## Convened when

Every project after architecture + security first-pass (shared lead with architecture).

## Lead

- **`engineering-lead`** — sonnet — Use this agent for the Architecture and Build phases of a DevSecOps Agency project. (*shared with architecture — lives at `agents/architecture/engineering-lead.md`*)

## Specialists

| Agent | Tier | Purpose |
| --- | --- | --- |
| `backend-dev` | `haiku` | Engineering Lead needs server-side code implemented from the architecture document — endpoints, business logic, data access, and integrations. |
| `frontend-dev` | `haiku` | Engineering Lead needs client-side code implemented from the architecture document — UI, state management, API integration, and accessibility. |
| `db-engineer` | `haiku` | VP-Eng (engineering-lead) needs database code — migrations, seed scripts, repository/query layer — matching the data-architect's design. |
| `integrations-engineer` | `haiku` | VP-Eng (engineering-lead) needs third-party integrations wired up — auth providers, payment, email, object storage, external APIs. |

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
