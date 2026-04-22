# GOVERNANCE.md

One-sentence tagline: **decision rights are a matrix, not a reflex — the CEO reads this before escalating, and the user reads it before overruling.**

Consolidates into one page every authority split that was previously scattered across `VALUES.md`, `KEEPER-TEST.md`, `CAREER.md`, and the per-council `AGENTS.md` contracts. Nothing new — this is the citable surface.

## Who decides what

| Decision kind                                 | Proposer              | Reviewer                      | Approver               | Final vote |
| --------------------------------------------- | --------------------- | ----------------------------- | ---------------------- | ---------- |
| Accept idea into backlog                      | opportunity-ranker    | pm-lead                       | CEO                    | CEO        |
| Kick off project from backlog                 | CEO                   | user-meeting 4-phase          | user                   | **user**   |
| Architecture decision (ADR)                   | engineering-lead      | security-lead                 | engineering-lead       | CEO (review on conflict) |
| Block on security critical/high              | security-lead (CISO)  | —                             | security-lead          | security-lead (blocking) |
| Block on eval regression > 5 pp               | evaluation-lead (CEVO)| —                             | evaluation-lead        | evaluation-lead (blocking) |
| Block on red-team high/critical               | red-team-lead (CRT)   | —                             | red-team-lead          | red-team-lead (blocking) |
| Block on close-audit integrity red            | cao                   | —                             | cao                    | cao (blocking) |
| Waive a blocking-council red                  | council lead          | CEO                           | **user**               | **user**   |
| Prompt upgrade on own agent persona           | any agent             | red-team + playbook prompt-diff| council lead          | council lead |
| Prompt upgrade on another agent in council    | L3 specialist         | red-team + playbook prompt-diff| council lead          | council lead |
| Tier change (Chief → Specialist or reverse)   | —                     | —                             | —                      | **user** (`VALUES §10`) |
| Level change (L1 ↔ L2 ↔ L3) within tier       | career-ladder         | COO                           | career-ladder ADR      | CAO audit (post-hoc) |
| Fire an agent                                 | performance-reviewer  | hiring-lead → COO → CEO       | **user** via inbox.json| **user** |
| Hire a new agent (via skill-creator)          | skill-creator         | COO                           | CEO                    | CEO |
| Archive a project                             | CEO                   | cao close-audit + cevo + crt  | CEO                    | CEO |
| Rung 3+ escalation                            | ladder                | CEO                           | CEO                    | CEO |
| Rung 7 parking                                | CEO                   | user-meeting                  | **user**               | **user** |
| Adopt new MCP / skill / third-party tool      | any agent             | tool-scout + CSRE             | CEO                    | CEO |
| Update `MISSION.md` / `VALUES.md` / `KEEPER-TEST.md` / `CAREER.md` / `GOVERNANCE.md` / `RESILIENCE.md` | CEO | — | **user** | **user** |
| Update `LESSONS.md` (append row)              | lessons-ledger        | —                             | lessons-ledger         | append-only (no reviewer) |
| Update `RHYTHM.md` cadence list               | CEO                   | —                             | **user**               | **user** |
| Change council membership (add/remove agent)  | coo via roster        | red-team prompt-diff          | CEO                    | CEO |
| Publish an artifact externally (GitHub push, release, etc.) | CEO  | sbom-slsa + ip-lineage        | **user** (explicit)    | **user** |
| Spend money (tool purchase, API upgrade, etc.)| any agent             | —                             | **user**               | **user** |

Blocking councils (security / evaluation / red-team / audit) hold **strict veto**; their red can only be cleared by the user via a formal waiver (see `skills/waivers/`).

## USER-ONLY actions

These cannot happen without explicit user approval in the chat interface, via `user-meeting` or `inbox.json`:

1. Kick off any project (go / no-go).
2. Tier change for any agent (Chief ↔ Specialist).
3. Fire any agent.
4. Waive a blocking-council red.
5. Rung 7 parking (permanent shelve with revival trigger).
6. Amend any of: `MISSION.md`, `VALUES.md`, `KEEPER-TEST.md`, `CAREER.md`, `GOVERNANCE.md`, `RESILIENCE.md`, `RHYTHM.md` cadence list.
7. Publish anything externally (GitHub push, release, blog, social).
8. Spend money.
9. Accept an idea that lands in a `MISSION.md` non-goal.
10. Cross-tier reassignment (roster-repurpose across tiers).

