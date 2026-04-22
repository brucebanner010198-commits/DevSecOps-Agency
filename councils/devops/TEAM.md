# `devops` council — TEAM

> Living team card. Updated whenever the roster changes. Paired with [`AGENTS.md`](./AGENTS.md) which declares the council's contract.

## Remit

CI, containerisation, deploy manifests, health endpoints, structured logs, one-command rollback.

## Convened when

Every project that ships a runtime.

## Lead

- **`devops-lead`** — sonnet — Use this agent for the DevOps phase of a DevSecOps Agency project.

## Specialists

| Agent | Tier | Purpose |
| --- | --- | --- |
| `ci-engineer` | `haiku` | DevOps Lead needs a CI workflow that lints, runs the test suite, runs an SCA security scan, and gates merges on results. |
| `deployment-engineer` | `haiku` | DevOps Lead needs a container/IaC, deploy checklist, and rollback plan tuned to the chosen deployment target. |
| `observability-engineer` | `haiku` | VP-Ops (devops-lead) needs the observability baseline wired up — structured logs, health endpoint, basic metrics, and an alert policy stub. |

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
