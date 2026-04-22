# lessons-ledger/references/row-schema.md

The exact schema for one row in `LESSONS.md`. Mirrors `LESSONS.md > ## Row schema` but adds derivation rules.

## Layout

One H3 block. One table. Fields in the exact order below.

```markdown
### <slug> — <closedAt YYYY-MM-DD>

| Field | Value |
| --- | --- |
| outcome | shipped / blocked / parked-rung-7 |
| council-lead ship | CISO=<gate>, GC=<gate> |
| okr-alignment final | green / yellow / red / n/a |
| rungs traversed | 0 | 1-<n> | 7 |
| fix-loops (sum) | <int> |
| waivers | <n> — [ADR-XXXX, ...] |
| stones authored | <n> — [paths] / none |
| lessons | <= 3 bullets, each with a citation |
| reusable decisions | <= 2 bullets citing ADR paths |
| what we'd change | <= 2 bullets |
| next-run trigger | <condition> / - |
```

## Field derivation

| Field | Source | Rule |
| --- | --- | --- |
| slug | `status.json > projectSlug` | kebab-case, must match the project folder name |
| closedAt | `status.json > lastUpdated` on the turn that wrote `phase: delivered` or `phase: blocked` | ISO YYYY-MM-DD only, no time |
| outcome | `status.json > phase` | map: `delivered`→shipped, `blocked`→blocked, `parked`→parked-rung-7 |
| council-lead ship | `status.json > gates.byCouncil.security` + `.legal` | final colours at close turn |
| okr-alignment final | `_vision/projects/<slug>.md > ## Closed > alignment` | literal value |
| rungs traversed | `status.json > metrics.rungAttempts` keys | `0` if empty; else `min-max` of keys; `7` if project parked |
| fix-loops (sum) | `status.json > metrics.fixLoops` | integer |
| waivers | `grep 'kind: waiver'` across `_decisions/ADR-*.md` filed in the project window | count + ADR IDs |
| stones authored | `_vision/playbooks/stones/*.md` where `project: <slug>` in frontmatter | count + paths, or `none` |
| lessons | `_meetings/<slug>-retro-<date>.md > ## Lessons` | copy bullets verbatim, preserve citations |
| reusable decisions | `_meetings/<slug>-retro-<date>.md > ## Reusable decisions` | copy bullets verbatim |
| what we'd change | `_meetings/<slug>-retro-<date>.md > ## What we'd change` | copy bullets verbatim |
| next-run trigger | `_meetings/<slug>-retro-<date>.md > ## Follow-ups` (if parked) | mandatory for parked-rung-7, `-` otherwise |

## Length rules

- **120 chars per table cell maximum.** Multi-bullet fields use `<br>` inside the cell to preserve the one-row-per-project invariant.
- **Citations are outside the 120-char budget.** They are meta.
- **No prose paragraphs.** Bullets or one-liners only.

## Required vs. optional fields

All fields are required. Optional values:

- `waivers` → `0 — none` if no waivers filed.
- `stones authored` → `none` if no stones.
- `next-run trigger` → `-` for shipped / blocked rows where no future revisit is planned.

Missing any required field = malformed row = CAO red at next portfolio audit + immediate rollback by `lessons-ledger`.

## Correction rows

A correction is a new row with:

- Same `slug`.
- Different `closedAt` (must be > original `closedAt`).
- `outcome` = `shipped-corrected` / `blocked-corrected` / `parked-corrected`.
- `lessons[0]` must start with `[correction]` and cite the original row's H3 anchor.

Example:

```
### invoice-splitter — 2026-05-12

| Field | Value |
| --- | --- |
| outcome | shipped-corrected |
| ... | ... |
| lessons | [correction] revised post-incident finding: auth retry loop masked a session-fixation issue (see LESSONS.md > invoice-splitter-2026-04-21). `_vision/audit/incident-INC-0017.md` |
```

## Sort invariant

Rows sorted by `closedAt` ascending. Correction rows sort after their originals by construction (`closedAt` strictly > original).

## Parser contract

Readers (idea-pipeline, carry-over-check, portfolio audit) parse by:

1. Split on `^### ` headings.
2. Slug + closedAt from the heading.
3. Fields from the table, matching by `| <Field Name>` column.

Readers fail-fast on malformed rows — they emit `error: "malformed row at <H3-anchor>"` and refuse to continue until the row is fixed (via a correction row, never edit).
