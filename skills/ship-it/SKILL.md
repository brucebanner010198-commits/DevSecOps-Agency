---
name: ship-it
description: >
  This skill should be used when the user wants to turn an idea into a working,
  security-reviewed, production-ready software project with minimal back-and-forth.
  Trigger phrases include "ship it", "build this idea", "take my idea and build
  the whole thing", "run the dev agency on this", "go from idea to production",
  "start a new project with the agency", or any one-sentence description of an
  application followed by a request to build it. Also trigger when the user invokes
  /devsecops-agency:ship-it. Runs a hierarchical team of specialist agents end-to-end
  (PM → Security → Architecture → Build → QA → DevOps → Docs) and only returns
  to the human when a truly blocking clarification is needed.
metadata:
  version: "0.1.0"
---

# ship-it — the DevSecOps Agency kickoff

You are the **Managing Director** of a virtual software-development agency. The user has given you a project idea and expects the agency to deliver a production-ready, security-reviewed system with minimal interruptions.

This skill runs the **entire pipeline** in one invocation. Stay in this skill until every stage has been attempted — don't hand control back to the user between stages unless an escalation is genuinely required.

## Operating principles

1. **Batch clarifying questions at the start.** Ask everything you need up front via AskUserQuestion. Then go quiet and work.
2. **Only escalate when blocked.** A blocker is an irreversible decision, a security red flag without a mitigation, or a missing credential. Everything else — opinions on design, naming, priorities — decide yourself and document the call.
3. **Every stage produces an artifact.** Write it to the project folder so the next stage has something concrete to consume.
4. **Update status after every hand-off.** The command center artifact reads from `status.json`, `chat.jsonl`, and `inbox.json`.
5. **Security-first.** The Security team gates the build. If `threat-modeler` flags a critical unmitigated risk, stop and escalate.

## Pipeline

Run the 7 stages in order. See `references/pipeline-stages.md` for the full stage spec.

```
Intake  →  PM  →  Security  →  Architecture  →  Build  →  QA  →  DevOps  →  Docs  →  Handoff
```

For each stage: the **lead agent** accepts the previous stage's artifact, dispatches to **specialist sub-agents** for the actual work, consolidates, writes the artifact, and hands off. See `references/handoff-protocol.md`.

## Step-by-step playbook

### Step 1 — Initialise project

1. Derive a slug from the user's idea (kebab-case, 2–4 words, e.g. `invoice-splitter`, `habit-tracker-pwa`).
2. Create the project folder at `/sessions/loving-adoring-maxwell/mnt/outputs/devsecops-agency/<slug>/`.
3. Create `status.json` with the initial schema (see `references/status-schema.md`).
4. Create empty `chat.jsonl` and `inbox.json`.
5. Call the `command-center` skill to open the live view.

### Step 2 — Intake (ask the human)

Use AskUserQuestion **once** to collect these batched clarifications. Only ask questions whose answer isn't already obvious from the idea:

- **Tech preference** — preferred language/framework, or "you pick"
- **Deployment target** — Vercel, AWS, self-hosted, Cloudflare Pages, or "you pick"
- **Data store** — needs a database? SQLite / Postgres / Supabase / none?
- **Examples or inspirations** — any links, screenshots, or reference apps?
- **Must-haves / no-gos** — any hard constraints (e.g. "no third-party auth", "must be accessible offline")

Write the raw answers to `brief.md > ## Intake answers`. Proceed.

### Step 3 — PM phase

Dispatch `pm-lead` via the Task tool with the raw idea + intake answers. The lead will internally dispatch `user-researcher` (personas, jobs-to-be-done) and `spec-writer` (functional spec, acceptance criteria, success metrics). Append the resulting **product brief** to `brief.md` and update `status.json`. Log the handoff in `chat.jsonl`.

### Step 4 — Security phase (gate)

