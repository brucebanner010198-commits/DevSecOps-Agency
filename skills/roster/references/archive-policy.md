# archive-policy.md — retiring an agent file

Agents are never deleted. Fired / repurposed / merged agents are preserved in `_vision/roster/_archive/<name>.md`. The archive is part of the permanent paper trail.

## File shape

```markdown
---
archived: true
archived_date: <YYYY-MM-DD>
archived_by_adr: ADR-NNNN-<slug>
final_tier: <haiku|sonnet|opus>
final_council: <council slug>
superseded_by: <new-agent-name | —>
redirect_reason: <fire | repurpose | merge>
---

# ARCHIVED: <original-agent-name>

**Retired on <date> via ADR-NNNN-<slug>.**

<One paragraph citing the retirement rationale + the owning council when archived.>

## Redirect

<If repurpose or merge:>
- Future dispatches for this scope → `<new-agent-name>`.
- Semantic overlap: <bullet list of where the scope moved>.

<If fire with no replacement:>
- No replacement. Scope is considered out of portfolio for now.
- Re-hire trigger: <conditions under which reviving this agent becomes sensible>.

## Original prompt (frozen at archival)

<Verbatim copy of the final agents/<name>.md body. Do not edit after archive.>
```

## Invariants

- Archive files are append-only after the archival commit. The "Original prompt" block is frozen; later context edits append below, never overwrite.
- Filename: `_vision/roster/_archive/<original-name>.md`. Preserve the original kebab-case slug.
- The original `agents/<name>.md` must be removed in the same commit as the archive creation. Concurrent `agents/<name>.md` + `_archive/<name>.md` is an invariant violation (`cao` will flag).
- Council roster tables (in `councils/<council>/AGENTS.md` and in `agents/AGENTS.md > Council color mapping`) are updated in the same commit.
- `_sessions/<name>/*.jsonl` are never moved. Logs live where they were written. The archive redirect links to the log directory.

## Re-hire path

If a retired agent's scope returns (a common case in seasonal products), **do not rename and restore**. File a new hire ADR via `hiring-lead`, reuse the name only if `_archive/<name>.md > redirect_reason: fire` (not `repurpose` or `merge`). Restoring a repurposed agent would contradict the successor.

If restoring under the original name:

- Cross-link the new `agents/<name>.md` description block to the archive ADR: `<commentary>Restored via ADR-MMMM after retirement via ADR-NNNN.</commentary>`.
- `archived: true` front-matter stays in the archive file. That file remains frozen.
- Fresh `_sessions/<name>/` starts with a new session ID; old logs stay archived.

## Audit hook

`adr-auditor` checks every `_archive/<name>.md` on close/portfolio audit:

- `archived_by_adr` resolves to a real accepted ADR.
- Original prompt block hash matches `git show <archival-commit>:agents/<name>.md`.
- No post-archival edits to the "Original prompt" section.
- If `superseded_by: <new>` is set, `agents/<new>.md` exists.

Any mismatch = red finding.
