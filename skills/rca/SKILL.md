---
name: rca
description: >
  Produce a blameless root-cause analysis for an incident or close-miss using
  5 Whys, Ishikawa (fishbone), and fault-tree analysis.  Invoke on every
  Severity >= High incident, every append-only violation, every raw-secret
  near-miss, and every Keeper Test finding.  Output is a structured RCA
  markdown file + a LESSONS.md row + (if systemic) a proposed Constitutional
  amendment or runtime-hook addition.  Trigger phrases include "run RCA",
  "root-cause this", "5 whys", "fishbone", "fault tree", "post-mortem for
  <incident>", or any /devsecops-agency:rca invocation.
metadata:
  version: "1.0.0"
---

# rca — Root-Cause Analysis

Authority: [`CONSTITUTION.md`](../../CONSTITUTION.md), [`RESILIENCE.md`](../../RESILIENCE.md), [`DISASTER-RECOVERY.md`](../../DISASTER-RECOVERY.md)
Owner: CIR (Incident Response) · Reviewer: CAO · Called from: `skills/retrospective`, `skills/drill`, `skills/incident-response`

## When to trigger

| Trigger | Required? |
|---|---|
| Severity ≥ High incident closed | REQUIRED (Constitution §7) |
| Append-only invariant violation | REQUIRED |
| Raw-secret near-miss (caught pre-commit) | REQUIRED |
| ASI-class escalation request | REQUIRED |
| Keeper Test finding | REQUIRED |
| Repeated Medium finding (same class ≥ 2× in 90d) | REQUIRED |
| Minor one-off Low finding | OPTIONAL |

## Blameless posture (non-negotiable)

This is a blameless RCA. The purpose is to identify systemic weaknesses, not to assign blame to an agent, council, or the User. If the RCA output reads like accusation, it has failed.

- Replace "X did Y wrong" with "the system permitted Y".
- Replace "should have known" with "the information was not available / not prompted".
- Replace "human error" with "the process relied on the human holding state the process did not hold".

If the RCA cannot be written blamelessly, return it to the CIR for re-framing.

## Inputs

1. The incident record (GitHub issue, session log range, or ADR).
2. The timeline of events (timestamps, actions, outcomes).
3. Affected artifacts (commits, releases, LESSONS rows, waivers).
4. Any detection signal that first fired.

## Procedure

### Step 1 — Establish the facts (not the narrative)

Write a numbered timeline. Each entry has: timestamp (UTC), actor (agent / hook / User), action, observable outcome, source (which log line).

Facts only. No interpretation. If you cannot cite a source for an entry, mark it `[UNSOURCED]` and treat it as a hypothesis to verify later.

### Step 2 — Frame the problem

One sentence: what happened that should not have happened, or what did not happen that should have.

Example: *"At 14:32 UTC on 2026-04-22, a commit was accepted to `main` modifying a file under `sessions/` without append-only enforcement firing."*

### Step 3 — Apply 5 Whys

Start from the problem and ask "why?" five times. Each answer becomes the next "why".

- **Why 1 — Why did the commit succeed?** Because `runtime-hooks/commit-gate.sh` did not run.
- **Why 2 — Why did the hook not run?** Because the hook was not installed into `.git/hooks/` on this clone.
- **Why 3 — Why was the hook not installed?** Because the install step is manual and was skipped by the contributor.
- **Why 4 — Why is the install step manual?** Because there is no bootstrap script that installs hooks on clone.
- **Why 5 — Why is there no bootstrap script?** Because the repo was designed to be edited by the CEO using a pre-configured workstation, and the contributor case was not modeled.

**Root cause:** the hook enforcement model assumed a single environment and did not cover the contributor-clone case.

Five is a floor, not a ceiling. Keep asking "why" until each answer stops pointing at a deeper cause.

### Step 4 — Ishikawa (fishbone) diagram

Draw (in markdown) the fishbone with six canonical branches, each populated with contributing factors:

```
                        [Problem statement]
        ┌──────────────────┼──────────────────┐
      People           Process            Technology
        │                  │                  │
      ...                ...                ...
        │                  │                  │
     Environment       Materials           Measurement
```

- **People:** who was in the loop, who was not, who held state.
- **Process:** which procedure applied, which was followed, which was skipped.
- **Technology:** which tool / hook / agent / skill was involved.
- **Environment:** repo state, time pressure, session context, platform state.
- **Materials (inputs):** what data / prompts / files were in play.
- **Measurement:** which metrics would have caught this earlier.

Mark each contributing factor with a `[C]` (cause), `[S]` (symptom), or `[T]` (trigger).

### Step 5 — Fault tree

