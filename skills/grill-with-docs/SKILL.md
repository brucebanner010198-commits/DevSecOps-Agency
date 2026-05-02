---
name: grill-with-docs
description: A relentless interview pattern that the Agency invokes when an agent realizes it doesn't have enough information to make a decision well. Walk down each branch of the design tree one question at a time, resolve dependencies between decisions before continuing, and update the project's CONTEXT.md and ADRs inline as terms get sharpened and load-bearing decisions crystallize. Distinct from intake-router (proposed v0.5.4, deferred v0.7.0) which decides project mode at Phase 1; grill-with-docs is the in-flight clarification tool that any specialist invokes mid-task when ambiguity surfaces. Default convening reasons include CONTEXT.md term resolution at Phase 2 (Design), ADR drafting on architecturally-load-bearing trade-offs, and bridging the gap between a Sovereign's prose directive and the testable acceptance criteria that QA gates against.
metadata:
  version: "1.0.0"
  ratified: "2026-04-26"
  shipped_with_plugin: "0.6.1"
---

# grill-with-docs

## When to convene

A Specialist invokes `grill-with-docs` when one of these conditions holds:

- The current task references a term whose meaning is unclear in this project's `<slug>/CONTEXT.md` or in the Agency-level `CONTEXT.md`.
- An architectural choice is being made that satisfies the three-way ADR test (hard to reverse, surprising without context, real trade-off).
- The Sovereign's directive is prose; QA needs testable acceptance criteria; the gap between the two is wider than the Specialist can close alone.
- Two prior council outputs disagree on a domain term and the disagreement is load-bearing.

`grill-with-docs` is NOT the right tool when the Specialist just hasn't tried hard enough. Read the existing `CONTEXT.md`, `<slug>/architecture.md`, recent ADRs first. Convene only after the artifacts are exhausted.

## Inputs

- The current question or decision the Specialist needs resolved.
- The convening Specialist's role-card identity (so the Sovereign knows who's asking).
- Read access to `CONTEXT.md` (Agency-level), `<slug>/CONTEXT.md` (project-level if exists), `<slug>/architecture.md`, recent ADRs in `_decisions/<slug>/adrs/`, and the codebase under `<slug>/`.

## Outputs

- **Inline updates** to `<slug>/CONTEXT.md` (or Agency-level `CONTEXT.md` if the term is Agency-wide) — every term resolved during the session is added immediately, not batched.
- **One or more ADRs** filed under `_decisions/<slug>/adrs/` (or `docs/adr/` for Agency-level decisions) when load-bearing trade-offs land.
- **A summary back to the convening Specialist** — what was resolved, what remains open, which artifacts now exist that didn't before.

## Procedure

### 1. Read what exists first

Before asking any question of the Sovereign, the Specialist reads:

- Agency-level `CONTEXT.md`
- Per-project `<slug>/CONTEXT.md` (if exists; create lazily during the session if needed)
- `<slug>/architecture.md` if exists
- All ADRs in `_decisions/<slug>/adrs/` matching the area being discussed
- Spot-check the relevant code modules to verify the artifacts match reality

If a question can be answered by the existing artifacts or by reading the code, **answer it from there**. Never ask the Sovereign a question that the artifacts already answer.

### 2. Walk the design tree one question at a time

Ask **exactly one question per turn**. Wait for the Sovereign's answer before continuing.

For each question, propose your **recommended answer** as part of the question. The Sovereign confirms, redirects, or expands. Recommendations make the conversation faster than open-ended questions because the Sovereign can react instead of having to author from scratch.

Before asking the next question, decide if the answer to the previous one resolves a dependency for any other branch of the tree. If so, take that branch next; if not, return to the next sibling branch.

### 3. Inline-update CONTEXT.md as terms get resolved

When the Sovereign uses a term that conflicts with the existing `CONTEXT.md`, surface the conflict immediately:

> *Your CONTEXT.md defines `cancellation` as the customer-initiated termination of an active subscription, but you're using it here to mean a refund of an already-fulfilled order. Should I add `refund` as a separate canonical term, or is `cancellation` actually meant to cover both?*

When a vague term is used, propose a precise canonical term. When a domain relationship is being discussed, stress-test it with a concrete edge-case scenario.

When a term is resolved, **update CONTEXT.md immediately** — same conversation turn. Do not batch. The append-only invariant (Constitution §5.2) means the update is a new line; corrections are new lines that supersede earlier ones, never edits.

### 4. Cross-reference with code

When the Sovereign states how something works, check whether the code agrees. If you find a contradiction, surface it:

