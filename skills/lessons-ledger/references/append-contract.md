# lessons-ledger/references/append-contract.md

Append-only write semantics for `LESSONS.md`. Hard rules from `VALUES.md §4`.

## Write operation

- Use `Write` with the full previous contents followed by the new H3 block.
- Never use `Edit` on `LESSONS.md`.
- `Edit` would be a hand-mutation — `VALUES.md §4` and `AGENTS.md > ## Writing` forbid that for this file.

## Slug collision

If the slug already has a row in `LESSONS.md`:

1. **Check whether the existing row's `outcome` is terminal.**
   - `shipped`, `blocked`, `parked-rung-7` → terminal.
   - `shipped-corrected`, `blocked-corrected`, `parked-corrected` → also terminal (a correction of a terminal row).
2. **If terminal:** the new row is a correction. Must match the correction-row rules in `row-schema.md > ## Correction rows`.
3. **If not terminal:** this is a bug. The ledger should never hold a non-terminal row. Abort and file CAO incident.

## `closedAt` monotonicity

Within a slug:

- All rows for the same slug must have strictly increasing `closedAt`.
- Ledger writer rejects a row whose `closedAt` ≤ the latest row for the same slug.

Across slugs: ledger writer appends any new slug's row at the bottom, and the sort pass moves it into place. If the new row's `closedAt` is not the most recent, the sort pass reorders the file.

## Sort pass

After every append:

1. Read the whole file.
2. Split on `^### `.
3. Parse `closedAt` from each heading.
4. Sort stable ascending by `closedAt`.
5. For ties (same day), sort by slug alphabetically.
6. Write back.

The stable sort preserves order within a `closedAt` day — this matters when multiple projects close the same day.

## ADR pairing

Every append files an ADR at `_decisions/ADR-NNNN-lessons-<slug>.md` in the same CEO turn.

ADR body (telegraph, per `skills/adr/SKILL.md`):

```
# ADR-NNNN — lessons-append: <slug>

- **Status:** accepted
- **Kind:** lessons-append
- **Slug:** <slug>
- **Ledger anchor:** LESSONS.md > <slug>-<closedAt>
- **Retro source:** _meetings/<slug>-retro-<closedAt>.md
- **Decision:** append one row per schema.
```

Skipping the ADR is a CAO red.

## Failure modes

| Failure | Behaviour |
| --- | --- |
| retro file missing | abort, log `blocked — retro missing`, do not write |
| CAO audit missing | abort, log `blocked — close-audit missing`, do not write |
| slug collision, non-terminal existing row | abort, file CAO incident, do not write |
| malformed retro (< 10 sections) | abort, return `bouncing retro back to retrospective skill` |
| disk write failure | retry once, then abort + notify |
| corrupted sort (parse failure of existing row) | abort, flag CAO red, do not write |

## Idempotency

The skill is **not** idempotent by design — appending the same row twice would violate append-only semantics. The slug collision check guards against double-append.

A deliberate re-try (e.g. same-day correction of a typo in the just-appended row) is handled as a **correction row** per `row-schema.md > ## Correction rows`. The original row stays; a new row with different `closedAt` overrides it.

## Read-before-write

Before appending, the skill always:

1. Reads `LESSONS.md` in full.
2. Scans for the slug's most recent row.
3. Applies collision + monotonicity checks.
4. Only then composes the new block.

Skipping this read = potential double-append. The skill must never short-circuit the read.

## Locking (future)

v0.3.8 is single-writer — only the CEO invokes `lessons-ledger`, so there is no concurrency concern. If future versions introduce parallel project closes, add a file-lock invariant here before implementing. Until then: assume single-writer.
