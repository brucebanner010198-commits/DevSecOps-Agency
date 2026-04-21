# Merge policy — how a worktree lands in the main tree

Two goals: atomic (all-or-nothing per worktree) and deterministic (same inputs → same merge, for prompt-cache stability).

## The merge algorithm

```
function merge(worktree):
    # 1. Scope check
    for path in list_files(worktree.dir):
        if path not in worktree.writes:
            return FAIL("out-of-scope write: " + path)

    for path in worktree.writes:
        if not exists(worktree.dir / path):
            return FAIL("declared write missing: " + path)

    # 2. Staleness check
    if main_tree_revision > worktree.baseRev:
        touched = paths_changed_in_main_since(worktree.baseRev)
        if any(p in touched for p in worktree.reads):
            return STALE(touched)

    # 3. Conflict check
    conflicts = []
    for path in sort(worktree.writes):                # <-- alphabetical, prompt-cache rule
        if exists(main_tree / path) \
           and mtime(main_tree / path) > worktree.baseRev:
            conflicts.append(path)

    if conflicts:
        for p in conflicts:
            if is_structural(p, worktree.dir / p, main_tree / p):
                return STRUCTURAL_CONFLICT(p)
        # non-structural: last-merger wins, emit note
        emit_conflict_note(conflicts)

    # 4. Atomic copy
    for path in sort(worktree.writes):
        mkdirs(main_tree / dirname(path))
        cp(worktree.dir / path, main_tree / path)

    # 5. Archive worktree
    mv(worktree.dir, "_worktrees/_merged/" + worktree.id + "-" + now())
    set worktree.status = "merged"
    set worktree.mergedAt = now()

    emit_merge_note(worktree)
    return OK
```

Four rules the algorithm encodes:

1. **No out-of-scope writes.** A Chief that writes paths it didn't declare fails the merge. This is the single strongest defense against a hallucinated artifact showing up in the main tree.
2. **Alphabetical merge order.** Always sort `writes[]` before copying. Same inputs → same byte sequence of operations → prompt-cache friendly for any log or artifact that embeds the order.
3. **Stale-read detection.** If a path the Chief read from main has changed since the worktree was created, the worktree is stale. Must re-dispatch with fresh reads.
4. **Structural vs non-structural conflicts.** Non-structural = both workers wrote the same file but in compatible shape (e.g. each added its own markdown section). Structural = incompatible (e.g. both rewrote the same section). Only structural conflicts escalate to the user.

## What counts as "structural"

A conflict is **structural** if any of:

- Both worktrees wrote a `status.json` with disagreeing field values.
- Both worktrees wrote a `package.json`/`requirements.txt` with overlapping dependency versions.
- Both worktrees rewrote the same markdown section (same `##` header block).
- Both worktrees wrote to the same line range in a code file.

Non-structural examples (merge with a note):

- Both worktrees wrote `chat.jsonl` — always append-only, just concatenate in timestamp order. Not a real conflict.
- One worktree added a new section to an existing doc, the other didn't touch that file.

In practice, `references/parallel-matrix.md` keeps `writes[]` sets disjoint, so structural conflicts should never happen. If one occurs, it's a planning bug — probably the parallel-matrix should be updated to serialise those two Chiefs.

## Stale rebase protocol

When merge returns `STALE(touched)`:

1. CEO writes a `stale` entry to `chat.jsonl` naming the worktree and the touched paths.
2. If the Chief's work is still valid (touched paths are not in its `writes[]` — it read them but didn't transform them), the CEO may **rebase**:
   - Update `worktree.baseRev` to the current main-tree revision.
   - Re-merge. If clean, proceed.
3. If the Chief's work depended on the stale bytes, CEO re-dispatches the Chief with a fresh worktree. Discard the stale one.

## Archive / discard policy

- `_worktrees/_merged/<id>-<mergeTs>/` — kept for the life of the project. The audit trail. Reviewers can diff against the main tree.
- `_worktrees/_discarded/<id>-<ts>/` — kept for 7 days (or until project close, whichever is first). After that, garbage-collected.
- Active `_worktrees/<chief>-<attempt>/` with `status: "open"` for > 30 minutes is a stuck task. CEO must either merge, discard, or escalate.

## Merge entry (chat.jsonl)

```json
{
  "ts": "<iso>",
  "scope": "board",
  "from": "ceo",
  "to": "<chief>",
  "type": "merge",
  "worktree": "<id>",
  "writes": ["threat-model.md", "security/compliance.md"],
  "conflicts": [],
  "baseRev": "main@<iso>",
  "note": "clean merge"
}
```

On conflict:

```json
{
  "ts": "<iso>",
  "scope": "board",
  "from": "ceo",
  "to": "<chief>",
  "type": "merge",
  "worktree": "<id>",
  "writes": ["..."],
  "conflicts": [
    {"path": "docs/README.md", "resolution": "last-merger-wins", "lost": "cro-0"}
  ],
  "note": "non-structural overlap on README; used docs-lead version"
}
```

On structural conflict (task goes `blocked`, not merged):

```json
{
  "ts": "<iso>",
  "scope": "board",
  "from": "ceo",
  "to": "<chief>",
  "type": "escalate",
  "worktree": "<id>",
  "conflicts": [{"path": "package.json", "reason": "disagreeing versions of react"}],
  "inboxItem": "inbox-0009"
}
```

## Anti-patterns

- **Silent partial merge.** Copying some of `writes[]` and stopping on first missing file. Atomicity means all or nothing.
- **Merging over a stale baseRev.** If main has changed, either rebase explicitly or re-dispatch. Never merge stale bytes silently.
- **Reading a sibling's worktree.** A Chief reads from main or its own worktree. Full stop.
- **Mutating `_merged/` or `_discarded/`.** Archive is read-only. For audit, not reuse.
- **Non-deterministic merge order.** Always sort `writes[]` alphabetically before iterating.
