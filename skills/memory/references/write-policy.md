# write-policy — rules for every memory write

Append-only. Redact. Cite. Sort.

## Append-only

- Never rewrite an existing line in `MEMORY.md`, `memory/<date>.md`, or any `patterns/<slug>.md`.
- To correct a prior entry, add a new entry with `[correction of <date>]` prefix. Do not delete.
- File layout is always newest-at-top for dated files, newest-at-bottom for `patterns/<slug>.md` (chronological within a project).

## Opt-in model

- Default: **on**, because the Cowork outputs directory is a private per-user workspace.
- Off-switch: if the user says "don't remember this project", "don't save learnings", or sets `brief.md > ## Decisions (CEO) > memory: off`, skip all writes for that slug and do not read from prior memory into its brief.
- Global off-switch: file `_memory/.disabled` — if present, every tier is a no-op. Leave `sessionLog` alone; that's a separate contract.

## Redaction checklist

Before writing any bullet or section:

- [ ] No email addresses (`rg '\b[\w.+-]+@[\w.-]+\.\w+\b'` before write — replace with `<email>`).
- [ ] No tokens/keys (`rg -i 'sk_|pk_|api[_-]?key|bearer\s|password\s*[:=]'` — replace with `<secret>`).
- [ ] No internal URLs with auth (`rg '://\w+:\w+@'` — replace auth with `<auth>`).
- [ ] No customer PII — names, addresses, phone numbers, IDs that map to real people. Replace with role labels ("user A").
- [ ] No IP addresses unless obviously public example (1.1.1.1, 8.8.8.8).

If a fact requires a secret to be useful, write the fact without the secret and note "requires secret" instead. Example: write `- [pattern] Stripe webhook endpoint must verify signature with raw body` — not the signing secret itself.

## Citation requirement

Every bullet in `patterns/<slug>.md` and `memory/<date>.md` must cite its source as a project-relative path, optionally with line range:

```
- [risk] N+1 query in invoice list view on load > 50 items (src/routes/invoices.ts:84-101)
- [decision] Chose PostgreSQL over SQLite for multi-tenant isolation (architecture.md:§Database)
```

Bullets without citations are not written. No exceptions.

## Deterministic ordering

Whenever memory is assembled into a prompt (for a dreaming pass or a brief injection):

- Sort sections alphabetically by header.
- Within a section, sort bullets by their first character after the category tag.
- This is not for the reader — it's for the prompt cache. Openclaw's rule: *"deterministic ordering for maps/sets/registries/plugin lists/files/network results before model/tool payloads."*

For human-facing output (the actual `.md` file), keep natural order (newest at the expected end per the append-only rule). Sorting is only applied to the in-flight prompt payload.

## File size caps

- `MEMORY.md` soft cap 500 lines. If exceeded, the next REM run must include a "compaction" step: collapse `Recurring risks` and `Anti-patterns` entries that appear less than twice into a single "Older noted risks" sub-bullet with file-path citations.
- `memory/<date>.md` has no cap; one per day is fine.
- `patterns/<slug>.md` soft cap 200 lines per project. Beyond that, Deep dreaming has kept low-signal content — re-run with tighter `max_bullets`.

## What the CEO logs after a write

Append to the active project's `chat.jsonl`:

```json
{"ts":"<iso>","scope":"memory","from":"ceo","to":"_memory","type":"write","tier":"light|deep|rem","artifact":"<path>","note":"<count> bullets"}
```

Command-center renders these with a small book-icon prefix. They do not count toward board/council filters.
