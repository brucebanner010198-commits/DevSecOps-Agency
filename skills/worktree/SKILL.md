---
name: worktree
description: >
  Internal skill. Allocates an isolated scratch directory (a "worktree") for a
  Chief's dispatch so parallel agents don't step on each other's artifacts and
  fix-loop attempts can be compared against a baseline before merging. Invoked
  by the CEO on parallel dispatches and on every fix-loop (attempt ≥ 1). Not a
  user-facing skill.
metadata:
  version: "0.2.4"
---

# worktree — isolated scratch dirs for parallel + fix-loop dispatches

A worktree is a subdirectory under `<slug>/_worktrees/<chief>-<attempt>/` where a Chief writes its artifacts in isolation. On a green/yellow report the CEO merges the worktree into the main project tree; on a red report the worktree stays in place so attempt N+1 can diff against it.

This skill is the openclaw-inspired analog of `git worktree add`. There is no git involved — just a disciplined convention that makes parallel work atomic and fix-loops diffable.

## When to allocate a worktree

Allocate when **any** of these is true:

1. **Parallel dispatch.** Two or more Chiefs are dispatched for the same phase (`CRO+CPO` in discovery, `CQO+CISO²` in verify, `CKO+GC` in document-legal).
2. **Fix-loop attempt ≥ 1.** The Chief already reported red on attempt 0 — attempt 1 and 2 go into worktrees so we can diff before merging.
3. **Speculative dispatch.** The CEO starts Chief B on phase N+1 before Chief A's phase N has finalised (rare, requires override).
4. **User-directed variant.** The user asks for two approaches side-by-side ("show me both Postgres and SQLite versions").

Do **not** allocate on a sequential attempt-0 dispatch (the default case). Direct writes to the main tree are cheaper and cleaner.

## Layout

```
outputs/devsecops-agency/<slug>/
├── _worktrees/
│   ├── cro-0/              # attempt 0 (only present if parallel or speculative)
│   │   ├── worktree.json
│   │   └── research-brief.md
│   ├── pm-lead-0/          # parallel sibling of cro-0 in discovery
│   │   ├── worktree.json
│   │   └── product/strategy.md
│   ├── security-lead-1/    # fix-loop attempt 1 after security-lead attempt 0 red
│   │   ├── worktree.json
│   │   └── threat-model.md
│   └── _merged/            # archive of worktrees that merged cleanly
│       └── cro-0-<mergeTs>/
└── ...                     # the main project tree (merge target)
```

### worktree.json

```json
{
  "id": "security-lead-1",
  "chief": "security-lead",
  "attempt": 1,
  "taskId": "t-0007",
  "phase": "verify",
  "baseRev": "main@<iso>",
  "parentWorktree": "security-lead-0",
  "createdAt": "<iso>",
  "status": "open",
  "writes": ["threat-model.md", "security/code-audit.md"],
  "reads": ["architecture.md", "src/**"],
  "mergedAt": null
}
```

- `id` = `<chief>-<attempt>`. Unique per project.
- `baseRev` is a marker of what the main tree looked like when the worktree was created. In a no-git world it's just an ISO timestamp of the main tree's last update. Used for staleness detection.
- `writes[]` lists the paths the Chief is allowed to create inside its worktree. Out-of-scope writes are a bug.
- `reads[]` lists paths the Chief reads from the **main** tree (not the worktree) — it never reads from a sibling worktree.
- `status` ∈ `open | merged | discarded | stale`.

## Lifecycle

```
allocate  →  open                                           (CEO creates the dir + worktree.json)
open      →  merged        (green/yellow report accepted)
open      →  discarded     (red report superseded by next attempt, or cancelled task)
open      →  stale         (baseRev drifted; requires rebase before merge)
```

### 1. Allocate

CEO, before writing the `dispatch` entry to `chat.jsonl`:

