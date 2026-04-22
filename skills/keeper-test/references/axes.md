# keeper-test/references/axes.md

The 4 scoring axes in detail. Thresholds in `KEEPER-TEST.md > ## Scoring axes`; this file adds derivation examples.

## Axis 1 — Gate hit rate

**Measure:** fraction of the agent's reports that landed with `gate: green` on first attempt within the review window.

**Data source:** `_sessions/<agent>/*.jsonl`, filter `type: "report"`, distinguish `fixAttempts: 0` (first attempt) from `fixAttempts > 0`.

**Thresholds:**

| Rating | First-attempt green rate |
| --- | --- |
| green | ≥ 85 % |
| yellow | 65 – 85 % |
| red | < 65 % |

**Minimum sample size:** 5 reports. Below 5 reports, skip this axis with `insufficient-sample — <n>/5`.

## Axis 2 — Fix-loop rate

**Measure:** fraction of the agent's tasks that required ≥ 1 fix-loop attempt.

**Data source:** `status.json > tasks[]`, filter `kind: "chief-dispatch"` for chiefs and `owner: <agent>` for specialists, read `fixAttempts` field.

**Thresholds:**

| Rating | Fix-loop rate |
| --- | --- |
| green | < 10 % |
| yellow | 10 – 25 % |
| red | > 25 %, **or** any attempt reached Rung 3+ per `skills/ladder` |

**Special case:** any Rung 3+ in the review window forces red on this axis, regardless of overall rate. Rung 3+ means the agent could not recover within the fix-loop cap on a specific task.

**Minimum sample size:** 5 tasks. Below 5 tasks, skip with `insufficient-sample`.

## Axis 3 — Audit findings

**Measure:** count + severity of CAO close-audit and portfolio-audit findings where the agent is cited as contributing to the finding.

**Data source:** `_vision/audit/*.md`, search for agent name in `## Findings` sections, read severity tag.

**Thresholds:**

| Rating | Audit findings |
| --- | --- |
| green | 0 findings |
| yellow | ≥ 1 finding, all severity `low` |
| red | ≥ 1 finding severity ≥ `medium` |

**Minimum sample size:** n/a — this axis can score on zero findings (green) but cannot skip.

## Axis 4 — Values compliance

**Measure:** whether the agent's reports cite specific values from `VALUES.md` when relevant, and whether any report violated a value.

**Data source:** `_sessions/<agent>/*.jsonl`, search for `VALUES.md §` citations in `note` fields; `_vision/audit/*.md` for violations; `_vision/playbooks/stones/*.md` for ASI-class stones where the agent was upstream.

**Thresholds:**

| Rating | Values compliance |
| --- | --- |
| green | agent cited at least one `VALUES.md §<n>` reference per 10 reports, **and** zero violations |
| yellow | inconsistent citation (< 1 per 10 reports), zero violations |
| red | **any** violation of any value — automatic red regardless of citation rate |

**Violation examples:**

- Writing a raw secret to a report (violates §7).
- Landing an agent-file edit without prompt-diff review (violates §10).
- A `git rm` on an ADR, session log, or agent file (violates §4).
- Skipping the ledger row at close (violates §11).

## Aggregation

Per-axis ratings combine into an overall rating:

| Overall | Rule |
| --- | --- |
| green (keep) | all 4 axes green |
| yellow (upgrade) | ≥ 1 yellow axis, 0 red axes |
| red (fire-or-repurpose) | ≥ 1 red axis on any axis |

**`insufficient-sample` treatment:** treat as n/a. An agent with < 5 reports and < 5 tasks cannot be graded on axes 1-2; the review defers to axes 3-4 only and notes "preliminary — re-review at next cadence."

## Worked example

Agent: `threat-modeler`. Window: 2026-01-01 → 2026-03-31 (quarter).

| Axis | Data | Rating |
| --- | --- | --- |
| Gate hit rate | 11 reports, 9 first-attempt green = 82 % | yellow |
| Fix-loop rate | 11 tasks, 2 required fix-loops = 18 % | yellow |
| Audit findings | 0 findings | green |
| Values compliance | cited `VALUES.md §2` twice, `§7` once; 0 violations | green |

Overall: **yellow → prompt upgrade**. Action: COO commissions a prompt-upgrade for `agents/security/threat-modeler.md` focused on lifting the gate hit rate above 85 %.

## Counter-example (red)

Agent: `hypothetical-specialist`. Window: 2026-Q1.

| Axis | Data | Rating |
| --- | --- | --- |
| Gate hit rate | 12 reports, 6 first-attempt green = 50 % | red |
| Fix-loop rate | 12 tasks, 5 fix-loops, 1 Rung-3 escalation | red |
| Audit findings | 1 finding, severity `medium` | red |
| Values compliance | wrote a raw secret to a report (2026-02-14) | red |

Overall: **red → fire-or-repurpose**. COO proposal via `hiring-lead` → CEO → `inbox.json` → user-meeting. User-only fire decision.