Write the problem at the root. For each immediate cause, create a sub-node. Connect with AND / OR gates.

```
[PROBLEM: commit to main bypassed append-only]
  └─ AND
     ├─ [commit-gate did not fire]
     │    └─ OR
     │       ├─ hook not installed on clone
     │       ├─ hook disabled by env var
     │       └─ hook script path was wrong
     └─ [branch protection did not block]
          └─ OR
             ├─ no branch protection configured (v0.6.0 gap)
             └─ configured but bypassed with admin push
```

The fault tree makes the *independence* of causes explicit. An AND gate means "all of these failed at the same time" — a serious multi-barrier failure.

### Step 6 — Identify the barrier that should have stopped this

For each AND branch in the fault tree, name the barrier that was supposed to hold. For each OR branch, name the defense-in-depth layer that was supposed to hold if the primary failed.

Mark each barrier: `HELD`, `DEGRADED`, `FAILED`, or `ABSENT`.

A healthy system fails no more than one barrier at a time. Two-barrier failures are Critical events. Three-barrier failures require a Constitutional review.

### Step 7 — Propose corrective actions

Each action has:
- **ID** (e.g., RCA-2026-04-22-A1)
- **What** — one-sentence action.
- **Why** — which cause/barrier this addresses.
- **Owner** — council or User.
- **Due** — ISO date.
- **Success criterion** — how we know it worked.
- **Class** — one of: CONTROL_ADD (new hook/skill), CONTROL_STRENGTHEN (tighten existing), DETECTION_ADD (new metric/alarm), PROCESS_CHANGE (runbook/checklist), DOCUMENTATION (clarify), CONSTITUTIONAL (amendment proposal).

If any corrective action is `CONSTITUTIONAL`, open an amendment PR per [`CONTRIBUTING.md`](../../CONTRIBUTING.md) §6.

### Step 8 — Distinguish contributing factors from root causes

Root cause = if removed, the incident does not happen.
Contributing factor = amplified the incident but incident could still happen.

Be strict. Promoting a contributing factor to a root cause inflates the corrective-action list and exhausts attention.

### Step 9 — Write the RCA document

Produce `_meetings/rca-<slug>-<date>.md` with these sections:

1. **Summary** — 3-5 sentences: what, when, impact, root cause, headline action.
2. **Timeline** — numbered, sourced (from Step 1).
3. **Impact** — blast radius: what was affected, for how long, by how much.
4. **5 Whys** — from Step 3.
5. **Ishikawa** — from Step 4.
6. **Fault tree** — from Step 5.
7. **Barrier analysis** — from Step 6.
8. **Root cause** — the one statement from Step 8.
9. **Contributing factors** — list from Step 8.
10. **Corrective actions** — table from Step 7.
11. **Lessons** — 2-4 bullets that will feed [`LESSONS.md`](../../LESSONS.md).
12. **Attachments** — links to session log range, commits, advisory.

### Step 10 — Produce the LESSONS row

Append one row to [`LESSONS.md`](../../LESSONS.md) citing the RCA file and the lessons from §11.

### Step 11 — Escalate if systemic

If the root cause is a control gap the Constitution should close, open an amendment issue per [`CONTRIBUTING.md`](../../CONTRIBUTING.md) §6.

If the root cause is a new threat class, add it to [`THREAT-MODEL.md`](../../THREAT-MODEL.md) in the next minor version.

## Anti-patterns (refuse these)

- **"Operator error"** as a root cause. Operator error is a symptom. The root cause is the process that let operator error produce this outcome.
- **Single-why analysis.** Stopping at the first plausible cause.
- **Blame language.** "X failed to Y" — re-frame as "the process did not enforce Y".
- **Action items without owners or due dates.** These die in the backlog.
- **Skipping the barrier analysis.** Without it, you cannot tell whether this was a single-barrier miss (expected over time) or a multi-barrier failure (systemic).
- **Closing the RCA without LESSONS row.** The RCA exists to feed the ledger.

## Outputs

- `_meetings/rca-<slug>-<date>.md` — the RCA.
- One appended row in [`LESSONS.md`](../../LESSONS.md).
- Optional: amendment issue, threat-model update, runtime-hook addition.

## References (original synthesis)

- Rasmussen, *Risk Management in a Dynamic Society* (1997).
- Reason, *Managing the Risks of Organizational Accidents* (1997) — Swiss Cheese model, basis for barrier analysis.
- Ishikawa, *Guide to Quality Control* (1982) — fishbone methodology.
- NASA, *Root Cause Analysis Overview for Program & Project Managers* — fault-tree practice.
- Google SRE Workbook, ch. 10 on blameless post-mortems.
- NIST SP 800-61 Rev. 2 — incident handling.
