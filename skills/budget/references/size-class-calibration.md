# size-class-calibration — picking a project's budget class

Authoritative decision tree for initial budget sizing.

## Decision tree

1. **Single-screen app or a CLI utility?** → `small` (75 k tokens, $1.50).
2. **Full-stack web app with auth + DB + deploy?** → `medium` (250 k tokens, $5.00).
3. **Multi-service architecture OR heavy AI/ML use OR ≥ 2 external integrations?** → `large` (1 M tokens, $20).
4. **Does the user set an explicit budget in the top-5 commit phase?** → `custom`, declared amount.

Ambiguous projects default **up** (small → medium; medium → large). Over-provisioning fails soft; under-provisioning triggers Rung 6 and wastes turns.

## Worked examples

- "A bill-splitter like Splitwise, iOS-only, no auth." → `small`.
- "A bill-splitter with shared accounts, Stripe payouts, web + iOS." → `medium`.
- "A personal finance app with bank connections (Plaid), AI categorization, budget recommendations, web + iOS + Android." → `large`.
- "Generate a landing page." → `small`.
- "Build a Kubernetes operator." → `large`.
- "Rewrite this CLI tool in Rust." → `small` unless the tool is large-class (> 5 k LoC).

## Triggers to re-class mid-flight

Never do this without an ADR. Re-class events:

- Design phase reveals the brief undersold scope — Chiefs convene, CEO files ADR proposing re-class, user confirms in a brief user-meeting.
- Blocking-council red on under-spec'd threat model pushes scope into `large`.
- Discovery surfaces a pivot that changes scope tier.

## Class-specific watermarks

### small

- Build phase cap: 30 k tokens. Blown = likely scoped wrong; not a fix-loop problem.
- Total burn at close typically 50–75 k.

### medium

- Build phase cap: 100 k tokens. Blown = likely needs re-class to large or a scope-pivot (ladder Rung 5).
- Total burn at close typically 180–250 k.

### large

- Build phase cap: 400 k. Blown = the work is a portfolio of features; split via idea-pipeline into sub-projects instead.
- Total burn at close typically 700 k–1 M.

## Anti-patterns

- Don't class by "how long it should take." Class by scope + dependencies + integration count.
- Don't default to `large` for safety. Over-provisioning erodes the signal.
- Don't defer class-setting to mid-build. It must be set at OKR derivation.
- Don't let a custom class bypass ADR discipline. Custom overrides file an ADR citing the why.
