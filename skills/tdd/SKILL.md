---
name: tdd
description: Test-driven development with a strict red-green-refactor loop, vertical-slice progression (one test → one implementation → repeat), and a discipline against horizontal slicing (writing all tests before any implementation). Owned by the Quality Council (CQO). Use when the convening Specialist wants to build a feature or fix a bug under TDD discipline; the Agency's QA gate at Phase 4 prefers TDD-built features over after-the-fact tested ones because the test suite produced by red-green-refactor verifies behavior through public interfaces (which survives refactoring) rather than implementation details (which break on every refactor).
metadata:
  version: "1.0.0"
  ratified: "2026-04-26"
  shipped_with_plugin: "0.6.1"
---

# tdd

## Philosophy in one paragraph

Tests verify **behavior through public interfaces**, not implementation details. If a test breaks when you rename a private function or restructure an internal data flow but the user-visible behavior hasn't changed, the test was testing the wrong thing. A good test reads like a specification: *"user can complete checkout with a valid cart"* tells you exactly what capability exists. That test survives refactors. A bad test mocks internal collaborators or asserts on private state — it's coupled to the implementation, not to the behavior, and it will fight every refactor instead of supporting it.

## The vertical-slice rule (the one that matters most)

**Do NOT write all the tests first, then all the implementation.** This is "horizontal slicing" — treating RED as "write all tests" and GREEN as "write all code." It produces tests written in bulk against *imagined* behavior, not *actual* behavior. The tests end up asserting on the *shape* of things (data structures, function signatures) rather than on user-facing behavior. They become insensitive to real changes — pass when behavior breaks, fail when behavior is fine.

The correct shape is **vertical slices via tracer bullets**: one test → one implementation → repeat. Each test responds to what you learned from the previous cycle. Because the implementation just landed, the next test is informed by what behavior actually matters and how to verify it.

```
WRONG (horizontal):
  RED:   test1, test2, test3, test4, test5
  GREEN: impl1, impl2, impl3, impl4, impl5

RIGHT (vertical):
  RED→GREEN: test1→impl1
  RED→GREEN: test2→impl2
  RED→GREEN: test3→impl3
  ...
```

## Workflow

### 1. Plan with the Sovereign

Before writing any code, the Specialist confirms with the Sovereign (or with the convening Council if the Sovereign already approved a scoped brief):

- Which **public interface** will be exposed or changed
- Which **behaviors** are most important to test, ranked
- Which **deep-module opportunities** exist (small interface, deep implementation, per Ousterhout)
- Whether the project's domain language in `<slug>/CONTEXT.md` provides names that test names should adopt
- Whether any ADRs in `_decisions/<slug>/adrs/` constrain the area being touched

Ask: *"What should the public interface look like? Which behaviors matter most?"*

You can't test everything. Confirm explicitly which behaviors matter most. Focus testing on critical paths and complex logic, not every edge case.

### 2. Tracer bullet (one test, one implementation, end-to-end)

Write **ONE** test that confirms **ONE** thing about the system end-to-end:

```
RED:   Write the first test → it fails because the code doesn't exist
GREEN: Write the minimum code to make it pass → it passes
```

This is the tracer bullet. It proves the path works from public interface down to whatever the test actually exercises. Even if the path is shallow, the tracer establishes the test infrastructure, the data fixtures, the import paths, and the failure mode of the test framework.

### 3. Incremental loop

For each remaining behavior on the prioritized list:

```
RED:   Write the next test → it fails
GREEN: Write the minimum code to pass → it passes
```

Hard rules:

- **One test at a time.** No batching.
- **Only enough code to pass the current test.** No anticipation of future tests.
- **Don't test what you don't yet need.** Speculative test coverage is technical debt.
- **Tests describe observable behavior**, not internal mechanics.

### 4. Refactor (only when GREEN)

After all priority-list tests pass, look for refactor candidates:

