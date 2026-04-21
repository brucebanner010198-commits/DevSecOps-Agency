# councils/product — boundaries

## Output contract

- Lead: `pm-lead` (CPO). Specialists: spec-writer, product-strategist, roadmap-planner.
- Artifacts: `<slug>/product/strategy.md`, `<slug>/product/roadmap.md`, plus spec sections in `<slug>/brief.md`.
- Roadmap framework: **Now · Next · Later · Never**. Every item has a reason.

## Must

- Take the CRO's wedge verbatim. Do not redefine it.
- Name user, job-to-be-done, failure mode without product, success signal.
- Cut list is a feature of the output, not a bug. "Never" entries explain why not.
- Write acceptance criteria that the CQO can test. Measurable or binary.

## Must not

- Propose features that fail the wedge test ("does it serve the named user's named job?").
- Produce a roadmap with > 5 items in Now.
- Conflate strategy with copywriting. Positioning sentences are strategy; landing-page prose is not here.

## Gate heuristic

- `green`: strategy names wedge + positioning, roadmap has ≤ 5 Now items, every item has acceptance criteria.
- `yellow`: roadmap missing estimates or acceptance criteria on ≥ 1 item.
- `red`: strategy contradicts CRO wedge, or Now list exceeds team capacity.
