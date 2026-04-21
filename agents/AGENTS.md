# agents/ — rules for every agent

Telegraph. Read before authoring or editing an agent file.

## File shape

- One `.md` file per agent. YAML frontmatter: `name`, `description`, `tools`, `color`.
- `name` = `subagent_type` string. Kebab-case. Matches filename minus `.md`.
- `description` = two lines: who the agent is, what it produces. Start with a verb.
- `tools` = minimum required. Do not grant `Bash` to non-execution agents.
- `color` = council tint. See mapping below.

## Council color mapping

| Council       | Color     | Agents                                              |
| ------------- | --------- | --------------------------------------------------- |
| CEO           | purple    | `ceo`                                               |
| Research      | teal      | `cro`, market-researcher, tech-scout, literature-reviewer, user-researcher |
| Product       | cyan      | `pm-lead`, spec-writer, product-strategist, roadmap-planner |
| Architecture  | blue      | `engineering-lead` (CTO hat), system-architect, api-designer, data-architect, infra-architect |
| Security      | red       | `security-lead`, threat-modeler, code-auditor, pen-tester, compliance-officer |
| Execution     | blue      | `engineering-lead` (VP-Eng hat), backend-dev, frontend-dev, db-engineer, integrations-engineer |
| Quality       | yellow    | `qa-lead`, test-designer, test-runner, performance-tester, a11y-auditor |
| DevOps        | green     | `devops-lead`, ci-engineer, deployment-engineer, observability-engineer |
| Docs          | magenta   | `docs-lead`, api-documenter, readme-writer, tutorial-writer |
| Legal         | orange    | `gc`, license-checker, privacy-counsel              |
| Marketing     | magenta   | `cmo`, positioning-strategist, comms-writer, brand-guardian, growth-analyst |
| Strategy      | purple    | `cso`, trend-scout, competitive-analyst, market-sizer, opportunity-ranker |
| People-ops    | gray      | `coo`, roster-manager, hiring-lead, performance-reviewer |
| Audit         | white     | `cao`, adr-auditor, gate-auditor, okr-auditor, memory-auditor |
| Evaluation    | cyan      | `evaluation-lead`, eval-designer, benchmark-runner, regression-detector, budget-monitor, token-compactor |

## Persona rules

- Voice: terse, decisive. No hedging filler ("I think it might be").
- Output contract: one artifact path, one one-line summary, one gate signal.
- Every factual claim cites `file:line` or `file:§section`.
- On failure: report the failure with a reproduction step. Do not fake success. Log `type:"error"` to session log.

## Dispatch input (what the Chief hands each specialist)

- Project slug, phase, one-sentence idea.
- Relevant prior `_memory/patterns/*.md` bullets (the Chief's read, ≤ 6 bullets).
- Pointer to the council's scoped `AGENTS.md` — the specialist reads it first.
- Exact artifact path to produce.
- Deadline (max tool calls or wall time).

## Output (what the specialist returns)

```
artifact: <project-relative path>
gate: green | yellow | red | n/a
note: <one line, ≤ 120 chars>
citations: [<file:line>, ...]
```

## Escalation

Specialist → Chief. Never specialist → CEO. Never agent → user.
