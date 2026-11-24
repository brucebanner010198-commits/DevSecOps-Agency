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

## 1. Record

Append the instruction to `_agency/change-requests.md` as `CR-<n>`, with:
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

## 3. Impact analysis (every class except "investigate")

Dispatch `devsecops-agency:engineering-lead`:
- **Task:** name the modules, tests, data and documents the change touches, from `_agency/system-map.md` and the code.
- **Output:** `_agency/cr/CR-<n>-impact.md`.

## 4. Run from the entry point

Run the agency's pipeline from the class's entry point to the end, as for new work:
- each phase's chief, gates and fix-loop rules apply;
- work lands on a branch;
- no push to a protected branch without the Chairman.

**The adoption baseline must hold.** A change that breaks a test which passed in `_agency/baseline/tests.md` is a red.

In the same change, update:
- `_agency/spec-as-is.md`;
- `_agency/system-map.md`;
- the repository's user documentation.

## 5. Close

Mark `CR-<n>` `done` (or `blocked`, with the reason) in `_agency/change-requests.md`, and link the branch, the tests and the gate results. Report to the Chairman in three lines.
