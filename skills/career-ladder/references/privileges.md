# career-ladder/references/privileges.md

What each level unlocks. Read by CEO, COO, CAO when routing work.

## Summary table

| Privilege | L1 | L2 | L3 |
| --- | --- | --- | --- |
| Runs assigned tasks | Yes | Yes | Yes |
| Reads ADRs / stones / lessons | Yes | Yes | Yes |
| Writes ADRs on own work | Yes | Yes | Yes |
| Writes session-log entries | Yes | Yes | Yes |
| Votes on prompt-diff review in own council | No | Yes | **First vote** |
| Authors stepping-stones | No | Yes | Yes (counts toward L3 re-validation) |
| Primary author of `roster-upgrade` ADR for another agent | No | No | Yes |
| Mentor assignment for newly-hired agent in same council | No | No | Yes |
| First-choice reviewer for cross-council drafts | No | No | Yes |
| Signs off on close-out gate without a second reviewer | No | No | Yes (for L3 within the gate's council) |

## Detail

### First vote on prompt-diff review (L3 only)

When a council reviews a prompt-upgrade diff (per `VALUES.md §10`), if **≥ 1 L3 is present in the review pool**, their vote is tallied first and is the de facto recommendation that other reviewers endorse, amend, or reject. Other L2 votes still count; the L3 vote is not a veto.

If no L3 is in the review pool (e.g., the only L3 in the council is the one whose prompt is being upgraded), the council lead acts as temporary first-voter. If the council lead is the one being upgraded, escalate to COO.

### Stepping-stone authorship (L2 + L3)

L2 agents can author stepping-stones. L3 agents can author stepping-stones AND they count toward L3 re-validation (keeps their streak alive). L1 agents cannot author — their work is filed but not canonicalized into the playbook archive until they reach L2.

**Primary author field.** Every stepping-stone has one `primaryAuthor`. Co-authors are named but do not accrue gate credit. An agent can have multiple stones, but a single stone cannot count for multiple agents' L3 gates.

### Primary author of roster-upgrade for another agent (L3 only)

Only L3 agents can be primary author on a `roster-upgrade` ADR body for a different agent in their council. This is the mentorship signal — it means the L3 drafted the prompt-edit, took it through `red-team` + `playbook` prompt-diff review, and shepherded it to merge.

L2 agents can co-author or suggest edits, but the `author:` field of the ADR must be an L3. (If no L3 exists in the council, the council lead acts as author.)

### Mentor assignment (L3 only)

When a new agent joins a council (via `skill-creator`), COO assigns one L3 from that council as the mentor. The mentor:

- Reviews the new agent's first 3 reports and signs off on them before close-out.
- Co-authors any `roster-upgrade` ADR for the new agent during their L1 trial window.
- Is cited in the new agent's Role Card `Reports to:` field (alongside the council lead) during trial.

If no L3 exists in the council when the new agent joins, the council lead acts as mentor.

### Close-out gate sign-off without second reviewer (L3 only)

A standard close-out gate (per `skills/gates/SKILL.md`) requires two agents to sign off. When one of those agents is L3 and the gate is in their council, the second reviewer can be waived and the L3's sign-off is sufficient. L1 and L2 always require the second reviewer.

This privilege does NOT apply to blocking-council gates (security, legal) — those always require the chief's sign-off regardless of level.

## Privileges that do NOT depend on level

- Any-level agent can escalate to the ladder (Rung 1–7).
- Any-level agent can request a user-meeting via `inbox.json` (subject to CEO routing).
- Any-level agent can file a red-team finding.
- Any-level agent can read `MISSION.md` / `VALUES.md` / `LESSONS.md` / `KEEPER-TEST.md` / `RHYTHM.md` / `CAREER.md`.
- Any-level agent can author memory entries (subject to novelty gate per `skills/memory`).
- Any-level agent can spawn workers if their frontmatter declares a worker pattern.

## Anti-patterns

- Don't use level as a shortcut for trust. Receipts are the trust surface (`VALUES.md §1`); level is an internal sort order for first-vote + mentor assignment.
- Don't let an L2 agent primary-author a `roster-upgrade` ADR for another agent. Enforcement: the `roster` skill's ADR validator rejects such ADRs at write time.
- Don't let a single L3 be mentor for more than 3 concurrent new-hires in their council. COO distributes load.
- Don't carry L3 privileges across a demotion. Demotion → L2 strips first-vote, stepping-stone gate credit, and mentor assignments immediately.
- Don't promote an L3 agent by making them a Chief. Chiefs are reserved and always L3; a specialist L3 stays L3 but does not become their council's chief. Tier / role changes happen via USER-only path.
