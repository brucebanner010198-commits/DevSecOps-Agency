# scope-boundary.md — independence + dual-hatting rules

Audit Council's value comes from independence. When that independence erodes, the audit no longer functions. This file defines the boundary and the handling when it's breached.

## The invariant

**No Audit Council agent participates in any project's delivery path.**

Concretely:

- `cao`, `adr-auditor`, `gate-auditor`, `okr-auditor`, `memory-auditor` never appear as dispatch agents in a project's `chat.jsonl` with `scope: delivery`.
- They never author artifacts under `<slug>/` except `<slug>/audit-report.md` (close audit's slug-scoped output).
- They never vote in a board meeting. Audit reports into board meetings; it doesn't participate in decisions.

## Dual-hatting forbidden

The following combinations are invariant violations:

- Any Audit agent simultaneously appearing in another council's roster.
- `cao` holding any other Chief role (unlike `engineering-lead` which legitimately hats CTO + VP-Eng by design; CAO has no such design).
- An agent named in `_archive/` under Audit reappearing under a delivery council without an explicit rehire ADR.

## Breach handling

When CAO detects a breach during audit setup:

1. **Pause the audit.** Do not dispatch the conflicted specialist.
2. **Escalate to CEO** with a written breach note: which specialist, which delivery scope, which file:line evidence.
3. **CEO files an ADR** titled "Audit breach — <agent> — <scope>" with severity = blocker. Proposed remediations:
   - Hand the conflicted audit slot to **COO** (who runs a substitute review).
   - Or defer the audit by ≥ 1 delivery cycle so the agent can be rotated out.
   - Or hire a new auditor (`skill-creator` + COO `hiring-lead`).
4. **Audit resumes only after ADR is accepted.** The finding itself is part of the paper trail.

## Legitimate cross-reading (not a breach)

Audit agents **may**:

- Read from `_decisions/`, `_meetings/`, `_sessions/`, `_memory/`, `<slug>/chat.jsonl`, `<slug>/status.json`, council `AGENTS.md` files, skill `SKILL.md` files. That's the job.
- Cite findings from other councils' delivery work. The finding is not participation.
- Attend a board meeting as a **reporting** presence (their `audit-report.md` is read aloud) without being a decision-maker.

## Audit-of-audit (meta-integrity)

The Audit Council audits itself only via CEO invocation — never via CAO-on-CAO. Meta-integrity checks cover:

- Was an audit skipped on a close that shipped? (red)
- Did the CAO's summary aggregate correctly from specialist findings? (red on mismatch)
- Did any CAO report show `gate: green` while containing an unresolved specialist red? (red, always)

The first meta-integrity audit of a quarter runs as a portfolio audit; subsequent ones run only on user request.
