# audit-matrix.md — what each auditor checks

One row per check. Auditors execute every row in scope; no sampling on machine-checkable rows.

## adr-auditor rows

| Row | Check | Evidence source | Severity |
| --- | --- | --- | --- |
| A1 | Every scope:decision chat entry → matching ADR | `<slug>/chat.jsonl` vs `_decisions/` | red |
| A2 | Every mandatory trigger fired → ADR filed | `skills/adr/references/decision-triggers.md` vs `_decisions/` | red |
| A3 | Accepted body checksum unchanged since acceptance | `git blame` vs current | red (always) |
| A4 | Supersede chain complete (no orphan `status: superseded`) | ADR headers | red |
| A5 | ADR numbering gap-free | `_decisions/ADR-*.md` sorted | yellow |
| A6 | No `status: proposed` for > 14 days | ADR header + date | yellow |

## gate-auditor rows

| Row | Check | Evidence source | Severity |
| --- | --- | --- | --- |
| G1 | Every `type: report` carries `gate` field ∈ {green, yellow, red, n/a} | `chat.jsonl` | red |
| G2 | Every report carries `okr_alignment` | `chat.jsonl` | red |
| G3 | Every yellow has non-empty `followups[]` | `chat.jsonl` | red |
| G4 | Every red has ≥ 2 citations | `chat.jsonl` | yellow |
| G5 | Blocking-council red shipped unwaived? | `inbox.json` waivers vs phase advance | red (always) |
| G6 | Phase-gate aggregation matches formula | `gates/references/gate-rules.md` vs `status.json` | red |

## okr-auditor rows

| Row | Check | Evidence source | Severity |
| --- | --- | --- | --- |
| O1 | Every report `okr_alignment` rederives via worst-of-3 | `okr/references/scoring-rules.md` | red on mismatch |
| O2 | Every report cites ≤ 3 KR IDs from active set | `_vision/VISION.md > ## OKRs` status:active | yellow on stale-KR |
| O3 | Per-project OKRs derived in `_vision/projects/<slug>.md` | file exists + ≥ 1 KR | red if missing |
| O4 | `okr_alignment: red` escalated to user with ADR? | `chat.jsonl` scope:escalation + ADR | red (always) |
| O5 | No report aligned green with artifact path touching non-goal | `_vision/VISION.md > ## Non-goals` | red |
| O6 | Orphan KR check (0 citations in window) | aggregate on KRs | yellow → CSO signal |

## memory-auditor rows

| Row | Check | Evidence source | Severity |
| --- | --- | --- | --- |
| M1 | Append-only: no `_memory/` or `_sessions/` line rewritten | `git blame` | red (always) |
| M2 | Every memory bullet cites `file:line` or `file:§section` | grep for trailing cite | yellow |
| M3 | PII/secret pattern scan | regex (SSN, email, bearer, sk-, ghp_, AKIA...) | candidate → human review |
| M4 | Novelty-gate block present on every memory write | `_sessions/*.jsonl` for novelty:{} | yellow (Light) / red (Deep + REM) |
| M5 | Pattern-drift: cited file:line still contains the claim | grep target file | yellow |
| M6 | Structured-rewrite exception only on VISION.md or ADR status header | rewrite location | red if elsewhere |

## Aggregation

- Every **red** in the table above → CAO report `gate: red` unless waived with user signature.
- Every **yellow** → taskflow task with owner. Yellow-without-task = CAO yellow upgraded to red.
- Rows marked "red (always)" cannot be waived by the CEO. Only the user can waive them via `inbox.json`.
- Machine-checkable rows (A3, G1, G2, G3, G6, O1, M1) walk every entry. No sampling.

## Portfolio amplifier

Cross-project consistency at portfolio audit:

- Same finding ID appearing in ≥ 2 close audits within a quarter → upgrade severity one step.
- Same agent named in ≥ 3 findings across the quarter → COO roster flag with citations.
- Any `supersede` chain longer than 3 on a single topic → CSO review (strategy instability signal).
