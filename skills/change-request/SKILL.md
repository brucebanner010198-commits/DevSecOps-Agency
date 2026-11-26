---
name: change-request
description: >
  This skill should be used when the Chairman gives an instruction about a
  repository the agency has already adopted (the adoption report was
  approved): add, change, redesign, remove, fix, update, or investigate.
  Trigger phrases include "add a feature", "remove the export", "fix this
  bug", "update the dependency", or /devsecops-agency:change-request. It
  records the instruction as a change request with an id, classifies it,
  and enters the pipeline at the stage the class requires (plan Part 6,
  "Change requests").
metadata:
  version: "0.1.0"
---

# change-request — route an instruction on an adopted repository

Use only after `adopt` has finished and the Chairman approved the adoption report. Records live in `_agency/`, as in `adopt`.

## 0. Precondition: commit drift

Run `adopt`'s re-entry check first (`skills/adopt/SKILL.md > ## Re-entry`). If the repository changed outside the agency since the recorded commit, re-map the changed files and record the new commit before this change request goes any further.

## 1. Record

`_agency/change-requests.md` is append-only (the guard enforces it). Every update is a new row; no row is edited in place.

Append the instruction as `CR-<n>`, with:
- the Chairman's words, verbatim;
- the date;
- the class from step 2;
- the status `open`.

## 2. Classify

| Class | Enters at | Extra requirements before work | The Chairman decides |
| --- | --- | --- | --- |
| Add a feature | Product (G1/G2) | Impact analysis; fits the architecture or goes to Architecture (G3) | Scope and priority |
| Change or redesign a feature | Product (G2) | Design review; migration of existing behaviour and data | Direction, if it departs from what was approved |
| Redesign the interface | Product (G2) with design | Prototype first; accessibility check | The new direction |
| Remove a feature | Product (G2) | Dependents found; data and user impact stated; deprecation plan | The removal, and any data deletion |
| Rework the architecture | Architecture (G3) | Migration and rollback plan | An irreversible or significant redesign |
| Fix a bug | Build (G5) | A failing test that reproduces it, first | Only if intended behaviour changes |
| Update a dependency or patch a vulnerability | Build (G5) | Changelog read; regression run | Only for major trade-offs |
| Investigate or answer a question | None | A report with evidence; no code change | Nothing |

If two classes fit, take the one that enters earlier.

**Classification audit.** The CEO decides the class. Before any work starts, dispatch `devsecops-agency:cao` to audit that decision against the Chairman's words; CAO does not choose the class (CONSTITUTION §3.5). Output: `_agency/cr/CR-<n>-class-audit.md`. If the audit finds the class wrong, the item goes to the Chairman and the change request waits.

**Dependency changes.** Every dependency change, in any class, is reviewed by `devsecops-agency:security-lead` before it lands. Output: `_agency/cr/CR-<n>-security.md`. This holds even though the class enters at Build (G5).

## 3. Impact analysis (every class except "investigate")

Dispatch `devsecops-agency:engineering-lead`:
- **Task:** name the modules, tests, data and documents the change touches, from `_agency/system-map.md` and the code.
- **Output:** `_agency/cr/CR-<n>-impact.md`.

## 4. Run from the entry point

Run the agency's pipeline from the class's entry point to the end, as for new work:
- each phase's chief, gates and fix-loop rules apply;
- work lands on a branch;
- no push, merge or publish without the Chairman (CONSTITUTION §2.2 clause 7).

**The adoption baseline must hold.** `devsecops-agency:evaluation-lead` (CEVO) owns the check, through `regression-detector`. It compares the change against every adoption baseline: `_agency/baseline/tests.md`, `security-scan.md`, `licenses.md` and `integrity.md`. Output: `_agency/cr/CR-<n>-baseline.md`. Anything that was passing and now fails is a CEVO red (CONSTITUTION §3.3).

In the same change, update, each through its chief:
- `_agency/spec-as-is.md`, by `spec-writer` (through `pm-lead`);
- `_agency/system-map.md`, by `legacy-code-specialist` (through `architecture-lead`);
- the repository's user documentation, by `docs-lead`.

## 5. Close

Append a row for `CR-<n>` to `_agency/change-requests.md`:
- `done` only if no gate is red. Link the branch, the tests and the gate results.
- Otherwise `blocked`, with the reason and the red gate.

Report to the Chairman in three lines.
