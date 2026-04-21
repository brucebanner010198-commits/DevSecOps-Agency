# positioning — canvas worked examples

## Per-project filled example

```markdown
# Positioning — dorm-splitter

## Audience (who, one segment)
- Primary: US college students living in dorms with ≥ 2 roommates, splitting shared expenses (groceries, utilities, subscriptions).
- Secondary: off-campus shared housing during first year post-college.

## Promise (one line)
Settle shared dorm expenses in under 30 seconds per transaction, with zero-setup onboarding.

## Proof (≥ 2, cited)
- Interview cohort n=12 reported 3.2 min average time per settle-up in current tools · source: `research/interviews/2026-04-12-dorm-cohort.md:41`
- Venmo adoption 91% in target cohort · source: Pew 2024 payment-app survey
- Splitwise onboarding requires email + phone + 4 app permissions · source: `research/competitors/splitwise-tear-down.md:23`

## Wedge (why us, one sentence)
We remove the three-step onboarding friction by piggybacking on a dorm's existing shared-Venmo group-chat, with zero new accounts to create.

## Category
- Chosen: "zero-setup expense split for short-term cohabitants"
- Alternatives considered: "Splitwise for dorms" (too derivative), "micro-treasurer app" (too novel a category)
- Rationale: chosen frame reuses "expense split" as the known handle + "zero-setup" as the wedge term

## Elevator pitch (≤ 30 words)
For US dorm roommates who split shared expenses, dorm-splitter is a zero-setup expense tracker that clears balances in 30 seconds via your existing group chat, unlike Splitwise which needs 4 permissions and a new account.

## Messaging hierarchy
- H1: Split dorm expenses without another app to download
- H2: Zero-setup expense tracking that piggybacks on your existing group chat
- Value props:
  - Settle up in 30 seconds, not 3 minutes
  - No new account, no email verification, no contact import
  - Works inside your roommates' existing Venmo group
```

## Pipeline-mode example

```markdown
### dorm-splitter
- Narrative clarity: 5
- Wedge strength: 4
- Category fit: 4
- Composite: 4.5
- One-sentence elevator: "Zero-setup expense tracker for dorm roommates that clears balances in 30 seconds via your existing group chat."

### commuter-ticket-aggregator
- Narrative clarity: 3
- Wedge strength: 2
- Category fit: 3
- Composite: 2.5
- One-sentence elevator: "Unified ticket search across commuter rail systems with one-tap refunds during outages."

### research-paper-thread-explorer
- Narrative clarity: 2
- Wedge strength: 3
- Category fit: 2
- Composite: 2.5
- One-sentence elevator: "An interactive visualisation of citation graphs for academic papers that surfaces under-read work in a field."
```

## Common failures

- **Superlative without citation**: "the fastest dorm expense app" → fail. Fix: "settles balances in 30 seconds, 6× faster than Splitwise (measured n=12)".
- **Wedge that is actually a feature**: "we have better UX" → fail. Fix: "we remove onboarding friction by piggybacking on existing group chat infra".
- **Audience that is "everyone"**: fail. Fix: name one segment.
- **Elevator > 30 words**: fail. Cut until it's ≤ 30.
- **Category that doesn't exist and isn't positioned as new**: fail. Either use an existing handle or explicitly coin one.
