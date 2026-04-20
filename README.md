# DevSecOps Agency

A plugin that turns Claude into a fully autonomous AI software-development company. You hand the **CEO** a one-sentence idea; the CEO convenes a board of 9 Chiefs; each Chief runs a council of specialists. Research, Product, Architecture, Security, Execution, Quality, DevOps, Docs, Legal. Security-first (STRIDE + OWASP Top 10). Ships to GitHub.

You speak only to the CEO. Everything else is internal.

A live **command center** artifact shows the org chart, every board and council meeting, every handoff, every artifact, and any blocker parked for you.

---

## The organisation

```
                                    USER
                                     │
                                     ▼
                         ┌──────────────────────┐
                         │         CEO          │  ← only one you talk to
                         └──────────┬───────────┘
    ┌────────┬──────────┬───────────┼───────────┬────────┬─────────┬────────┬────────┐
    ▼        ▼          ▼           ▼           ▼        ▼         ▼        ▼        ▼
  CRO      CPO       CTO         CISO        VP-Eng     CQO     VP-Ops    CKO       GC
Research Product  Architecture  Security   Execution  Quality   DevOps    Docs    Legal
```

| Council       | Chief (agent)        | Specialists                                                                 |
| ------------- | -------------------- | --------------------------------------------------------------------------- |
| Research      | `cro`                | market-researcher, tech-scout, literature-reviewer, user-researcher         |
| Product       | `pm-lead` (CPO)      | spec-writer, product-strategist, roadmap-planner                            |
| Architecture  | `engineering-lead` (CTO) | system-architect, api-designer, data-architect, infra-architect          |
| Security      | `security-lead` (CISO)   | threat-modeler, code-auditor, pen-tester, compliance-officer             |
| Execution     | `engineering-lead` (VP-Eng) | backend-dev, frontend-dev, db-engineer, integrations-engineer         |
| Quality       | `qa-lead` (CQO)      | test-designer, test-runner, performance-tester, a11y-auditor                |
| DevOps        | `devops-lead` (VP-Ops)   | ci-engineer, deployment-engineer, observability-engineer                 |
| Docs          | `docs-lead` (CKO)    | api-documenter, readme-writer, tutorial-writer                              |
| Legal         | `gc`                 | license-checker, privacy-counsel                                            |

**1 CEO + 9 Chiefs + ~28 specialists.** Each specialist does one thing well and hands their artifact up to the Chief, who consolidates and reports to the CEO.

## Skills (slash commands)

| Command                              | What it does                                                                                  |
| ------------------------------------ | --------------------------------------------------------------------------------------------- |
| `/devsecops-agency:ceo`              | **Main entry point (v0.2)**. Adopts the CEO persona. Convenes the board, runs all 7 phases. |
| `/devsecops-agency:ship-it`          | Lean v0.1 pipeline (6-team hierarchy). Still supported.                                       |
| `/devsecops-agency:command-center`   | Opens (or refreshes) the live status artifact.                                                |
| `/devsecops-agency:board-meeting`    | Re-run a specific board phase (power-user).                                                   |
| `/devsecops-agency:council-meeting`  | Re-run a specific council (power-user).                                                       |
| `/devsecops-agency:intake`           | Run intake Q&A only — produces a project brief without kicking off engineering.               |
| `/devsecops-agency:status`           | Quick text summary of the active project.                                                     |
| `/devsecops-agency:escalate`         | Process the human-input queue: surface parked questions, capture answers, resume pipeline.    |
| `/devsecops-agency:retro`            | Post-deploy retrospective — what went well, what to fix, follow-up tickets.                   |

## Quick start

```
/devsecops-agency:ceo I want a secure invoice-splitting web app for roommates
```

The CEO will ask 3–5 short questions (tech preference, deployment target, constraints), then run everything autonomously. Open `/devsecops-agency:command-center` at any time to watch.

## The 7 phases

```
Phase 1  Discovery       CRO + CPO           (parallel)
Phase 2  Design          CTO → CISO          (sequential; CISO reviews)
Phase 3  Build           VP-Eng
Phase 4  Verify          CQO + CISO²         (parallel)
Phase 5  Ship            VP-Ops
Phase 6  Document+Legal  CKO + GC            (parallel)
Phase 7  Close           CEO
```

Each phase has an **exit criterion** (see `skills/ceo/references/board-phases.md`). No Critical/High unmitigated risk ever gets past CISO.

## Output

Each project gets its own folder under the Cowork outputs directory:

```
outputs/devsecops-agency/<project-slug>/
├── brief.md                    # CEO's intake + decisions
├── research-brief.md           # CRO output
├── research/                   # market, tech-landscape, prior-art, user-needs
├── product/                    # strategy.md, roadmap.md
├── architecture.md             # CTO output
├── architecture/               # data-model.md, infra.md
├── threat-model.md             # CISO output (STRIDE + OWASP)
├── security/                   # compliance.md, code-audit.md, pentest-report.md
├── src/                        # VP-Eng output — the actual code
├── tests/                      # CQO output
├── qa-report.md, qa/           # test results, perf, a11y
├── deploy/                     # VP-Ops output — CI, container, rollback, observability
├── docs/                       # CKO output — README, API, tutorial
├── legal/                      # GC output — licenses.md, privacy.md
├── status.json                 # Pipeline state (read by the command-center)
├── chat.jsonl                  # Board + council meeting log
└── inbox.json                  # Parked human questions
```

If a GitHub connector is present, the plugin will offer to push to a fresh repo at the end.

## Security posture

Default gate: **full STRIDE threat model + OWASP Top 10 coverage** before any code is written, plus a second-pass **code audit + pen-test** after build. CISO blocks the pipeline if any Critical/High risk has no mitigation plan. Compliance posture (GDPR / CCPA / PCI / HIPAA as applicable) is scanned by `compliance-officer`. License compatibility and privacy posture are gated by the GC before public release. See `skills/ship-it/references/owasp-checklist.md`.

## Files of interest

- `skills/ceo/SKILL.md` — the v0.2 orchestrator playbook
- `skills/ceo/references/board-phases.md` — exact phase inputs/outputs/exit criteria
- `skills/ceo/references/meeting-log-format.md` — chat.jsonl entry types
- `skills/board-meeting/SKILL.md` — CEO ↔ Chief meeting contract
- `skills/council-meeting/SKILL.md` — Chief ↔ specialist meeting contract
- `skills/command-center/references/artifact-template.html` — live HTML view
- `skills/ship-it/references/owasp-checklist.md` — security gate rules
- `skills/ship-it/references/status-schema.md` — status.json schema (v0.2 + v0.1)
- `skills/ship-it/references/escalation-rules.md` — when a Chief must escalate

## Versions

- **0.2.0** — CEO + 9 councils + ~28 specialists. 7-phase board. Command center shows meetings by scope.
- **0.1.0** — 6-team hierarchy. 10-stage pipeline. Still runnable via `ship-it`.
