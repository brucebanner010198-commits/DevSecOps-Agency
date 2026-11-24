---
adr: 0009
title: Standing mandates and a go-live gate (E3)
status: draft (not proposed; awaiting the Chairman)
date: 2026-11-24
deciders: user (pending)
kind: constitution-amend
related: design review 1 (E3, proposal C mandates M1 to M7), ADR-0008, alignment plan Parts 6 and 7
---

# ADR-0009: Standing mandates and a go-live gate

## Status

**Draft.** Written under the Chairman's 2026-11-24 delegation so that the decision is ready when they take it. Under `CONSTITUTION.md` §10.4, an amendment is USER-ONLY. Nothing in this ADR takes effect, and `CONSTITUTION.md` is unchanged, until the Chairman approves it and the review roll in §10.3 is complete.

## Context

- **The problem.** §2.2 clauses 7 and 8 reserve every publish and every spend to the User, with no standing permission. So the agency cannot keep a product running: each staging deploy, rollback or security patch would wait for the User. Design review 1 (E3) found that no part of the design runs a deployment or operates a product.
- **The plan.** Plan Part 6 has G9 (deployment approval: the User for high-risk or external release) and G10 (production operations).
- **The proposal.** Proposal C proposes standing mandates as the only form of standing autonomy: written, capped, expiring, revocable and receipted. The seven are:
  - M1, heartbeat;
  - M2, staging deploy;
  - M3, rollback to the last verified release;
  - M4, patch updates;
  - M5, money envelope;
  - M6, research egress;
  - M7, housekeeping.

## Decision (proposed for the Chairman)

Add a §2.6 "Standing mandates" that lets the User pre-approve a named, bounded class of a §2.2 clause 7 or 8 action for one product. Mandates M1 to M4 and M7 can be granted. M5 (money) and M6 (egress) are listed but each needs its own decision.

Add a go-live gate (G9) to `skills/gates`. The first public release of a product, and any release outside a mandate, needs the User's signature.

## Redline (§10.2)

```diff
@@ Article II — The Sovereign (The User)
+### §2.6 Standing mandates
+
+The User MAY grant a standing mandate that pre-approves one named class of a §2.2
+clause 7 or clause 8 action for one product. A mandate:
+
+- is written as an ADR `kind: standing-mandate`, naming the product, the action
+  class, the cap (count, money or scope) and the accounts or targets it covers;
+- expires on a calendar date no more than 90 days away, and lapses silently if not renewed;
+- is revocable by the User at any time, effective immediately;
+- is receipted: every use appends a receipt that names the mandate, the action and its result;
+- never covers the first public release of a product, a production data deletion,
+  a new account or credential, or any action outside its cap. Those stay USER-ONLY.
+
+A mandate is not consent for anything it does not name (§8.5).
```

```diff
@@ §2.2 The Ten USER-ONLY actions
-7. **Publishing or releasing the Agency's output externally** (GitHub push, public release, third-party broadcast).
-8. **Spending money** (tool purchase, API upgrade, paid subscription).
+7. **Publishing or releasing the Agency's output externally** (GitHub push, public release, third-party broadcast), except within a standing mandate under §2.6.
+8. **Spending money** (tool purchase, API upgrade, paid subscription), except within a standing mandate under §2.6.
```

## Effect on other root documents (§10.2)

| Document | Effect |
| --- | --- |
| `GOVERNANCE.md` | The decision matrix gains a "standing mandate" row. Proposer: CEO. Reviewers: CISO and CAO. Approver: User. |
| `MISSION.md` | None. The Chairman experience contract gains fewer interrupts. |
| `VALUES.md`, `RESILIENCE.md` | None |

## What it also needs (not part of the amendment)

- An operating account register that the User owns: host, registrar, payments, email.
- Scoped tokens for the agency.
- A narrow deploy tool.

Creating accounts and credentials stays the User's.

## Rollback

Revoke every mandate. Then remove §2.6 and restore clauses 7 and 8 by a second amendment.

## Review roll (§10.3)

CAO and CRT (mandatory), and CISO (this touches secrets and egress).
