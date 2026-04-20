# Pipeline Stages — detailed spec

Each stage has a **lead**, **specialists**, **inputs**, **outputs**, and **exit criteria**. The lead is always responsible for the stage artifact; specialists contribute sections.

---

## 1. Intake

| Role       | Managing Director (the ship-it skill itself)          |
| ---------- | ------------------------------------------------------ |
| Inputs     | Raw user idea                                          |
| Outputs    | `brief.md` section `## Intake answers`                 |
| Exit       | All intake questions answered (by user or sensible default) |

## 2. PM

| Lead        | `pm-lead`                                               |
| ----------- | ------------------------------------------------------- |
| Specialists | `user-researcher`, `spec-writer`                        |
| Inputs      | `brief.md` (intake section)                             |
| Outputs     | Appends `## Personas`, `## Jobs to be done`, `## Functional spec`, `## Acceptance criteria`, `## Success metrics` to `brief.md` |
| Exit        | Acceptance criteria are testable (each has a pass/fail condition) |

## 3. Security (gate)

| Lead        | `security-lead`                                         |
| ----------- | ------------------------------------------------------- |
| Specialists | `threat-modeler` (now), `code-auditor` (stage 8)        |
| Inputs      | `brief.md`                                              |
| Outputs     | `threat-model.md` with STRIDE table + OWASP Top 10 coverage + mitigation plan |
| Exit        | Every Critical and High risk has an assigned mitigation; otherwise escalate |

## 4. Architecture

| Lead        | `engineering-lead`                                      |
| ----------- | ------------------------------------------------------- |
| Specialists | `api-designer`                                          |
| Inputs      | `brief.md`, `threat-model.md`                           |
| Outputs     | `architecture.md` covering tech stack, module layout, data model, API surface, deploy topology, how each mitigation is enforced |
| Exit        | Architecture references every acceptance criterion and every Critical/High mitigation |

## 5. Build

| Lead        | `engineering-lead`                                      |
| ----------- | ------------------------------------------------------- |
| Specialists | `backend-dev`, `frontend-dev` (dispatched in parallel when both apply) |
| Inputs      | `architecture.md`                                       |
| Outputs     | Code under `src/`, consistent with the architecture     |
| Exit        | Project builds / installs cleanly; smoke check passes   |

## 6. QA

| Lead        | `qa-lead`                                               |
| ----------- | ------------------------------------------------------- |
| Specialists | `test-designer`, `test-runner`                          |
| Inputs      | `brief.md` acceptance criteria, `src/`                  |
| Outputs     | `tests/` with unit + integration tests, `qa-report.md`  |
| Exit        | All acceptance criteria have at least one test; test suite passes or a failure is logged with a proposed fix |
| Fix loop    | If tests fail, hand back to `engineering-lead` (max 2 loops) |

## 7. Security — second pass

| Lead        | `security-lead`                                         |
| ----------- | ------------------------------------------------------- |
| Specialists | `code-auditor`                                          |
| Inputs      | Built code, `threat-model.md`                           |
| Outputs     | Appends `## Post-build audit` to `threat-model.md`       |
| Exit        | Zero Critical findings; any High has a ticket in `deploy/follow-ups.md` |
| Fix loop    | Criticals → hand back to `engineering-lead` (max 2 loops) |

## 8. DevOps

| Lead        | `devops-lead`                                           |
| ----------- | ------------------------------------------------------- |
| Specialists | `ci-engineer`, `deployment-engineer`                    |
| Inputs      | `src/`, `architecture.md`                               |
| Outputs     | `deploy/` with CI workflow, container/IaC, deploy checklist, rollback plan |
| Exit        | CI config runs the test suite and a security scan; deploy checklist has a rollback step |

## 9. Docs

| Lead        | `docs-lead`                                             |
| ----------- | ------------------------------------------------------- |
| Specialists | `api-documenter`, `readme-writer`                       |
| Inputs      | Everything                                              |
| Outputs     | `docs/` and a polished project `README.md`              |
| Exit        | README covers setup, run, test, deploy, troubleshooting |

## 10. Handoff

| Role   | Managing Director                                       |
| ------ | ------------------------------------------------------- |
| Inputs | All artifacts                                           |
| Outputs| Final chat summary + optional GitHub push               |
| Exit   | `status.json.phase = "delivered"`                       |
