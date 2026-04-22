---
name: fanout
description: >
  Internal skill. Defines the worker tier — Chief → Specialist → Worker — used
  when a task decomposes cleanly along a dimension (per-file, per-endpoint,
  per-dep, per-table, per-agent-file). Declares the `workers:` frontmatter
  convention, the default depth cap (three levels; deeper requires an ADR),
  parallelism policy, deterministic ordering, and the aggregation contract.
  Invoked by any specialist that declares workers in its frontmatter. Pairs
  with `skills/taskflow` (state machine) — fanout is the spawn half, taskflow
  is the accounting half.
metadata:
  version: "0.3.7"
---

# fanout — the worker tier

Amazon's two-pizza rule applied recursively: when a specialist's task scales with the size of the artifact (files, endpoints, dependencies), the specialist spawns a pool of identical **workers** — one per shard — and aggregates their output back. Workers are not new agents in the roster; they are ephemeral shards of the parent specialist, carrying the parent's tool set and model tier unless overridden.

This skill gives the convention. Actual invocation is via `Task` (Claude Code's subagent tool) with a fanout wrapper that the CEO skill and the parent specialist use.

## When to fan out

Fan out **only** when the work splits along an independent, enumerable dimension AND the work per shard is small enough that serial execution wastes time.

Legal split dimensions:

- **per-file** — e.g. `license-checker` running over SBOM rows, `code-auditor` over source files
- **per-endpoint** — e.g. `pen-tester` over API routes, `a11y-auditor` over routes
- **per-dep** — e.g. `license-checker` over runtime deps
- **per-table** — e.g. `data-architect` running PII classification over schema
- **per-agent** — e.g. `agent-governance-reviewer` over `agents/**/*.md`
- **per-preprint** — e.g. `literature-reviewer` over search results
- **per-probe** — e.g. `pen-tester` over OWASP A01–A10

Do **not** fan out when shards are interdependent, when a shard's output is input to the next, or when the aggregation cost exceeds the serial cost.

## Depth cap

Default: **three levels** — `Chief → Specialist → Worker`. Workers do not spawn workers. If a domain genuinely wants a fourth level, the council **lead** files an ADR under `_decisions/ADR-NNNN-<council>-deep-fanout-<dim>.md` naming the dimension, expected shard count, parallelism cap, and aggregation strategy. CEO approves before first use.

Rationale: deeper trees make post-hoc reasoning hard and memory costs quadratic. Three levels = CEO / board-room / shop-floor. That's enough.

## Worker declaration (frontmatter)

In the parent specialist's agent file, add a `workers:` block to the frontmatter:

```yaml
---
name: license-checker
model: haiku
tools: ["Read", "Grep", "Glob"]
workers:
  - name: dep-scanner
    split: per-dep           # one shard per row in the SBOM
    max_parallel: 8          # cap concurrency
    model: haiku             # optional, inherits parent if omitted
    aggregation: union       # one of: union | majority | worst-of | tally
---
```

`split` values declare the shard dimension. `aggregation` declares how worker outputs combine.

## Parallelism policy

- **Default cap:** 8 concurrent workers per specialist. Councils may override in `councils/<c>/TEAM.md > Worker tier`.
- **Council-wide cap:** 24 concurrent workers per council across all specialists. CEO enforces via `status.json > workers.inflight`.
- **Agency-wide cap:** 64 concurrent workers total. Beyond this the parent specialist queues.

Deterministic ordering: workers receive shards in a stable sort order (alphabetical for files, ascending for numeric IDs, row order for tables). Aggregation preserves this order in the final report. Non-determinism here breaks prompt-cache hits on re-runs.

## Aggregation contracts

| `aggregation` | Semantics | Example |
| --- | --- | --- |
| `union` | concatenate findings, dedupe by key | license verdicts across deps |
| `majority` | median verdict across workers | chaos-engineer voting on ladder state |
| `worst-of` | take the most severe rung | gate roll-up |
| `tally` | count-by-label, report histogram | test pass/fail across files |

Parent specialist writes the **aggregated** artifact; worker drafts stay in a sidecar directory (`_workers/<specialist>/<shard>.md`) for traceability.

## Isolation

- Each worker runs in a fresh conversation (no shared context except what the parent specialist passes in the dispatch envelope).
- Workers share **read** access to the project workspace but write only under `_workers/<specialist>/<shard>.md`.
- Workers cannot dispatch further tasks. They return text + gates; the parent aggregates.

## Relationship to taskflow

`taskflow` defines the state machine. `fanout` adds one new legal transition: a specialist task in state `in-progress` may spawn child tasks (workers) in state `queued` → `in-progress` → `reported`. When all worker tasks reach `reported` (or one hits `escalated`), the parent specialist aggregates and transitions itself to `reported` (or `escalated`).

Worker task records live in `status.json > tasks[]` with `parent_task_id` set. The command-center renders workers as nested rows under their parent.

## Minimal example — license-checker fanning per-dep

1. `license-checker` reads the SBOM, produces a list of N deps.
2. Declares `workers: per-dep, max_parallel: 8, aggregation: union`.
3. Spawns N worker tasks, 8 at a time. Each worker reads one dep's license text, returns a `{dep, license, verdict, rationale}` row.
4. When all workers report, license-checker writes `<slug>/legal/licenses.md` with the union of verdicts, preserving dep-name ordering.
5. Gate: red if any verdict is ❌, yellow if any ⚠️, else green.

No worker spawned a sub-worker. Depth = 3 (ceo → gc → license-checker → dep-scanner). Legal under the default cap.

## Anti-patterns

- Fanning out when the shards depend on each other — this is sequential, not parallel.
- Spawning workers from a lead directly — leads dispatch specialists, never workers.
- Ad-hoc worker pools not declared in frontmatter — breaks discoverability and prompt-cache layout.
- Per-worker model upgrades (haiku → sonnet) without a rationale — justify in the worker block or use the specialist's tier.

## See also

- `skills/taskflow/SKILL.md` — task state machine
- `councils/<c>/TEAM.md > Worker tier` — per-council worker patterns
- `_decisions/ADR-NNNN-<council>-deep-fanout-<dim>.md` — deeper-than-three-level approvals
