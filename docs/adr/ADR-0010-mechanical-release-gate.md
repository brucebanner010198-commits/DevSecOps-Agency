---
adr: 0010
title: A mechanical release gate without a fifth veto (E4)
status: draft (not proposed; awaiting the Chairman)
date: 2026-11-24
deciders: user (pending)
kind: constitution-amend
related: design review 1 (E4), alignment plan Part 6 (G8), scripts/release_check.py, skills/gates
---

# ADR-0010: A mechanical release gate

## Status

**Draft.** Written under the Chairman's 2026-11-24 delegation so that the decision is ready when they take it. Under `CONSTITUTION.md` §10.4, an amendment is USER-ONLY. Nothing here takes effect, and `CONSTITUTION.md` is unchanged, until the Chairman approves it and the §10.3 review roll is complete.

## Context

- **Blocking reds.** §3.3 gives four councils a veto, and only the User can waive a blocking red (§2.2 clause 4, §8.4).
- **Informing reds.** §3.4 and `skills/gates` let the CEO waive a red from an informing council after "logging user consent". That includes a quality (CQO) red against the acceptance criteria. Design review 1 (E4) found that the CEO can therefore ship with failing acceptance tests.
- **Plan G8.** Plan Part 6's G8 passes only on "every prior gate green or formally waived; acceptance against the original requirements".
- **Evidence.** The advisory `scripts/release_check.py` shows that in runs G1 and G2, CEVO, CRT and CAO never rendered a verdict. Nothing stopped the ship.

## Options

- **(a)** Make CQO a fifth blocking council. That is a larger amendment, because it changes the four-council structure.
- **(b) Recommended.** A mechanical G8:
  - the release passes only when the record shows each phase gate green by its own verifier, or waived by the User;
  - every §3.3 council has recorded its own verdict;
  - acceptance failures go to CEVO's existing veto;
  - the CEO loses the informing-red waiver at release.

**Whether Legal (GC) blocks** is a separate choice for the Chairman. `skills/gates` treats GC as blocking today, and the Constitution lists Legal as informing.

## Redline (§10.2), option (b)

```diff
@@ §3.4 Informing-only councils
-Every council not in §3.3 is informing-only. Informing chiefs raise ADRs, publish reports, contribute to gates — but they do NOT veto ship on their own authority.
+Every council not in §3.3 is informing-only. Informing chiefs raise ADRs, publish reports, contribute to gates — but they do NOT veto ship on their own authority.
+At the release gate (§8.6), an informing red can be waived only by the User; the CEO MAY NOT waive it.
```

```diff
@@ Article VIII — Governance
+### §8.6 Release gate
+
+A release passes only when, for the release candidate:
+
+1. each phase gate is `green` or `n/a` as recorded by its own verifier, or carries a User-signed waiver;
+2. each §3.3 blocking council has recorded its own verdict (a council record, not the CEO's status
+   entry), and none is `red` without a User-signed waiver;
+3. acceptance against the original requirements is part of CEVO's verdict, so an acceptance failure is a
+   CEVO red.
+
+The check is mechanical: `scripts/release_check.py` (or its successor) computes it from the receipts,
+and a release without a passing check is a §11.3 CAO red.
```

## Effect on other root documents (§10.2)

| Document | Effect |
| --- | --- |
| `GOVERNANCE.md` | The waiver row for informing reds changes its approver from CEO to User, at release. |
| `MISSION.md`, `VALUES.md`, `RESILIENCE.md` | None |

## Rollback

Remove §8.6 and the added §3.4 sentence by a second amendment. The advisory script stays.

## Review roll (§10.3)

CAO and CRT (mandatory), CEVO (this touches eval and acceptance), and CISO (this touches waivers).
