---
name: compliance-drift
description: Detect drift between declared compliance posture (SOC 2, GDPR, HIPAA, state privacy) and observed practice. Runs monthly + on-demand when CLO flags an incoming audit. Drift = early warning; breach = finding. Both get reported. Owned by compliance-drift specialist on the Legal Council.
metadata:
  version: 0.3.0
---

# compliance-drift

Auditors find gaps eventually. We find them first.

## When to use

- Monthly cadence across all active compliance frameworks.
- On-demand when CLO hears of an incoming audit.
- After any incident that may have exposed a control (e.g. secrets leak → access-review drift check).
- Quarterly paired with CAO's portfolio audit.

## Process

1. **Identify scope** — which framework (SOC 2 Type 2, GDPR, HIPAA, state privacy, custom).
2. **Pull rubric version** — version-pin the rubric file (`references/rubrics/<framework>-v<n>.md`).
3. **Gather evidence** for each control:
   - Logs: audit, access, secrets-vault, incident response.
   - Taskflow: rotation cadence, access-review completion, training attendance.
   - ADR history: exceptions, waivers.
4. **Diff declared vs observed**:
   - **Compliant** — control active + evidence matches. Green.
   - **Drift** — practice diverges; no breach yet. Yellow + remediation task.
   - **Breach** — control violated. Red + ADR + CAO notify + user consult if material.
5. **Report** — `_vision/legal/<date>-compliance-drift.md`.
6. **File remediation taskflow** for every yellow + red.

## Output shape

```markdown
# Compliance drift — <date>

## Framework scope
- <framework> · rubric v<n>

## Results
| Control | Status | Evidence | Remediation |
| ... | ... | ... | ... |

## ADRs filed
- ADR-NNNN: <title>

## Taskflow
- [task-id] <remediation> — <owner>
```

## ADR triggers

- Every breach.
- Every rubric-version upgrade.
- Every scope amendment (adding / removing a framework).
- Every waiver accepted.

## Invariants

- Drift and breach are distinct.
- Breach files an ADR same-turn.
- Evidence is linkable.
- Rubric is version-pinned per report.
- Reports stay separate from red-team findings.

## What never happens

- Hide drift because it's small.
- Self-certify.
- Third-party auditor templates dropped in without ADR.
- Skipping a control because "we don't do that anymore".
- Merging drift with red-team findings.
