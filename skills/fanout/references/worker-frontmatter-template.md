# Worker frontmatter template

Paste into the parent specialist's agent frontmatter when that specialist's task naturally shards along one of the legal dimensions.

```yaml
workers:
  - name: <short-slug-describing-what-a-single-worker-does>
    split: <per-file|per-endpoint|per-dep|per-table|per-agent|per-preprint|per-probe>
    max_parallel: <1..8>
    model: <haiku|sonnet|opus>      # optional — inherits parent if omitted
    tools: ["Read", "Grep", "Glob"]  # optional — inherits parent if omitted
    aggregation: <union|majority|worst-of|tally>
    shard_from: <glob-or-artifact>   # e.g. "<slug>/legal/sbom.json[].dep" or "agents/**/*.md"
    output_row:                      # what one worker returns (one JSON row)
      - <field>: <type>
      - <field>: <type>
    envelope: |
      <free-form instructions the parent embeds when dispatching each worker>
```

Keep each worker's job small enough that it fits in a single prompt-cache window with its shard content plus the envelope (≤ 20k tokens rough ceiling).

## Sizing rule of thumb

| Shard cardinality (N) | Parallelism | Notes |
| --- | --- | --- |
| N ≤ 3 | skip fanout — serial is fine | overhead > gain |
| 4 ≤ N ≤ 8 | cap at N | one wave |
| 9 ≤ N ≤ 40 | cap at 8 | multiple waves |
| N > 40 | cap at 8 + consider split-then-aggregate | file an ADR if N > 200 |

## Naming convention

Worker names: `<specialist>-<split-short>`. Examples:

- `license-checker` → workers: `dep-scanner`
- `code-auditor` → workers: `file-auditor`
- `pen-tester` → workers: `endpoint-prober`
- `agent-governance-reviewer` → workers: `agent-scanner`

The parent specialist is the noun; the worker is a scoped verb-noun for its shard job.

## Writing the envelope

The envelope is the per-shard dispatch message. It **must** contain:

- the shard identifier (e.g., `dep: lodash@4.17.21`)
- the shard content (or a read path to it)
- the exact output schema the parent will aggregate
- the model tier and tools (for hygiene; runtime enforces)
- the deadline — workers longer than 2 minutes are killed and their shard re-dispatched

It **must not** contain:

- the parent specialist's full history
- other shards' content
- cross-shard state

This keeps workers independent and the aggregation deterministic.
