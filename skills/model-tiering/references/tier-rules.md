# tier-rules.md — per-agent model assignment

Floor tier per agent. Upgrades allowed per `SKILL.md > ## When to override`. Downgrades forbidden.

## Opus

| Agent | Rationale                                                                 |
| ----- | ------------------------------------------------------------------------- |
| ceo   | Single user voice; multi-phase orchestration; irreducible-decision triage. |

## Sonnet

| Agent              | Council       | Rationale                                                        |
| ------------------ | ------------- | ---------------------------------------------------------------- |
| cro                | Research      | Synthesises 4 specialists + names a wedge + emits gate.          |
| pm-lead            | Product       | Writes the spec from fragmented specialist inputs.               |
| engineering-lead   | Architecture + Execution | Dual-hat: trades off design choices, then leads build.  |
| security-lead      | Security      | STRIDE + OWASP judgement; blocking gate owner.                   |
| qa-lead            | Quality       | Test strategy across unit/integration/perf/a11y; blocking gate.  |
| devops-lead        | DevOps        | CI/CD + observability + runbooks; blocks ship on red.            |
| docs-lead          | Docs          | Narrative synthesis across README, API docs, tutorial.           |
| gc                 | Legal         | License + privacy judgement; blocking gate owner.                |
| skill-creator      | (cross-cut)   | Authors AGENTS.md-compliant personas and skills from scratch.    |

## Haiku (specialists)

| Agent                   | Council       | Artifact                                  |
| ----------------------- | ------------- | ----------------------------------------- |
| market-researcher       | Research      | `research/market.md`                      |
| tech-scout              | Research      | `research/tech-scan.md`                   |
| literature-reviewer     | Research      | `research/literature.md`                  |
| user-researcher         | Research      | `research/users.md`                       |
| spec-writer             | Product       | `product/spec.md`                         |
| product-strategist      | Product       | `product/strategy.md`                     |
| roadmap-planner         | Product       | `product/roadmap.md`                      |
| system-architect        | Architecture  | `architecture.md`                         |
| api-designer            | Architecture  | `architecture/api.md`                     |
| data-architect          | Architecture  | `architecture/data-model.md`              |
| infra-architect         | Architecture  | `architecture/infra.md`                   |
| threat-modeler          | Security      | `threat-model.md`                         |
| code-auditor            | Security      | `security/code-audit.md`                  |
| pen-tester              | Security      | `security/pentest-report.md`              |
| compliance-officer      | Security      | `security/compliance.md`                  |
| backend-dev             | Execution     | `src/` (backend)                          |
| frontend-dev            | Execution     | `src/` (frontend)                         |
| db-engineer             | Execution     | `src/` (migrations)                       |
| integrations-engineer   | Execution     | `src/` (3rd-party)                        |
| test-designer           | Quality       | `tests/` skeleton                         |
| test-runner             | Quality       | `qa-report.md`                            |
| performance-tester      | Quality       | `qa/perf-report.md`                       |
| a11y-auditor            | Quality       | `qa/a11y-report.md`                       |
| ci-engineer             | DevOps        | `deploy/ci.yml`                           |
| deployment-engineer     | DevOps        | `deploy/deploy.md`                        |
| observability-engineer  | DevOps        | `deploy/observability.md`                 |
| api-documenter          | Docs          | `docs/api.md`                             |
| readme-writer           | Docs          | `README.md`                               |
| tutorial-writer         | Docs          | `docs/tutorial/getting-started.md`        |
| license-checker         | Legal         | `legal/licenses.md`                       |
| privacy-counsel         | Legal         | `legal/privacy.md`                        |

## Override log

Runtime upgrades/downgrades are not edits to this file. They go to `references/override-log.md` as append-only entries, keyed by project slug.
