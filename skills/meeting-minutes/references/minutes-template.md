# minutes-template — skeleton + 2 worked examples

## Skeleton

```markdown
# Meeting minutes — YYYY-MM-DD — <kind>

- **Kind:** <kind>
- **Started:** YYYY-MM-DD HH:MM UTC
- **Ended:** YYYY-MM-DD HH:MM UTC
- **Chair:** <actor>
- **Scribe:** <actor>
- **Project:** <slug> | workspace
- **Related:** <refs or "none">

## Attendees

- <role> · <actor> — present|absent|partial
- ...

## Agenda

1. <topic>

## Discussion

### <topic>
- <point — by whom — cite>

## Decisions

- **D1** — <one line> — ADR-NNNN | no ADR (rationale)

## Action items

- **A1** — <action> — owner: <slug> — due: YYYY-MM-DD — task: <task-id>

## Open questions

- <question>
```

## Worked example 1 — user top-5 meeting

```markdown
# Meeting minutes — 2026-04-21 — user

- **Kind:** user
- **Started:** 2026-04-21 19:00 UTC
- **Ended:** 2026-04-21 19:18 UTC
- **Chair:** ceo
- **Scribe:** ceo
- **Project:** workspace
- **Related:** _vision/VISION.md, ADR-0001, ADR-0002, ADR-0003

## Attendees

- user · sir — present
- ceo · ceo — present

## Agenda

1. Review top-5 ideas from CMO + strategy council
2. Pick 1–2 ideas to execute this month
3. Commit ETAs
4. Cover non-goals

## Discussion

### Top-5 ideas (CMO roll-up)
- CMO presented 5 ideas ranked by market signal + fit-to-OKR. Top 3 aligned with "revenue-positive in 30 days" KR: `student-expense-tracker`, `dorm-marketplace`, `campus-event-finder`. Cites `_marketing/top5-2026-04-21.md`.
- User asked about defensibility of `student-expense-tracker` — CMO cited `research/competitors.md:22` (no targeted competitor).

### Selection
- User picked `student-expense-tracker` as primary. Paused on `campus-event-finder` pending moderation discussion next meeting.

### ETA commit
- CEO proposed 21 days end-to-end, consistent with [KR1.3]. User accepted with 1 caveat: hard stop at 28 days — cancel if not shipping.

### Non-goals
- User reaffirmed "no regulated industries" and added "no consumer financial instruments — expense tracking only, not advice."

## Decisions

- **D1** — Execute `student-expense-tracker` with 21-day ETA, 28-day hard stop — ADR-0008
- **D2** — Defer `campus-event-finder` to next meeting — no ADR (routine deferral)
- **D3** — Add non-goal: "no consumer financial advice" to VISION.md — ADR-0009

## Action items

- **A1** — Derive project OKRs for `student-expense-tracker` — owner: ceo — due: 2026-04-21 — task: T-0021
- **A2** — Amend VISION.md with new non-goal + history entry — owner: ceo — due: 2026-04-21 — task: T-0022
- **A3** — Open project folder, start Phase 1 Discovery — owner: ceo — due: 2026-04-21 — task: T-0023

## Open questions

- Moderation stance for `campus-event-finder` (carry to next user meeting)
```

## Worked example 2 — security council waiver

```markdown
# Meeting minutes — 2026-04-23 — council-security

- **Kind:** council-security
- **Started:** 2026-04-23 14:00 UTC
- **Ended:** 2026-04-23 14:22 UTC
- **Chair:** ciso
- **Scribe:** ciso
- **Project:** student-expense-tracker
- **Related:** ADR-0012, `security/pentest-report.md`

## Attendees

- CISO · ciso — present
- threat-modeler · threat-modeler — present
- code-auditor · code-auditor — present
- pen-tester · pen-tester — present
- compliance-officer · compliance-officer — partial (reviewed artifacts, async)

## Agenda

1. Pen-test findings review
2. Waiver request from CPO for a11y medium-severity findings (referred by council-qa)
3. CISO second-pass signoff decision

## Discussion

### Pen-test findings review
- 2 Low-severity findings (missing CSP on /public, overly-permissive CORS on /api/v1).
- No High or Critical.
- Cites `security/pentest-report.md:14` and `:78`.

### Waiver for a11y mediums
- This council does not waive a11y. Referring to CQO council for their call; noting here for cross-council audit trail.

### Signoff decision
- 2 Low findings fixable in < 1 day. Engineering takes fix; second-pass rerun before deploy. No waiver from security side.

## Decisions

- **D1** — Security second-pass BLOCKED on 2 Low findings; fix required — ADR not required (routine fix loop, not a waiver)
- **D2** — No security-side waiver on a11y mediums; deferred to CQO — no ADR (non-decision)

## Action items

- **A1** — Add CSP to /public routes — owner: backend-dev — due: 2026-04-24 — task: T-0034
- **A2** — Tighten CORS on /api/v1 to app origin — owner: backend-dev — due: 2026-04-24 — task: T-0035
- **A3** — Re-run pen-test second-pass after fix — owner: pen-tester — due: 2026-04-24 — task: T-0036

## Open questions

- (none)
```

## Never

- Skip the Ended: timestamp. Meetings that don't end, don't end.
- Empty Decisions section with full Discussion. Either reach a decision or note "no decision; carry to <next meeting>".
- Empty Attendees. At minimum chair + one other.
- Missing ADR link on a decision that fired a trigger.
