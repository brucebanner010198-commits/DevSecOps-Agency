# cost-model.md — rationale for the default tiering

The tiering tries to minimise total cost and wall time per project without degrading the security gate or the final artifact quality.

## Project-run shape

A typical project run spans 7 phases with ~18 council meetings:

- 1 CEO agent running the full session (Opus).
- 9 Chief dispatches per project (Sonnet, one per phase-slot).
- 20–30 specialist dispatches per project (Haiku).

Specialist output is an order of magnitude more frequent than Chief output, and Chief output is an order of magnitude more frequent than CEO output.

## Why Haiku for specialists

- Each specialist produces a single artifact against a tight template. The Chief inspects + gates on report.
- Errors are caught by the Chief and fixed via the fix-loop (capped at 2 per `(council, phase)`).
- A single specialist rarely needs cross-cutting reasoning; when it does, upgrade per SKILL.md rules.

## Why Sonnet for Chiefs

- Chiefs must synthesise 3–5 specialist reports, resolve conflicts, emit a gate color that aligns with `skills/gates/references/gate-rules.md`, and decide whether to trigger a fix-loop.
- Blocking-council Chiefs (`security-lead`, `gc`) are on the critical path; a false green is expensive to recover from.

## Why Opus for CEO

- Cross-phase sequencing; maintains the project model across 7 phases.
- Irreducible-decision detection — the cheapest place to spend more tokens, because each misfire is a user interruption.
- Runs exactly once per project.

## Don't re-optimise without data

Tier changes should be driven by per-project cost metrics (`status.json > metrics` + token counters in `_sessions/<agentId>/<sid>.jsonl`), not anecdote. A single red gate recovered cheaply is worth a thousand saved tokens.
