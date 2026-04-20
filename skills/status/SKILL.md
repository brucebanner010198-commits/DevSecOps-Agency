---
name: status
description: >
  This skill should be used when the user wants a quick text summary of the
  active DevSecOps Agency project — current phase, active agents, any blockers,
  and what just happened. Trigger phrases include "what's the status", "where
  are we", "quick update on the project", or /devsecops-agency:status. Prefer
  command-center for the visual view; status is for a terse in-chat summary.
metadata:
  version: "0.1.0"
---

# status — quick in-chat summary

Produce a 6-line summary of the active project. Do not open the artifact.

## Steps

1. Find the active project under `/sessions/loving-adoring-maxwell/mnt/outputs/devsecops-agency/` (the one with `status.phase != "delivered"`; most recently updated if multiple).
2. Read `status.json` and the last 5 entries of `chat.jsonl`.
3. Print, with nothing else:

```
📋 <projectSlug>
Phase:    <phase>   · completed: <comma-sep>
Active:   <activeAgents joined with commas>
Blockers: <count> — <first blocker question if any>
Last:     <last chat entry: "from → to · type · note">
```

4. If no active project, say "No active project." and stop.
5. If blockers > 0, suggest `/devsecops-agency:escalate` to handle them.