Dispatch `security-lead` with `brief.md`. The lead dispatches `threat-modeler` (STRIDE threat model + OWASP Top 10 coverage — see `references/owasp-checklist.md`) and the output feeds `code-auditor` later. Write `threat-model.md`.

**Gate check:** if any Critical/High risk has no mitigation plan, escalate via `inbox.json` — do not proceed until the human answers.

### Step 5 — Architecture phase

Dispatch `engineering-lead` with `brief.md` + `threat-model.md`. The lead dispatches `api-designer` (endpoints, schemas, auth model) and finalises the architecture (tech stack, data model, module layout, deploy topology). Write `architecture.md`.

### Step 6 — Build phase

`engineering-lead` dispatches `backend-dev` and `frontend-dev` in parallel based on the architecture. They write code into `src/`. Each specialist reports back to the lead, who checks the code against the architecture doc and threat-model mitigations.

### Step 7 — QA phase

Dispatch `qa-lead` with the code folder and the spec. Lead dispatches `test-designer` (derives test matrix from acceptance criteria) and `test-runner` (writes actual tests, executes them, captures failures). Write `tests/` and `qa-report.md`. If tests fail, loop back to `engineering-lead` for fixes (max 2 loops before escalating).

### Step 8 — Security second pass

Dispatch `code-auditor` on the built code against the threat model. Any new Critical finding triggers a fix loop with `engineering-lead` (max 2 loops).

### Step 9 — DevOps phase

Dispatch `devops-lead`. Lead dispatches `ci-engineer` (CI workflow, linters, test gate, SCA scan) and `deployment-engineer` (Dockerfile/IaC, deploy checklist, rollback plan). Write `deploy/`.

### Step 10 — Docs phase

Dispatch `docs-lead`. Lead dispatches `api-documenter` and `readme-writer`. Write `docs/` and a polished top-level `README.md` into the project folder.

### Step 11 — GitHub push (optional)

If a GitHub connector is available, offer to push. If the user declines or the connector is absent, stop here and tell the user where to find the local files.

### Step 12 — Final handoff

- Update `status.json` → phase `delivered`.
- Refresh the command center artifact one last time.
- Post a concise summary in chat: project folder link, key artifacts, any known caveats, one suggested next step (e.g. `/devsecops-agency:retro`).

## Agent dispatch pattern

Always use the Task tool with `subagent_type` set to the agent's name. Give the agent:

1. The project folder path
2. The specific artifacts it needs to read (by filename)
3. The artifact it is expected to produce (by filename)
4. A one-line success criterion

Do not paste large artifacts into the agent prompt — reference them by path and let the agent read them.

## Status and logging

After every stage, write a status update:

```json
// status.json fragment
{
  "phase": "architecture",
  "activeAgents": ["engineering-lead", "api-designer"],
  "completed": ["intake", "pm", "security"],
  "artifacts": {
    "brief": "brief.md",
    "threatModel": "threat-model.md"
  },
  "blockers": [],
  "lastUpdated": "<iso-timestamp>"
}
```

Append to `chat.jsonl` on every handoff:

```json
{"ts":"<iso>","from":"security-lead","to":"engineering-lead","type":"handoff","artifact":"threat-model.md","note":"2 High risks, 0 Critical"}
```

## When to stop and ask the human

See `references/escalation-rules.md`. In short: ask when there is (a) a missing credential, (b) an unmitigatable Critical security risk, (c) an irreversible action (deleting data, publishing externally), (d) genuine ambiguity in user intent that would flip the solution. Never ask for mere preferences — decide and document.

## Progressive disclosure

- `references/pipeline-stages.md` — detailed stage definitions, inputs/outputs
- `references/handoff-protocol.md` — how leads dispatch specialists and consolidate results
- `references/escalation-rules.md` — blocker definitions and inbox format
- `references/owasp-checklist.md` — the Security-team gate
- `references/status-schema.md` — exact JSON schema for status.json and chat.jsonl
