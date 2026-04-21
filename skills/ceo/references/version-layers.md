# version-layers.md — cumulative invariants

Each release layer is still in effect. The CEO playbook in `SKILL.md` is the condensed view; this is the long form.

## v0.2.4 — worktree parallelism

- Parallel dispatches and fix-loops (attempt ≥ 1) write to `<slug>/_worktrees/<chief>-<attempt>/`, not the main tree.
- Lifecycle: allocate → {merged | discarded | stale}. See `skills/worktree/SKILL.md`.
- Merge is **atomic** (all-or-nothing), **scope-checked** (out-of-scope writes bounce), **deterministic** (alphabetical write order).
- Structural conflicts escalate to `inbox.json`. Non-structural merge with a note.
- Per-phase `writes[]` / `reads[]` matrix: `skills/worktree/references/parallel-matrix.md`.

## v0.2.3 — gates + taskflow

- **Gates vocabulary**: `green · yellow · red · n/a`. Nothing else.
- **Blocking councils**: security (CISO) + legal (GC). Their reds block ship unless user waives via `inbox.json`.
- **Informing councils** aggregate into the project gate; CEO may waive after consent.
- **`yellow` requires non-empty `followups[]`.** No silent yellows.
- **Aggregation**: blocking red unwaived → red; any red → red; any yellow → yellow; else green. `n/a` skipped.
- **Task states**: `queued → in-progress → needs-decision → blocked → done/cancelled`. See `skills/taskflow/references/state-machine.md`.
- **Fix-loop cap**: 2 per `(council, phase)`. Attempt 3 forces `blocked`.
- **Handoff invariants**: no `needs-decision` or unblocked `blocked` task; no open worktree for the phase.

## v0.2.2 — scoped AGENTS.md + determinism

Hierarchy:

- Root `AGENTS.md` — repo-wide conventions, gate vocabulary, anti-patterns.
- `agents/AGENTS.md` — persona file shape, dispatch/report contract.
- `skills/AGENTS.md` — SKILL.md shape, progressive disclosure, versioning.
- `councils/<council>/AGENTS.md` — per-council Must / Must not / Gate heuristic.

**Before every Chief dispatch:** quote the matching `councils/<council>/AGENTS.md` Must / Must not / Gate heuristic into the dispatch context. Largest single lever against hallucination.

**Prompt-cache rule:** sort maps/sets/lists/registries/file lists/network results by a stable key (alphabetical for names, timestamp ascending for events) before passing to a model or tool.

## v0.2.1 — durable memory + session logs

- `_memory/` — cross-project. Read at init, Light after each phase, Deep at close, REM on retro.
- `_sessions/<agentId>/<sid>.jsonl` — append-only transcripts. One entry per dispatch / report / handoff / note / error.
- See `skills/memory/SKILL.md`, `skills/session-log/SKILL.md`.

## v0.2.0 — org chart

- CEO + 9 Chiefs + ~28 specialists. Dual-hat: `engineering-lead` covers Architecture + Execution.
- 7-phase board. Sequential where dependent, parallel where disjoint.
