# status-lifecycle — transitions, immutability, supersede vs reverse

## The five states

- `proposed` — filed but not yet executed on. Rare.
- `accepted` — decision made, executing or executed.
- `rejected` — the alternative won; kept for the record.
- `superseded-by-ADR-MMMM` — a newer ADR replaces this one.
- `reversed` — undone without replacement.

## Legal transitions

```
proposed  → accepted | rejected
accepted  → superseded-by-ADR-MMMM | reversed
rejected  → (terminal — never re-opens; file a new ADR instead)
superseded-by-ADR-MMMM → (terminal)
reversed  → (terminal)
```

Accepted is the only state that can forward to supersede or reverse. Rejected and terminal states never re-open.

## Immutability rules

After an ADR is `accepted`:
- **Body is immutable.** Context, Decision, Consequences, Alternatives, Follow-ups — frozen.
- **Header is mutable** — only `Status` and `Related:` (to add the superseding ADR number).
- **Every edit appends to `## Status history`** at the bottom.

Before acceptance (while still `proposed`):
- Whole ADR is mutable. Update in place.
- No `## Status history` until first acceptance transition.

## Supersede vs reverse vs new-ADR

**Supersede** — use when a new decision replaces this one with a different decision on the same question. The new ADR explicitly names the predecessor in `Related:`.

Example: ADR-0007 picks Supabase. ADR-0027 picks Neon (the team outgrew Supabase's free tier and needs branching). ADR-0027 is filed with `Related: ADR-0007 (superseded)`. ADR-0007 status flips to `superseded-by-ADR-0027`.

**Reverse** — use when the decision is undone without a replacement. This is the "we tried it, it didn't work, we're unwinding" pattern. Rare. Requires a paragraph of rationale in a fresh ADR that reverses — still file a new ADR (`ADR-NNNN: Reverse ADR-0007 — drop Supabase, return to hand-rolled`), AND flip the reversed ADR's status to `reversed` with the reverser's ADR number in `Related:`.

**New ADR** — use when the question is similar but meaningfully different. ADR-0007 picks Supabase for tracker. ADR-0027 picks Firebase for a chat project. These are different projects — don't supersede; file independently with cross-references.

## Status history block shape

```markdown
## Status history
- 2026-04-21: proposed → accepted (ceo)
- 2026-04-22: accepted → superseded-by-ADR-0027 (ceo, rationale: team needed branching)
```

One line per transition. Date, transition, actor, optional rationale ≤ 20 words.

## Related: field rules

- Comma-separated list of ADR numbers, vision sections, or project slugs.
- When superseding, include the predecessor's number.
- When being superseded, the newer ADR's number is added (via edit to the Status header + Related field).
- Never remove a reference from Related: — it's append-only like status history.

## Enforcement

The `adr` skill's write path validates:
- Status transition is legal (see graph above).
- If status is `superseded-by-ADR-MMMM`, ADR MMMM exists and references this ADR in its own `Related:`.
- If status is `reversed`, a separate reversing ADR exists.
- `## Status history` has a line for every transition after initial creation.

Violations bounce the write with `"illegal ADR status transition: <from> → <to>"`.

## Never

- Re-open a rejected ADR. File a new ADR with new reasoning instead.
- Edit an accepted ADR's body. Supersede.
- Delete an ADR file. Ever.
- Forward a superseded or reversed ADR to any other state.
- Reverse an ADR without filing the reversing ADR that explains why.
