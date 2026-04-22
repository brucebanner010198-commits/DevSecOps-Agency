# `sre` council — TEAM

> Living team card. Updated whenever the roster changes. Paired with [`AGENTS.md`](./AGENTS.md) which declares the council's contract.

## Remit

MCP registry + vetting, a2a adapters, sandboxed tool exec, model-routing failover, OTel-GenAI telemetry, prompt-cache tuning.

## Convened when

Every project that ships a runtime; every MCP adoption; ongoing observability.

## Lead

- **`sre-lead`** — sonnet — Chief Site Reliability Officer (CSRE) — the Chief who runs the SRE Council.

## Specialists

| Agent | Tier | Purpose |
| --- | --- | --- |
| `mcp-registry-scout` | `haiku` | SRE Council specialist. |
| `a2a-adapter` | `haiku` | SRE Council specialist. |
| `sandbox-runner` | `haiku` | SRE Council specialist. |
| `model-routing-override` | `haiku` | SRE Council specialist. |
| `agent-telemetry-engineer` | `sonnet` | SRE council needs OTel-GenAI instrumentation wired for agent-level telemetry — trace-id propagation in dispatch envelopes, per-span attributes (gen_ai. |
| `mcp-author` | `sonnet` | Agency needs to BUILD an MCP (Model Context Protocol) server — exposing internal capabilities to external agents, wrapping a third-party API behind MCP, or shipping a draft MCP ... |
| `prompt-cache-tuner` | `sonnet` | SRE council needs to design, tune, or remediate Anthropic prompt-cache breakpoints for a project — canonical 4-breakpoint assembly, post-Feb-2026 5-min TTL strategy, workspace-i... |

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
