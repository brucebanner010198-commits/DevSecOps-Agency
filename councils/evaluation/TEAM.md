# `evaluation` council — TEAM

> Living team card. Updated whenever the roster changes. Paired with [`AGENTS.md`](./AGENTS.md) which declares the council's contract.

## Remit

Eval sets, benchmarks, regression detection, variance-gated skill evaluation, FinOps, token hygiene.

## Convened when

Every project pre-release; standing weekly FinOps; every new/changed skill.

## Lead

- **`evaluation-lead`** — sonnet — Chief Evaluation Officer (CEVO) — the Chief who runs the Evaluation Council.

## Specialists

| Agent | Tier | Purpose |
| --- | --- | --- |
| `eval-designer` | `haiku` | Use this agent to design an eval set from a project's OKRs + brief + shipped artifacts. |
| `benchmark-runner` | `haiku` | Use this agent to execute an eval set or external benchmark harness against a project's shipped artifacts. |
| `regression-detector` | `haiku` | Use this agent to detect cross-project eval regressions — agency-wide quality drift. |
| `budget-monitor` | `haiku` | Use this agent to track token + dollar burn against a project's declared budget and surface overruns early. |
| `token-compactor` | `haiku` | Use this agent to compress redundant session-log and chat. |
| `finops-analyst` | `sonnet` | Evaluation council needs cost attribution work — 4-column × 3-dim token tracking, weekly FinOps report generation, anomaly triage (span > $1, trace > $10, runaway thresholds), p... |
| `skill-evaluator` | `sonnet` | A new or changed skill needs evaluation evidence before it lands in the plugin, when a skill's behavior has drifted and needs benchmarking, or when CEVO needs variance-analyzed ... |

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
