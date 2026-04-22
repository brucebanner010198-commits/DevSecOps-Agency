---
name: audit
description: This skill should be used when the CAO (or CEO on CAO's behalf) runs an integrity audit on the agency's paper trail. Trigger phrases include "close-audit", "portfolio audit", "integrity check", "run an audit", "pre-release audit", "did we follow our own rules", "why did X ship as green when CISO was red", "are the ADRs complete", "is the memory clean". Wired into CEO close phase (mandatory on every project close), into quarter roll-up (portfolio), and invoked ad-hoc on user request or on incident-response.
metadata:
  version: 0.3.0-alpha.3
---

# audit — independent paper-trail integrity

Audit is the only Council that never participates in product delivery. Its job is to catch rule violations that the delivering councils missed or hid. Close-audit is mandatory on every ship.

## When to trigger

- **Close** — every project close, before archival. Mandatory. CEO cannot mark a project archived without a green/yellow audit.
- **Portfolio** — every quarter roll-up. Mandatory.
- **Pre-release** — before any `plugin.json.version` bump + outbound `.plugin` zip ship.
- **Incident** — on any gate-red waiver that the user overrode, or on user request.
- **Ad-hoc** — user asks "how are we doing on X rule" → CAO scopes down to just that rule.

## Audit kinds → specialist mapping

| Kind         | Specialist(s)                                              | Fail-fast conditions                     |
| ------------ | ---------------------------------------------------------- | ---------------------------------------- |
| ADR trail    | `adr-auditor`                                              | mutated accepted body · missing mandatory ADR |
| Gates        | `gate-auditor`                                             | wrong-blocking-flag shipped · aggregation error |
| OKR          | `okr-auditor`                                              | unescalated OKR-red · non-goal drift     |
| Memory       | `memory-auditor`                                           | append-only violation · PII leak         |
| Close        | all four in parallel                                       | any red from any specialist              |
| Portfolio    | all four + cross-project consistency                       | ≥ 2 identical findings across projects   |
| Pre-release  | adr-auditor + `skill-version-auditor` (future wave)        | version-bump without skill contract changes |

## Artifact layout

```
_vision/audit/
  <date>-<scope>-<kind>.md        # e.g., 2026-04-21-dorm-splitter-close.md
  <date>-portfolio-<kind>.md      # quarter roll-ups
  _index.md                       # alphabetical chronological index — rewritten on every audit
```

## Process

1. **CEO convenes CAO.** Specify scope: slug (close) or `portfolio` (roll-up).
2. **CAO independence check.** If any Audit specialist was previously dispatched as a delivery agent in the same scope, CAO hands that specialist's slot back to COO to flag the dual-hatting. Independence is not optional.
3. **Parallel dispatch.** All 4 auditors go in parallel. No ordering dependency (one of the reasons `audit` is always parallel, per root AGENTS.md worktree matrix).
4. **Aggregate.** CAO synthesises `<date>-<scope>-close.md` with the summary + findings + reds-to-ADRs list.
5. **CEO files ADRs in the same turn.** Every red becomes an ADR. Every yellow becomes a taskflow task with owner + deadline. Orphan reds = CAO re-files on next audit.
6. **Update `_vision/audit/_index.md`.** Alphabetized chronologically (ISO date prefix handles ordering naturally). Deterministic.

## Invariants

- Audit Council is read-only on the records being audited. Corrections flow through new ADRs or `[correction]` session-log lines.
- Machine-checkable audits walk **every row** (gate aggregation, OKR worst-of-3, append-only git blame). No sampling.
- Every red files an ADR in the same CEO turn. Per root AGENTS.md: "land a material decision without filing an ADR in the same CEO turn = never".
- Every yellow has a concrete taskflow task ID + owner. No floating follow-ups.
- See `references/audit-matrix.md` for the per-kind rule list.
- See `references/scope-boundary.md` for the independence rule + dual-hatting handling.

## Contract with adjacent skills

- `okr.score` runs on CAO's report (OKRs are on paper-trail integrity, not product).
- `gates.validate` uses Audit heuristic in `councils/audit/AGENTS.md`.
- `meeting-minutes` writes for every audit convening (kind: `audit`).
- `adr` files mandatory ADRs on every red finding.
- `roster` skill is downstream: Audit reds on an agent's output become performance-reviewer evidence at the next roster checkpoint.
- `runtime-hooks/governance-audit/` runs at session-start + per-prompt + session-end. Scans prompts for 5 threat categories (data-exfiltration, privilege-escalation, system-destruction, prompt-injection, credential-exposure) and appends findings to `.github/logs/copilot/governance-audit/audit.log`. Close-audit (CAO) reads this log — any unacknowledged threat line is a mandatory ADR finding.

## What this skill is not

- Not a code review. QA Council owns code review.
- Not a security review. Security Council owns that.
- Not a retro. Retro is forward-looking ("what to change"); audit is backward-looking ("what did we do vs what we said").
- Not an eval. Eval-lead (Wave 5) scores agent output quality; audit scores paper trail integrity.
