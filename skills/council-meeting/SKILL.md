---
name: council-meeting
description: >
  This skill should be used when a Chief needs to hold a council meeting with
  their specialists — dispatching work to the council, collecting results, and
  consolidating into the Chief's board report. Trigger phrases include "run the
  research council", "convene the engineering council", "dispatch specialists",
  "council review". Also trigger when invoked as /devsecops-agency:council-meeting.
  Not a user-facing skill — Chiefs use it internally; advanced users may invoke
  to re-run a council (e.g., re-run the Security council after a code change).
metadata:
  version: "0.2.0"
---

# council-meeting — structured Chief-to-specialist orchestration

This skill enforces the contract between a Chief and their specialists.

## When to use

Called by any Chief at the start of their phase work. Can also be invoked directly if the user wants to rerun just one council.

## Councils

| Council       | Chief              | Specialists                                                     |
| ------------- | ------------------ | --------------------------------------------------------------- |
| Research      | `cro`              | market-researcher, tech-scout, literature-reviewer, user-researcher |
| Product       | `pm-lead`          | spec-writer, product-strategist, roadmap-planner                |
| Architecture  | `engineering-lead` | system-architect, api-designer, data-architect, infra-architect |
| Security      | `security-lead`    | threat-modeler, code-auditor, pen-tester, compliance-officer    |
| Execution     | `engineering-lead` | backend-dev, frontend-dev, db-engineer, integrations-engineer   |
| Quality       | `qa-lead`          | test-designer, test-runner, performance-tester, a11y-auditor    |
| DevOps        | `devops-lead`      | ci-engineer, deployment-engineer, observability-engineer        |
| Docs          | `docs-lead`        | api-documenter, readme-writer, tutorial-writer                  |
| Legal         | `gc`               | license-checker, privacy-counsel                                |

## Process

1. **Open the council.** Append to `chat.jsonl`:
   ```json
   {"ts":"<iso>","scope":"council","council":"<name>","from":"<chief>","to":"council","type":"dispatch","note":"<agenda>"}
   ```

2. **Dispatch specialists** (parallel whenever there are no intra-council dependencies). Use the Task tool, one call per specialist. Prompt must include:
   - Project folder path
   - Specific input artifacts (by filename)
   - Expected output artifact (by filename)
   - One-line success criterion

3. **Collect outputs.** Each specialist returns a 3-bullet summary. Append:
   ```json
   {"ts":"<iso>","scope":"council","council":"<name>","from":"<specialist>","to":"<chief>","type":"report","artifacts":[...],"note":"<summary>"}
   ```

4. **Chief consolidates.** The Chief reads the specialists' artifacts (not just the summaries), resolves conflicts, writes the Chief-level artifact (e.g., `research-brief.md`, `threat-model.md`, `architecture.md`), and sets the council gate signal.

5. **Close the council.** Append:
   ```json
   {"ts":"<iso>","scope":"council","council":"<name>","from":"<chief>","to":"council","type":"board-decision","gate":"<g/y/r>","note":"<one line>"}
   ```

6. Chief is now ready to report up to the CEO.

## Parallelism rules

- Specialists producing **independent** artifacts → parallel
- Specialists where one reads another's output → sequential
  - e.g., in Research: market-researcher → tech-scout → literature-reviewer can all be parallel. user-researcher also parallel.
  - In Architecture: system-architect first, then data-architect + api-designer + infra-architect in parallel (they depend on the system shape).
  - In Security: threat-modeler first (on the design); code-auditor + pen-tester later (on the code).
  - In Execution: backend-dev + frontend-dev + db-engineer + integrations-engineer parallel once data model is set.

## What you never do

- Dispatch specialists without reading the Chief-level brief yourself first
- Copy a specialist's output as your Chief-level artifact — you synthesise
- Skip the council-close entry — the command center shows council progress
