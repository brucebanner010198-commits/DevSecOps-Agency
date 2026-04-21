# replay-recipes — grep + jq for agency history

Zero-infrastructure replay. Run directly via Bash.

All examples assume `$OUT=/sessions/loving-adoring-maxwell/mnt/outputs/devsecops-agency`.

## Agent-scoped queries

### What has agent X concluded across all projects?

```
rg --no-filename --no-heading -N '' "$OUT/_sessions/market-researcher/" | \
  jq -c 'select(.type=="report") | {ts, projectSlug, gate, artifact, note}'
```

### All green/yellow/red gates for a specific Chief

```
rg --no-filename --no-heading -N '' "$OUT/_sessions/security-lead/" | \
  jq -c 'select(.type=="report" and .gate=="red") | {ts, projectSlug, phase, note, artifact}'
```

### Top-N busiest agents by entry count

```
for d in "$OUT"/_sessions/*/; do
  count=$(cat "$d"/*.jsonl 2>/dev/null | wc -l)
  echo "$count $(basename "$d")"
done | sort -rn | head -10
```

## Project-scoped queries

### Full CEO transcript for a project

```
rg --no-filename --no-heading -N '' "$OUT/_sessions/ceo/" | \
  jq -c 'select(.projectSlug=="invoice-splitter") | {ts, type, from, to, phase, gate, note}'
```

### All entries (every agent) for a project, time-ordered

```
rg --no-filename --no-heading -N '' "$OUT/_sessions/" | \
  jq -c --arg slug "invoice-splitter" 'select(.projectSlug==$slug) | {ts, agentId, type, note}' | \
  jq -s 'sort_by(.ts)[]'
```

### Which agents blocked the project?

```
rg --no-filename --no-heading -N '' "$OUT/_sessions/" | \
  jq -c --arg slug "invoice-splitter" 'select(.projectSlug==$slug and .gate=="red") | {agentId, phase, note}'
```

## Pattern queries (feed memory)

### All notes mentioning a keyword (Stripe, OAuth, N+1, etc.)

```
rg --no-filename --no-heading -N -i 'stripe' "$OUT/_sessions/" | \
  jq -c 'select(.type=="report" or .type=="note") | {ts, agentId, projectSlug, note}'
```

Use this as the input to a Light or REM dreaming pass when investigating a recurring theme.

### Time-to-green per phase

```
rg --no-filename --no-heading -N '' "$OUT/_sessions/ceo/" | \
  jq -c --arg slug "invoice-splitter" '
    select(.projectSlug==$slug) |
    select(.type=="dispatch" or (.type=="report" and .gate=="green")) |
    {ts, phase, type}' | \
  jq -s 'group_by(.phase)'
```

## Histogram / cost queries

### Tokens by agent (when populated)

```
rg --no-filename --no-heading -N '' "$OUT/_sessions/" | \
  jq -c 'select(.tokens.in) | {agentId, in: .tokens.in, out: .tokens.out}' | \
  jq -s 'group_by(.agentId) | map({
    agentId: .[0].agentId,
    in:  (map(.in)  | add),
    out: (map(.out) | add)
  }) | sort_by(-.in)'
```

### Failure modes

```
rg --no-filename --no-heading -N '' "$OUT/_sessions/" | \
  jq -c 'select(.type=="error") | {ts, agentId, projectSlug, note}'
```

## Index-refresh recipe (idempotent)

After any write, the writer should update both index files. A safe pattern:

```bash
SLUG="invoice-splitter"
AGENT="market-researcher"
SESSION="a4f1c09b22e8"

DIR="$OUT/_sessions/$AGENT"
mkdir -p "$DIR"
# append the entry
echo "$ENTRY_JSON" >> "$DIR/$SESSION.jsonl"

# refresh per-agent index (full rewrite of small JSON is fine)
# ... produce sessions.json via jq over the directory ...

# refresh global index
# ... produce _sessions/sessions.json ...
```

The CEO skill provides a small inline bash helper in its playbook; specialists do not need to construct this themselves.

## Anti-patterns

- Do NOT run `rg` without `--no-filename --no-heading -N` — the output won't pipe cleanly into `jq`.
- Do NOT parse JSONL with `awk`/`grep`-only. Always `jq -c`. One broken line kills the query silently otherwise.
- Do NOT read sessions from inside a running dispatch (race on append). Read after the writer has returned.
- Do NOT hand-edit a `.jsonl` file. If you need to correct an entry, append a new `note` entry referencing it.