1. `mkdir -p <slug>/_worktrees/<chief>-<attempt>/`
2. Write `worktree.json` with `status: "open"` and the `writes[]`/`reads[]` for this Chief (looked up in `references/parallel-matrix.md`).
3. Pass the worktree root path into the Chief's dispatch context. The Chief must write every artifact **under this path**, not the main tree.
4. On the task row, set `worktree: "<chief>-<attempt>"`.

### 2. Merge

On a `green` or `yellow` report:

1. Verify every path in `writes[]` exists under the worktree.
2. Verify no path outside `writes[]` has been created in the worktree (bounce with `red` if so).
3. Verify `baseRev` matches the main tree's current revision. If drifted → `stale`; require the Chief to re-merge or rebase.
4. Copy each `writes[]` path from the worktree into the main tree, preserving directory structure.
5. Move the worktree dir to `_worktrees/_merged/<id>-<mergeTs>/` (keep for audit, not active). Update `worktree.json > status: "merged"`, `mergedAt: <iso>`.
6. Append a `merge` entry to `chat.jsonl`:
   ```json
   {"ts":"<iso>","scope":"board","from":"ceo","to":"<chief>","type":"merge","worktree":"<id>","writes":["..."],"note":"clean merge"}
   ```
7. Clear `worktree` on the task row.

### 3. Discard

On a `red` report that's being superseded by a fix-loop (not cancelled), the previous worktree stays `open` for diff purposes, and a **new** worktree is allocated for attempt N+1. When the fix-loop's new worktree merges, the old `red` worktree's `status` flips to `discarded` and it's moved to `_worktrees/_discarded/<id>-<ts>/`.

On a cancelled task, discard immediately.

### 4. Stale

If a worktree sits open for > 15 minutes and another dispatch has merged into paths in its `reads[]`, it becomes stale. The CEO must either (a) re-dispatch the Chief with a fresh worktree, or (b) merge as-is with an explicit `note: "possibly stale"`. Option (b) is allowed only if the stale paths are not in the Chief's `reads[]`.

## Conflict detection

On merge, a **conflict** is any path in the worktree's `writes[]` that has also been written in the main tree since the worktree was created (i.e. by a parallel dispatch that merged first).

Resolution rules, in order:

1. **Non-overlapping writes** — no conflict. Parallel sibling wrote to different paths. Merge clean.
2. **Same-file conflict** — last-merger wins on the exact bytes, but the CEO must emit a `conflict` entry to `chat.jsonl` listing the file, the two sources, and which won.
3. **Structural conflict** (same file, incompatible shape — e.g. both rewrote the same section) — CEO refuses to merge, opens an `inbox.json` item, task goes `blocked`.

Rule 2 is tolerable because our parallel dispatches write to non-overlapping paths by design (see `references/parallel-matrix.md`). Rule 3 is rare and always escalates.

## Why this reduces hallucination

- **Smaller context.** A Chief sees only its worktree + its declared `reads[]`. No sibling's draft contaminates its prompt.
- **Diffable fix-loops.** Attempt 1 can read attempt 0's artifact (from the previous worktree) and explicitly cite what changed. `corrections[]` in the fix-loop dispatch maps to visible diffs.
- **Atomic merge.** A partial artifact never ends up in the main tree — either the whole `writes[]` lands or none of it does.

## Invocation points (for the CEO)

- On parallel dispatch or fix-loop attempt ≥ 1: allocate.
- On Chief report: if the task had a worktree, run merge (green/yellow) or schedule discard (red superseded).
- On phase advance: verify no `_worktrees/*/worktree.json` has `status: "open"` for a completed phase. Any lingering open worktree is a bug.
- Emit `worktree` references in the task row, `chat.jsonl`, and (optionally) the command-center lane.

## Progressive disclosure

- `references/parallel-matrix.md` — per-phase table of parallel dispatches, each with `writes[]` + `reads[]` for every Chief.
- `references/merge-policy.md` — exact merge algorithm, conflict classes, and the stale-rebase protocol.
