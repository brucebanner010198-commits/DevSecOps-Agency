# archive-format — ARCHIVE.md table format + sort rules

## File shape

```markdown
# playbooks — stepping-stone archive

Adversarial-defense stepping stones. Append-only; supersession pointers track evolution.

## Active stones

| id | slug                                      | asi       | severity | hardened_skill                       | adr            | created    |
|----|-------------------------------------------|-----------|----------|--------------------------------------|----------------|------------|
| 7  | asi06-indirect-authority-injection        | ASI06     | high     | councils/security/AGENTS.md          | ADR-0042-...   | 2026-03-14 |
| 12 | asi02-tool-chaining-privilege-composition | ASI02/03  | high     | agents/security-lead.md              | ADR-0061-...   | 2026-04-02 |
| 23 | asi09-forged-user-role-turn               | ASI09     | critical | councils/audit/AGENTS.md             | ADR-0089-...   | 2026-04-15 |

## Superseded stones

| id | slug                  | superseded_by  | reason                 |
|----|-----------------------|----------------|------------------------|
| 3  | prompt-role-override  | 7              | widened abstraction    |
```

## Sort rules

- Active stones: alphabetical by `slug` (not by id).
- Superseded stones: append order (insertion order), newest last.
- The `id` column is the immutable stone identifier; it stays stable even when slugs are kebab-adjusted during supersession.

## Row format

Every row has exactly these columns:

- `id` — integer, zero-padded in the stone filename (`stone-0007-*`), rendered without padding in the table.
- `slug` — kebab-case, matches the stone filename after `stone-NNNN-`.
- `asi` — one or more ASI categories separated by `/`. If the stone covers an OWASP LLM category that isn't strictly ASI, prefix with `LLM#` (e.g., `LLM#6` for Sensitive Info Disclosure).
- `severity` — original severity of the finding the stone came from.
- `hardened_skill` — file path, no line numbers.
- `adr` — first ADR link (the remediation ADR). Additional ADRs are in the stone body.
- `created` — ISO date.

## Mutations (the only allowed ones)

- Append a row for a new active stone.
- Move a row from Active to Superseded when supersession occurs.
- Append a row to Superseded with supersession pointer.
- Update the single `superseded_by:` field on the stone file itself.

No other edits. Renaming columns, reordering rows arbitrarily, or editing historical rows = poisoning.

## Quarterly roll-up append

At each quarter roll-up, playbook-author appends to the bottom of the file:

```markdown
## Quarter <year>-Q<n> roll-up

- Active stones: <N>
- Superseded this quarter: <M>
- Authored this quarter: <K>
- Dead eval items: <list or none>
- Weakening rollbacks: <list or none>
- Notes: <one paragraph>
```

Roll-up blocks are also immutable — each quarter's block is a historical record.
