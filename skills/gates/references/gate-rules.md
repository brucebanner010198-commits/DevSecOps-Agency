# Per-council gate rules

Authoritative matrix. Each row is an individual Must / Must-not item pulled from the council's `AGENTS.md`. Each has a trigger severity (what color it produces when tripped) and whether it **blocks** the ship (blocking-council) or only **informs** it (informing-council).

This file is the reference the CEO consults when a Chief report is ambiguous. If a condition matches more than one row, take the **worst** severity.

## Blocking councils

### Security (CISO) — blocking

| Trigger                                                             | Severity | Gate  |
| ------------------------------------------------------------------- | -------- | ----- |
| Critical STRIDE/OWASP item with no mitigation plan                  | critical | red   |
| High STRIDE/OWASP item with no mitigation plan                      | high     | red   |
| Medium STRIDE item with documented mitigation + test                | medium   | yellow|
| Hardcoded secret found in `src/` during code-audit                  | critical | red   |
| PII not classified in `architecture/data-model.md`                  | high     | red   |
| `compliance-officer` missing signoff for restricted jurisdiction    | critical | red   |
| Dependency audit skipped in CI                                      | high     | red   |

### Legal (GC) — blocking

| Trigger                                                             | Severity | Gate  |
| ------------------------------------------------------------------- | -------- | ----- |
| GPL/AGPL dependency in a closed-source ship                         | critical | red   |
| `PRIVACY.md` missing when PII is in data model                      | critical | red   |
| PII classification disagrees with `architecture/data-model.md`      | high     | red   |
| MPL/LGPL dependency with documented dynamic-linking caveat          | low      | yellow|
| License text not checked (package name ≠ verdict)                   | high     | red   |

## Informing councils

### Research (CRO) — informing

| Trigger                                                     | Severity | Gate  |
| ----------------------------------------------------------- | -------- | ----- |
| Can't articulate a defensible wedge                         | high     | red   |
| Unverified source cited                                     | medium   | yellow|
| Invented quote or statistic                                 | critical | red   |

### Product (CPO) — informing

| Trigger                                                     | Severity | Gate  |
| ----------------------------------------------------------- | -------- | ----- |
| `Now` list has > 5 items                                    | high     | red   |
| Success metric missing or unmeasurable                      | high     | red   |
| Spec skips user rights (DSAR / deletion / export)           | high     | red   |
| Acceptance criteria missing on a spec row                   | medium   | yellow|

### Architecture (CTO) — informing

| Trigger                                                     | Severity | Gate  |
| ----------------------------------------------------------- | -------- | ----- |
| Any column missing PII classification                       | high     | red   |
| Circular service dependency in the diagram                  | high     | red   |
| Cost model missing on infra doc                             | medium   | yellow|
| No ADR for a non-obvious tech choice                        | medium   | yellow|

### Execution (VP-Eng) — informing

| Trigger                                                     | Severity | Gate  |
| ----------------------------------------------------------- | -------- | ----- |
| String-concatenated SQL in `src/`                           | critical | red   |
| Secret committed to tree                                    | critical | red   |
| API shape drift from `api-designer` spec                    | high     | red   |
| Migration missing `down` step                               | medium   | yellow|
| Integration without a mock                                  | low      | yellow|

### Quality (CQO) — informing

| Trigger                                                     | Severity | Gate  |
| ----------------------------------------------------------- | -------- | ----- |
| Failing test in the suite                                   | critical | red   |
| Branch coverage on business logic < 70% (no CEO waiver)     | high     | red   |
| Missing coverage on a mitigated threat                      | high     | red   |
| Perf p95 regression > 2x baseline                           | high     | red   |
| a11y critical (keyboard trap, no labels on form)            | high     | red   |
| Flaky test (passes 4/5)                                     | medium   | yellow|
| a11y medium (contrast near-miss) with ticket                | low      | yellow|

### DevOps (VP-Ops) — informing

| Trigger                                                     | Severity | Gate  |
| ----------------------------------------------------------- | -------- | ----- |
| No rollback plan                                            | critical | red   |
| `:latest` tag in prod config                                | critical | red   |
| Secret logged unredacted                                    | critical | red   |
| No CI on the repo                                           | critical | red   |
| One non-critical log field unredacted                       | medium   | yellow|
| Observability thin but functional                           | low      | yellow|

### Docs (CKO) — informing

| Trigger                                                     | Severity | Gate  |
| ----------------------------------------------------------- | -------- | ----- |
| Tutorial does not produce a visible result in 10 minutes    | high     | red   |
| Documented feature not in code                              | critical | red   |
| Placeholder text in shipped docs                            | high     | red   |
| API section missing one endpoint                            | medium   | yellow|
| Tutorial has one unverified step                            | medium   | yellow|

## Applying the matrix

1. When a Chief reports, map every `note` + `followup` against its council's rows.
2. Take the worst-matching row. Its `Gate` is the report gate.
3. If the worst row is `red` and the council is **blocking**, project aggregate immediately goes `red` unless waived by the user.
4. If the worst row is `red` and the council is **informing**, the CEO may waive it after logging user consent in `inbox.json`.
5. Never emit a gate not found in this matrix. Add a row here first.
