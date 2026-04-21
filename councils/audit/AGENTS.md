# councils/audit — boundaries

## Output contract

- Lead: `cao`. Specialists: `adr-auditor`, `gate-auditor`, `okr-auditor`, `memory-auditor`.
- Artifact root: `_vision/audit/<date>-<scope>-<kind>.md` where `<scope>` is slug or `portfolio` and `<kind>` ∈ `{adr, gates, okr, memory, close, pre-release, incident}`.
- Informing council. Reds file ADRs in the same CEO turn.
- Independence invariant: Audit Council is **never** in any project's delivery path. No dual-hatting.

## Must

- Run in parallel. All 4 auditors are independent by design; sequencing creates implicit ordering bias.
- Read-only on the records being audited. Findings propose remediations; remediations flow through CEO + ADR + owning council.
- Cite every finding with ≥ 1 `file:line` + name the rule violated (root AGENTS.md, council AGENTS.md, or SKILL.md section).
- Walk **every** row for machine-checkable audits (gate aggregation, OKR worst-of-3, append-only git blame). No sampling.
- File a new ADR for every red finding. Audit of audits is itself part of the paper trail.

## Must not

- Participate in the project or decision being audited. If any Audit specialist was previously dispatched as a delivery agent in the same scope, hand the audit slot to COO + escalate to CEO.
- Mutate the record being audited. Corrections are appended via `[correction]` lines in session logs, or via new ADRs. Never revert, never rewrite.
- Mark a missing ADR as "acceptable" because "the decision was obvious". The missing ADR is the finding.
- Accept a yellow verdict from a specialist without a concrete taskflow task ID paired to the follow-up.
- Issue a green on the close audit if any blocking-council red went un-waived. Ship-but-red is the worst headline.

## Gate heuristic

- `green`: all 4 specialists green, no missing mandatory ADR, no append-only violation, no unescalated OKR-red.
- `yellow`: one specialist yellow with concrete remediation owner + taskflow task; no blocking-red evidence.
- `red`: any append-only memory violation · mutated accepted ADR · unwaived blocking-council red · unescalated OKR-red · gate aggregation-error · PII/secret leak.

## OKR alignment hint

- Audit Council scores `okr_alignment` against **paper-trail OKRs only** (e.g., "zero missing ADRs per quarter", "zero append-only violations"), never against product OKRs.
- If a close-audit finding would indict the active workspace OKRs themselves (e.g., OKR-auditor shows all green traces are to a stale superseded KR), flag `okr_alignment: red` and force a VISION.md structured rewrite through the CEO.
