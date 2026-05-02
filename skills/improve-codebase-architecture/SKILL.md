---
name: improve-codebase-architecture
description: A periodic architecture-deepening review that surfaces friction in the codebase and proposes refactors that turn shallow modules into deep ones. The aim is twofold — testability and AI-navigability. Distinct from incident-response (which fixes a specific known break) and from tdd (which builds a specific feature); this skill walks the codebase looking for accumulated drift between what the project's CONTEXT.md says the system is and what the code actually does. Owned by the Architecture Council (CTO). Recommended cadence is once every two weeks per active project, or any time the User asks "is this codebase still healthy?". Heavily informed by the project's CONTEXT.md (domain language) and docs/adr/ + _decisions/<slug>/adrs/ (decisions the skill should not re-litigate).
metadata:
  version: "1.0.0"
  ratified: "2026-04-26"
  shipped_with_plugin: "0.6.1"
---

# improve-codebase-architecture

## Mission

Surface architectural friction. Propose **deepening opportunities** — refactors that turn shallow modules into deep ones, where "deep" means: a lot of behavior behind a small interface (Ousterhout, *A Philosophy of Software Design*). Deep modules give callers leverage and concentrate maintenance. Shallow modules look like complexity but actually just route it.

The skill exists because agent-driven coding accelerates software entropy. Codebases get more complex faster than ever, and the complexity often takes the shape of many small modules whose interfaces are nearly as complex as their implementations. This skill is the periodic counter-pressure.

## Architectural vocabulary (use these terms exactly)

Consistency in vocabulary is the point. When proposing a deepening opportunity, drift into "component," "service," "API," or "boundary" loses the precision the rest of the procedure depends on.

- **Module** — anything with an interface and an implementation (function, class, package, slice).
- **Interface** — everything a caller must know to use the module: types, invariants, error modes, ordering, config. Not just the type signature.
- **Implementation** — the code inside.
- **Depth** — leverage at the interface: a lot of behavior behind a small interface. **Deep** = high leverage. **Shallow** = interface nearly as complex as the implementation.
- **Seam** — where an interface lives; a place behavior can be altered without editing in place.
- **Adapter** — a concrete thing satisfying an interface at a seam.
- **Leverage** — what callers get from depth.
- **Locality** — what maintainers get from depth: change, bugs, knowledge concentrated in one place.

Three load-bearing principles:

- **Deletion test**: imagine deleting the module. If complexity vanishes, the module was a pass-through. If complexity reappears across N callers, the module was earning its keep.
- **The interface is the test surface.** The interface determines what behaviors can be asserted on without coupling tests to implementation.
- **One adapter = hypothetical seam. Two adapters = real seam.** A seam isn't a seam until at least two things depend on it; until then it's just an internal abstraction.

This skill is **informed by** the project's domain model. The domain language gives names to good seams. ADRs record decisions the skill MUST NOT re-litigate (the decisions were trade-offs at the time; this skill doesn't second-guess them unless friction is real and load-bearing).

## Procedure

### 1. Explore

Read first:
- `<slug>/CONTEXT.md` (project domain language)
- All ADRs under `_decisions/<slug>/adrs/` matching the area being reviewed
- The Agency-level `CONTEXT.md` for cross-cutting terms

Then dispatch a Worker with `subagent_type=Explore` to walk the codebase. Don't follow rigid heuristics — explore organically and note where you experience friction:

- Where does understanding one concept require bouncing between many small modules?
- Where are modules **shallow** — interface nearly as complex as the implementation?
- Where have pure functions been extracted just for testability, but the real bugs hide in how they're called (no **locality**)?
- Where do tightly-coupled modules leak across their seams?
- Which parts of the codebase are untested, or hard to test through their current interface?

Apply the **deletion test** to anything you suspect is shallow: would deleting it concentrate complexity, or just move it? "Yes, concentrates" is the signal you want.

### 2. Present a numbered list of deepening opportunities

For each candidate:

- **Files** — which files/modules are involved
- **Problem** — why the current architecture is causing friction; cite the specific deletion-test result or shallowness signal
- **Solution** — plain-English description of what would change
- **Benefits** — explained in **leverage** + **locality** terms, plus how tests would improve

**Vocabulary discipline:** use `<slug>/CONTEXT.md` for domain terms (e.g. talk about "the Order intake module," not "the FooBarHandler" or "the Order service"). Use the **architectural vocabulary** above for deepening terms.

**ADR-conflict handling:** if a candidate contradicts an existing ADR, only surface it when the friction is real enough to warrant revisiting the ADR. Mark it clearly:

> *Contradicts `ADR-0007-monolithic-payment-flow` — but worth reopening because the shallow-module count in the payment domain has grown from 4 to 19 since that ADR was filed, and the deletion test concentrates 12 of them.*

