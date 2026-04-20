---
name: retro
description: >
  This skill should be used when the user wants a post-deploy retrospective
  of the latest DevSecOps Agency project — what went well, what to fix, and
  concrete follow-up tickets. Trigger phrases include "run a retro", "what
  could we have done better", "post-mortem this project", or
  /devsecops-agency:retro. Expects a delivered project with all artifacts
  present.
metadata:
  version: "0.1.0"
---

# retro — post-deploy retrospective

Generate a retrospective for the most recently delivered project.

## Steps

1. Find the most recent project under `/sessions/loving-adoring-maxwell/mnt/outputs/devsecops-agency/` with `status.phase == "delivered"`.
2. If none, say "No delivered project to retrospect." and offer `/devsecops-agency:status`.
3. Read `status.json`, `chat.jsonl`, `threat-model.md`, `qa-report.md`, `deploy/follow-ups.md`.
4. Synthesise a retrospective into `retro.md` in the project folder with this structure:

```markdown
# Retrospective — <projectSlug>

## What went well
- <3–5 specific wins, grounded in the logs>

## What to improve
- <3–5 friction points or recurring issues, with file references>

## Metrics
- Handoffs: <N>   · Fix loops: <N>   · Escalations: <N>
- Time in each phase: <table>

## Follow-ups
<Structured list of actionable items. For each:>
- [ ] <title>  —  <why>  —  owner: <team>  —  priority: P0|P1|P2

## Residual risks
<Copy from threat-model.md "Residual risks" + any High/Medium findings from code-auditor>
```

5. If a project tracker connector is available (Linear/Jira/Asana), offer to create tickets from the `## Follow-ups` list.
6. Refresh the command-center artifact to show the retro link in the Artifacts panel.