If an agent believes a user-only action is urgent and the user is not present, the correct move is to file a `user-decision-pending` row in `inbox.json` and continue on remaining work — never to self-authorize.

## Proposer / Reviewer / Approver rules

- **Proposer** writes the draft (ADR body, prompt-diff, waiver request, etc.).
- **Reviewer** signs off or sends back with specific changes. Cannot approve.
- **Approver** lands the decision. For blocking-council reds, the approver is always the user.
- **Independence rule** (`VALUES §3`): an Audit / Evaluation / Red-Team / SRE specialist cannot be proposer + reviewer + approver on the same decision. At least one must be outside those four councils.

## Chief-level blocking vs. informing

| Chief | Blocking on | Informing only |
| --- | --- | --- |
| CISO (security-lead) | Critical/High without mitigation; raw secrets; wildcard allowlist; missing SBOM+SLSA on ship | — |
| CEVO (evaluation-lead) | ≥ 5 pp regression vs. baseline; < 8/10 skill-eval on release; variance σ/μ > 0.15 | — |
| CRT (red-team-lead) | ASI-class finding; self-red-team independence breach; unpinned-hash adoption | — |
| CAO (cao) | Append-only violation; missing ADR for material decision; non-goal drift without ADR | — |
| CSRE (sre-lead) | — | Model-routing outages, tool-scout verdicts, sandbox posture (escalates via CEO if red) |
| CPO / CTO / VP-Eng / CQO / VP-Ops / CKO / GC / CMO / CSO / COO | — | All default informing; blocking moves happen via ladder + ADR |

A blocking Chief's red converts to an explicit gate — the ladder cannot re-try past it. Only a user-signed waiver clears the gate.

## Paper-trail requirements per decision

Every decision row in the matrix above must produce:

1. An ADR (`_decisions/ADR-NNNN-*.md`) with `kind:` matching the decision type.
2. A session-log entry by the approver citing the ADR id.
3. For blocking-council decisions: a `red-team`/`eval`/`audit` findings row + resolution path.
4. For user-only decisions: a `user-meeting` entry + `inbox.json` update if async.

Missing any of these is a CAO red at the next close-audit.

## Interaction with other root docs

- `VALUES.md §1` (receipts over opinions): every row here produces receipts.
- `VALUES.md §3` (independence): row 17+ above can't collapse approver into reviewer.
- `VALUES.md §10` (USER-ONLY on tier, persona updates, publishing): enumerated in this doc.
- `KEEPER-TEST.md`: the fire row here cites it as the sole framework.
- `CAREER.md`: the level-change row here defers to it.
- `RHYTHM.md`: the cadence-list row here requires user approval to amend.
- `RESILIENCE.md`: failure-mode escalation defers to `skills/ladder` + `skills/drill` + this matrix.

## Waivers

A waiver is the only way to clear a blocking-council red without fixing the underlying finding. Waivers:

- Are proposed by the responsible council lead, reviewed by the blocking Chief + CEO, approved by the user.
- Carry an explicit expiration (calendar date, not "until ship").
- File an ADR `kind: waiver-grant` with the finding id, the approver (user), and the remediation commitment.
- File a follow-up ADR `kind: waiver-expiry` on the expiration date — if unremediated, the red re-fires.

See `skills/waivers/` for the exact flow.

## Anti-patterns

- Don't approve your own proposal. Proposer ≠ approver except for `lessons-ledger` append (which has no reviewer by design).
- Don't let a blocking Chief approve a waiver on their own red. The approver must be the user.
- Don't collapse "Chief was informed" into "Chief approved". Informing-only chiefs don't gate.
- Don't take a user-only action because "the user said yes last quarter". Consent is per-decision; priors don't carry.
- Don't file an ADR with `kind: waiver-grant` that lacks an expiration date. Permanent waivers are prohibited.
- Don't escalate a decision that already has an approver in the matrix. CEO's job is to run the matrix, not to override it.
- Don't route past a blocking red by picking a different council. The gate follows the artifact, not the path.
