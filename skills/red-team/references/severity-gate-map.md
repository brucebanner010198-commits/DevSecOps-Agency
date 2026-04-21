# severity-gate-map — red-team findings → gate signal

## Table

| Findings present                                   | Gate     |
|----------------------------------------------------|----------|
| ≥ 1 critical                                       | red      |
| ≥ 1 high, 0 critical                               | red      |
| ≥ 1 medium, 0 high, 0 critical                     | yellow   |
| low / info only                                    | green    |
| no findings AND coverage of applicable ASI = 100%  | green    |
| no findings AND coverage < 100% (any unjustified)  | yellow   |
| red-team skipped when mandatory                    | n/a (procedural red — CEO cannot advance) |

## Follow-ups requirement

- **Yellow:** every finding gets `owner` + `fix-by-phase`. Unassigned yellow = rejected.
- **Red:** every finding gets `owner` + ADR + Rung 3 task created. CEO cannot advance the phase until the taskflow task is acknowledged by the owner.

## Ladder routing

- Red → Rung 3 (cross-council escalation). Ladder files ADR.
- Rung 3 fix-loop exhaustion → Rung 4 (hire / repurpose via COO) only if the council doesn't have the skill.
- Rung 3 failure to fix a high-severity finding after two attempts → Rung 6 user consult (accept-without-fix waiver).
- Rung 6 accept-without-fix → ADR + user signature in `inbox.json` + permanent `<slug>/red-team/findings.md` note `waived: ADR-NNNN`.

## Special rule — prompt-upgrade red-team

A prompt-diff review that returns a reject does NOT map to a gate; it maps directly to **rollback**. The diff does not land. Rollback is automatic — no ladder, no ADR-to-negotiate, just revert. The ADR files the attempt + the reject.

## Special rule — incident red-team

An incident red-team always outputs an informational gate (`n/a` or `yellow` at most); the "gate" is the user's acceptance of the incident findings. The actual remediation goes through the owning council via standard taskflow.
