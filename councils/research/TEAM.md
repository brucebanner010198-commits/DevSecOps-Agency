# `research` council — TEAM

> Living team card. Updated whenever the roster changes. Paired with [`AGENTS.md`](./AGENTS.md) which declares the council's contract.

## Remit

Market, technology, literature, user — wedge declaration, build/don't-build verdict.

## Convened when

Every new project idea; before product strategy; pivots.

## Lead

- **`cro`** — sonnet — Chief Research Officer — the Chief who runs the Research Council.

## Specialists

| Agent | Tier | Purpose |
| --- | --- | --- |
| `market-researcher` | `haiku` | CRO needs a quick market scan for the idea — audience size, direct competitors, unmet niches. |
| `tech-scout` | `haiku` | CRO needs a scan of the current technical landscape — standard stacks, libraries, patterns, and known-broken paths for the problem domain. |
| `literature-reviewer` | `haiku` | CRO needs prior-art surfaced — past attempts, public post-mortems, design patterns, and known failure modes for this kind of project. |
| `user-researcher` | `haiku` | PM Lead needs personas and jobs-to-be-done derived from a project intake. |

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
