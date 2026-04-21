# decision-triggers — when an ADR is mandatory

If a trigger fires and no ADR is written, the `retro` skill flags it as `missed_adr` and it surfaces in the next retro report.

## Mandatory triggers

### User-facing decisions
- User picks 1–2 ideas from a top-5 meeting. (ADR per chosen idea.)
- User commits to an ETA on a project.
- User cancels or defers a project mid-flight.
- User overrides a Chief's recommendation.
- User sets or amends a workspace non-goal.

### People-ops (v0.3.0 Wave 3)
- `skill-creator` produces a new agent file (Hire).
- Any agent retires — `agents/<name>.md` moves to `_vision/roster/_archive/<name>.md` (Fire).
- A specialist is renamed + rescoped (Repurpose).
- A Chief's scope expands or contracts.
- Model tier upgrades (e.g. Haiku → Sonnet). Downgrades are forbidden entirely.
- Any contract-changing prompt edit to `agents/<name>.md` or `skills/<slug>/SKILL.md`.
- Any audit-breach event — an Audit Council specialist found on a project's delivery path.

### Audit (v0.3.0 Wave 3)
- Any CAO red finding (one ADR per finding, same CEO turn).
- Any close-audit skipped on a project that shipped (backfill ADR + taskflow task).
- Any appended-body mutation found on an accepted ADR (itself an ADR finding).
- Any PII / secret leak candidate escalated to human review (ADR tracks remediation).

### Scope + strategy
- Adding or removing a phase in the board playbook.
- Adding or removing a council.
- Any `_vision/VISION.md` mutation (mission, OKR, non-goal).
- Mid-project OKR amendment.
- Non-goal violation accepted (CEO proceeds despite).

### Gate + risk
- Any waiver of a council gate (security, legal, a11y, qa).
- Any `okr_alignment: red` accepted (CEO proceeds despite).
- Any Critical-severity risk accepted without mitigation.
- Any compliance exception (future Wave 7 compliance-drift skill).

### Technology
- Framework / runtime / vendor choice with reversal cost > 1 engineering day.
- Adding a new external service dependency (payments, auth, storage, AI API).
- Switching an LLM provider or model family.
- Introducing a non-text content format to the product (images, audio, etc.).

### Process
- Extending the 2-attempt fix-loop cap on a specific task.
- Using the never-give-up ladder (future Wave 4 skill) — every rung escalation is an ADR.
- Merging a worktree with structural conflicts accepted.
- Publishing a project publicly (GitHub push to public repo, npm publish, etc.).

## Optional triggers (file one if in doubt)

- Choice between two comparable libraries with similar reversal costs.
- Naming decisions (project name, repo name, brand mark).
- Color, copy, tone decisions.
- Choice of test framework.
- Choice of observability stack.

Heuristic: **if you'd want a future Chief to know why, file an ADR.**

## Non-triggers (do NOT file an ADR)

- Routine task transitions through the `taskflow` state machine.
- Phase advances that hit all handoff invariants cleanly.
- Memory writes that pass the novelty gate.
- Worktree creation / merge when no conflict surfaces.
- Green-green-green phase reports.
- Conversation turns with the user that don't produce a decision.

## Placement rules

- **Workspace-level** decisions → `Project: workspace`.
- **Project-level** decisions → `Project: <slug>`.
- Cross-project decisions (template extraction, shared library adoption) → filed at workspace level, referenced from each affected project's `brief.md`.

## Enforcement

The CEO SKILL.md (v0.3.0+) includes an `adr.check` step inside the board-meeting loop. After each gate validation, the CEO asks: "did this phase fire any of the mandatory triggers?" If yes and no ADR was filed in this project's `_decisions/` since the phase started, the CEO pauses the pipeline until the ADR exists.

This is a soft gate — the CEO can escalate to the user if the pause persists, but the default is: file the ADR, resume.

## Never

- File an ADR for a non-decision ("we used git" — trivial, not a decision).
- Skip an ADR because the decision "feels obvious." (Obvious to whom?)
- Bundle multiple decisions into one ADR. (Split.)
- Write an ADR after the project closes ("retrocon"). File at decision time.