- Extract duplication
- Deepen modules — move complexity behind simple interfaces (Ousterhout)
- Apply SOLID principles where natural (don't force them)
- Consider what the new code reveals about the existing code

**Never refactor while RED.** Get to GREEN first. Refactoring under failing tests means you can't tell whether your refactor broke something or whether the test was already broken.

Run the test suite after each refactor step. If a test breaks during a refactor, you have two pieces of information: the refactor changed observable behavior (bad — revert and rethink), or the test was coupled to the implementation (bad in a different way — fix the test to assert on behavior, then continue refactoring).

## Per-cycle checklist

Each red-green cycle, before moving to the next, verify:

- [ ] Test describes behavior, not implementation
- [ ] Test uses public interface only — no asserting on private state
- [ ] Test would survive an internal refactor of the module under test
- [ ] Code is minimal for this test — no speculative features added
- [ ] Test name uses vocabulary from `<slug>/CONTEXT.md` (so future readers don't have to translate)

## When to break the rules

The vertical-slice rule is load-bearing for new features and bug fixes. Two narrow exceptions:

- **Regression test for a known bug.** Write the failing test that reproduces the reported bug FIRST, then fix the bug, then continue with the priority list. The bug-reproduction test is its own tracer bullet for the fix.
- **Public-API contract test.** When the public interface is the contract (e.g., a published HTTP API), a small horizontal pass writing all the contract tests at once is acceptable AS LONG AS the implementations follow vertical-slice. The contract tests are specifying the surface; the slice work is building the implementation.

In both exceptions, the tests are still asserting on behavior, not on implementation.

## Anti-patterns

- **Horizontal slicing** (writing all tests first). The single most damaging anti-pattern in TDD; produces brittle tests against imagined behavior.
- **Mocking internal collaborators** to "isolate the unit under test." If a test breaks when you rename a private function, the test was wrong.
- **Testing private methods.** If the private method needs testing, it's actually part of the public contract — refactor to expose it through the public interface, then test that.
- **Asserting on database state directly** instead of going through the interface. Same coupling problem as mocking internals.
- **Speculative tests.** Tests for behavior that's not on the priority list. They become technical debt the first time the priority list shifts.
- **Refactoring while RED.** You lose the ability to distinguish "the refactor broke something" from "the test was already broken."
- **Skipping the planning step.** Without a prioritized behavior list, the cycles have no shape; the test suite ends up as a random walk.
- **Reusing test names from a different domain.** Use `<slug>/CONTEXT.md` vocabulary so the test reads like a specification in the project's own language.

## Quality gates (Phase 4 hand-off to QA)

When the TDD cycle completes for a feature/fix, the Specialist verifies:

- [ ] Every priority-list behavior has at least one test asserting on it through the public interface
- [ ] Test names use `<slug>/CONTEXT.md` vocabulary
- [ ] No test asserts on private state, mocks internal collaborators, or queries internal data stores directly
- [ ] All tests pass on the current implementation
- [ ] At least one refactor pass has run on the implementation while staying GREEN
- [ ] Any deep-module opportunities surfaced during refactor are documented in the Phase-4 hand-off (CQO will decide whether to act on them this phase or queue for `improve-codebase-architecture`)

CQO at Phase 4 spot-checks the test suite for the anti-patterns above. Failures route back through the never-give-up ladder per `RESILIENCE.md`.

## Interaction with other skills

| Skill | How `tdd` composes |
|---|---|
| `grill-with-docs` | Run before `tdd` when the public interface or priority-list behaviors are unclear. The grilling output (interface design + prioritized behavior list) is one input to `tdd`. |
| `improve-codebase-architecture` | Run after a TDD cycle if refactor surfaced deep-module opportunities that exceed the current cycle's scope. |
| `code-review` (existing engineering skill) | Reviews the diff produced by the TDD cycle. Check that tests assert on behavior, not implementation. |
| `incident-response` | Bug found in production gets a regression test FIRST (per the "regression test for a known bug" exception above), then the fix, then continues with normal priority-list. |
| `audit` (CAO close-audit) | Spot-checks that the test suite produced by TDD actually exercises behavior the User would notice. |

## Provenance

- **Kent Beck**, *Test-Driven Development: By Example* (Addison-Wesley, 2002) — origin of the red-green-refactor cycle.
- **Kent Beck**, *Extreme Programming Explained* (2nd ed., Addison-Wesley, 2004) — *"Invest in the design of the system every day"* (the principle that motivates step 4 refactoring).
- **John Ousterhout**, *A Philosophy of Software Design* (2nd ed., 2021) — deep-modules concept used in the planning step and refactor step.
- **Hunt & Thomas**, *The Pragmatic Programmer* (anniversary edition) — *"Always take small, deliberate steps. The rate of feedback is your speed limit."* (the principle that motivates vertical slicing over horizontal).
- The `mattpocock/skills` repository (MIT, 2026) is the curator that surfaced the strict-vertical-slice variant of TDD with the explicit horizontal-slicing anti-pattern callout to the Agency in the v0.6.1 cycle. The procedure above is Agency-original synthesis from the underlying primary sources.
