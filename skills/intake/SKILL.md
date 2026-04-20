---
name: intake
description: >
  This skill should be used when the user wants the DevSecOps Agency to produce
  a project brief from an idea without kicking off the full engineering pipeline.
  Trigger phrases include "scope this idea", "help me flesh out this concept",
  "turn this into a spec", "just do the intake", or /devsecops-agency:intake.
  Runs intake Q&A and the PM team only, then stops and lets the user decide
  whether to continue with /devsecops-agency:ship-it.
metadata:
  version: "0.1.0"
---

# intake — scope without building

A lightweight alternative to the full `ship-it` pipeline. Run intake and the PM phase, stop there.

## Steps

1. Derive a project slug from the user's idea.
2. Create the project folder at `/sessions/loving-adoring-maxwell/mnt/outputs/devsecops-agency/<slug>/` if it does not exist.
3. Initialise `status.json` (phase = `pm`), `chat.jsonl`, `inbox.json`.
4. Run the intake Q&A batch (same as `ship-it`'s Step 2).
5. Dispatch `pm-lead` with the raw idea + intake answers.
6. Write `brief.md`.
7. Call the `command-center` skill to open the live artifact at `status.phase = "pm-delivered"`.
8. Tell the user the brief is ready and offer: continue with `/devsecops-agency:ship-it` (it will pick up the existing project folder and skip intake), or stop here.

## Re-entry

If `ship-it` is invoked later and finds an existing project folder with `brief.md` already populated, it should skip intake and PM and resume from the Security phase.
