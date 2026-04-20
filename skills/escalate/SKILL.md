---
name: escalate
description: >
  This skill should be used when the user wants to answer questions that the
  DevSecOps Agency agents have parked in the human-input queue, or when the
  user wants to pause the pipeline to override a decision. Trigger phrases
  include "answer agent questions", "clear the inbox", "unblock the pipeline",
  "what are the agents waiting on me for", or /devsecops-agency:escalate. Also
  called internally by ship-it when a blocker is raised.
metadata:
  version: "0.1.0"
---

# escalate — process the human-input queue

Surfaces any open questions in the active project's `inbox.json`, captures answers, and resumes the pipeline.

## Steps

1. Locate the active project. If none, say so and exit.
2. Read `inbox.json`. If `open` is empty, print "No open questions. Agents are running autonomously." and exit.
3. For each question in `open`, present it to the user via AskUserQuestion:
   - Question text from `q.question`
   - Options from `q.options` if present (otherwise allow free-form answer via the Skip/Other field)
4. On each answer:
   - Move the entry from `open` to `answered` with `answer` and `answeredAt` fields.
   - Append `{"ts":"<iso>","from":"human","to":"<raisedBy>","type":"resume","note":"answered: <brief>"}` to `chat.jsonl`.
   - Clear this blocker id from `status.json.blockers`.
5. After all questions handled:
   - If `status.phase` was previously `blocked`, restore it to the phase the pipeline was in when it blocked (stored in `status.blockedFromPhase`).
   - Call the `command-center` skill to refresh the artifact.
   - Re-dispatch the lead of the current phase with the new context so the pipeline resumes automatically.

## Override mode

If the user invokes `/devsecops-agency:escalate override` or similar, let them inject a new instruction/question into the active phase without waiting for an agent-raised blocker. Write their instruction as a synthetic inbox entry with `raisedBy: "human-override"`, then immediately mark it answered and re-dispatch.