Do NOT list every theoretical refactor an existing ADR forbids. The skill is informed by ADRs, not blind to them.

**Do NOT propose specific interfaces yet.** The exploration produces a numbered list; the Sovereign picks which one to explore further. Save interface design for step 3.

### 3. Grilling loop on the chosen candidate

Once the Sovereign picks a candidate, drop into a `grill-with-docs`-style conversation. Walk the design tree with them — constraints, dependencies, the shape of the deepened module, what sits behind the seam, what tests survive.

Side effects happen inline (same discipline as `grill-with-docs`):

- **Naming a deepened module after a concept not yet in `<slug>/CONTEXT.md`?** Add the term to `CONTEXT.md` immediately. Same lazy-creation rule — create the file if it doesn't yet exist.
- **Sharpening a fuzzy term during the conversation?** Update `CONTEXT.md` right there.
- **Sovereign rejects the candidate with a load-bearing reason?** Offer an ADR, framed as: *"Want me to record this so future architecture reviews don't re-suggest it?"* Only offer when the reason would be needed by a future explorer to avoid re-suggesting the same thing — skip ephemeral reasons ("not worth it right now") and self-evident ones.

### 4. Produce the refactor brief (or queue it)

If the Sovereign greenlights the deepening:

- Produce a refactor brief describing the new module's interface (using `CONTEXT.md` vocabulary) and the migration steps.
- Hand off to `tdd` for implementation IF the refactor changes observable behavior. Otherwise hand off to a normal Engineering Council dispatch.
- File a `deepening-decision` ADR under `_decisions/<slug>/adrs/` recording what was deepened and why.

If the Sovereign queues the deepening for later:

- Add a row to `<slug>/architecture-backlog.md` with the candidate description and the conversation summary, so the next run of this skill doesn't re-discover the same opportunity from scratch.

## Cadence

Recommended: every two weeks per active project. The CTO can run it more often during heavy refactoring periods or less often during stable maintenance phases. Per the Beck principle: *"Invest in the design of the system every day."* This skill is the explicit design-investment moment when daily incremental design isn't enough.

Skipping multiple consecutive runs without a written reason routes the project to compliance-drift in the monthly heartbeat (`RHYTHM.md`).

## Anti-patterns

- **Re-litigating ADRs without real friction.** ADRs are the result of past trade-offs; only surface contradictions when current friction makes the prior trade-off worth reopening.
- **Proposing interfaces in step 2.** Save interface design for the grilling loop in step 3, after the Sovereign picks a candidate.
- **Using "service / component / API / boundary" vocabulary** instead of the architectural-vocabulary terms above. Vocabulary drift defeats the point.
- **Skipping the deletion test.** It's the load-bearing diagnostic; without it, "shallow" claims are subjective.
- **Treating one adapter as a seam.** One adapter = hypothetical seam. Two adapters = real seam.
- **Convening during a live incident** affecting the same subsystem. Use `incident-response`. Architectural review is a calm-day activity.
- **Auto-deepening without Sovereign approval.** This skill produces candidates and briefs; refactor execution requires explicit greenlight.

## Interaction with other skills

| Skill | How `improve-codebase-architecture` composes |
|---|---|
| `grill-with-docs` | Step 3 of this skill IS a grilling session, scoped to the chosen candidate. Same procedure, same CONTEXT.md and ADR side effects. |
| `tdd` | When a deepening lands, `tdd` runs the red-green-refactor cycle to implement it. The refactor brief from step 4 is one input to `tdd`. |
| `zoom-out` | Drop into `zoom-out` during step 1 if the responder doesn't yet have the layer-above map of the area being explored. |
| `audit` (CAO close-audit) | CAO spot-checks `<slug>/architecture-backlog.md` at quarterly retrospective for queued deepenings that have aged out. |
| `incident-response` | If a deepening identified here would have prevented a recent incident, the link is recorded in both the deepening ADR and the incident postmortem. |

## Provenance

- **John Ousterhout**, *A Philosophy of Software Design* (2nd ed., 2021) — origin of "deep modules" + the deletion-test-style reasoning about whether a module earns its interface complexity.
- **Kent Beck**, *Extreme Programming Explained* (2nd ed., 2004) — *"Invest in the design of the system every day"* — the principle that motivates the periodic-cadence framing.
- **Eric Evans**, *Domain-Driven Design* (2003) — ubiquitous language as the source of names for seams; the "use CONTEXT.md vocabulary" discipline.
- **Michael Nygard**, *Documenting Architecture Decisions* (2011) — the ADR convention this skill is informed by but does not re-litigate.
- The `mattpocock/skills` repository (MIT, 2026) is the curator that surfaced this combination — periodic deepening review tied to CONTEXT.md vocabulary and ADR-aware proposal generation — to the Agency in the v0.6.1 cycle. The procedure above is Agency-original synthesis from the underlying primary sources.