> *Your code at `src/orders/cancel.ts:47` cancels entire Orders. You just said partial cancellation is supported. The code doesn't match the spec — which is the truth right now?*

Code-vs-spec contradictions are themselves outputs worth filing as `code-spec-mismatch` ADRs when the gap is load-bearing.

### 5. File ADRs sparingly

Only file an ADR when ALL THREE of the following are true (the Nygard 2011 test, encoded in `docs/adr/README.md`):

1. **Hard to reverse** — the cost of changing your mind later is meaningful
2. **Surprising without context** — a future reader will wonder "why did they do it this way?"
3. **Real trade-off** — there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR. Most grilling-session decisions don't warrant an ADR; the few that do, do.

### 6. Stop when the dependency tree is resolved

The session ends when the Specialist has enough resolved to proceed with the original task. Not when every conceivable branch has been explored — when the immediate decision is unblocked. Open branches that surfaced during the session but weren't load-bearing for the immediate decision are noted in the summary back to the convening Specialist.

## Quality gates

Before reporting the session complete, the Specialist verifies:

- [ ] Every question that could have been answered by existing artifacts WAS answered from artifacts (no unnecessary Sovereign-time spent).
- [ ] Every term resolved during the session has a row in the appropriate `CONTEXT.md`.
- [ ] Every load-bearing trade-off has either an ADR filed or a written justification for not filing.
- [ ] Code-vs-spec contradictions surfaced during the session are recorded somewhere (ADR if load-bearing; project notes if not).
- [ ] The summary to the convening Specialist names the question that the session was convened to answer and confirms it's now answered.

## Anti-patterns

- **Asking the Sovereign questions the existing artifacts already answer.** Read first.
- **Asking multiple questions at once.** One per turn. Walk the tree.
- **Open-ended questions without a recommended answer.** Slower for the Sovereign; lazier for the Specialist.
- **Batching CONTEXT.md updates to the end of the session.** They get forgotten or merged wrong. Update inline.
- **Filing an ADR for every decision.** ADRs are receipts for load-bearing decisions only — three-way Nygard test or skip.
- **Coupling CONTEXT.md to implementation details.** Only domain-meaningful terms. If a term is meaningful only to one module's implementation, it doesn't belong in the project's ubiquitous language.
- **Treating the session as therapy.** It's a focused work session. The Sovereign's time is finite; resolve the dependency tree and end the session.
- **Convening during a live incident.** Incidents use `incident-response`. Grilling is for design and clarification, not crisis.

## Interaction with other skills

| Skill / convention | How `grill-with-docs` composes |
|---|---|
| `CONTEXT.md` (per-project + Agency-level) | The session's primary write target. Updated inline. |
| `docs/adr/` + `_decisions/<slug>/adrs/` | Load-bearing decisions land here. Three-way Nygard test gates filing. |
| `intake-router` (deferred v0.7.0) | Convened at Phase 1 to set project scope/mode. `grill-with-docs` is the in-flight clarification tool that any phase can convene; they don't compete. |
| `cross-model-panel` | When a grilling session surfaces a question that warrants cross-model deliberation (ASI-class, Constitution amendment, USER-ONLY at COST §2.4 threshold), the Specialist hands off to `panel-chair`. |
| `tdd` | After grilling resolves what to build, `tdd` runs the red-green-refactor loop. The grilling output (acceptance criteria + interface design) is one input to `tdd`. |
| `improve-codebase-architecture` | Step 3 of that skill drops into a grilling conversation when the Sovereign picks a deepening candidate. Same procedure as this skill, scoped to the candidate. |

## Provenance

- **Eric Evans**, *Domain-Driven Design* (Addison-Wesley, 2003) — the "ubiquitous language" pattern this skill operationalizes through inline CONTEXT.md updates.
- **Hunt & Thomas**, *The Pragmatic Programmer* (anniversary edition) — "No-one knows exactly what they want" framing that motivates the relentless-interview posture.
- **Michael Nygard**, *Documenting Architecture Decisions* (2011) — the three-way ADR test (hard to reverse + surprising + real trade-off) used in step 5.
- **Constitution §5.1 + §5.2** (this repo) — receipts ratio + append-only invariants that govern how CONTEXT.md and ADRs are updated.
- The `mattpocock/skills` repository (MIT, 2026) is the curator that surfaced this pattern combination — a relentless interview tied to inline CONTEXT.md and ADR updates — to the Agency in the v0.6.1 cycle. The procedure above is Agency-original synthesis from the underlying primary sources.
