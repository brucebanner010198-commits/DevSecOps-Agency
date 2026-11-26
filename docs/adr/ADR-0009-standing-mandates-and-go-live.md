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

Add a §2.6 "Standing mandates" that lets the User pre-approve a named, bounded class of a §2.2 clause 7 or 8 action for one product. Mandates M1 to M4 and M7 can be granted. M5 (money) and M6 (egress) are excluded from §2.6; each needs its own amendment.

Add a go-live gate (G9) to `skills/gates`. The first public release of a product, and any release outside a mandate, needs the User's signature.

## Redline (§10.2)

```diff
@@ Article II — The Chairman of the Board (The User)
+### §2.6 Standing mandates
+
+The User MAY grant a standing mandate that pre-approves one named class of a §2.2
+clause 7 or clause 8 action for one product. A mandate:
+
+- is written as an ADR `kind: standing-mandate`, naming the product, the action
+  class, the cap (count, money or scope) and the accounts or targets it covers;
+- expires on a calendar date no more than 90 days away. On expiry it lapses, and a paired expiry ADR is filed, as for waivers (§8.4); nothing clears silently (§7.4, §11.6);
+- is revocable by the User at any time, effective immediately;
+- is receipted: every use appends a receipt that names the mandate, the action and its result;
+- never covers the first public release of a product, a production data deletion,
+  a new account or credential, or any action outside its cap. Those stay USER-ONLY.
+
+A mandate never waives a gate: a blocking-council red, a §8.4 non-waivable finding and the
+release gate all still apply to every action under it.
+
+Money (clause 8, M5) and research egress (M6) cannot be granted under this section; each
+needs its own amendment.
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

## Open questions for the Chairman (from round 1)

Each has a recommended option. None is decided here.

1. **Which clauses does §2.6 amend?** The §2.2 preamble ("no prior consent"), §2.3 (an ADR per action) and §9.4 (publishing and spending are irreversible) all conflict with standing consent. *Recommended:* amend all three in this ADR, each with a "except within a standing mandate under §2.6" clause.
2. **How does the Chairman sign a mandate?** *Recommended:* only through `user-meeting` (a direct call) or `board-meeting`, recorded in `inbox.json` with an approval timestamp. An agent-written ADR is never a mandate.
3. **Who reviews a grant?** CAO also audits mandate receipts, so reviewing grants would break §3.5. *Recommended:* CISO and GC review the grant, CAO audits only the receipts, and no M2 to M4 executor comes from CAO, CEVO, CRT or CSRE.
4. **Define "first public release" and "outside a mandate" for G9,** and add the `skills/gates` redline. *Recommended:* the first time a product is reachable by anyone other than the Chairman. A staging URL open to the internet counts.
5. **Secrets.** *Recommended:* a mandate holds only a vault reference, scoped to its named target and revoked when the mandate ends. A raw secret in a mandate or receipt is a §8.4 non-waivable finding.
6. **Receipts and failure.** *Recommended:*
   - add mandate receipts to §5.2 (append-only);
   - one failed use suspends the mandate until the Chairman reviews it;
   - register the `standing-mandate` ADR kind.
7. **Security preconditions for M2 to M4.** *Recommended:* SBOM, SLSA provenance and a non-red CISO verdict before each use (§5.7).
8. **Are M1 (heartbeat) and M7 (housekeeping) mandates at all?** Neither is a clause 7 or 8 action. *Recommended:* drop both from §2.6, since they need no USER-ONLY carve-out.

### Round 1 (2026-11-26, read-only, each agent on its own tier, full files)

Pasted unedited. Round 1 did not approve either ADR. The fixes below restate existing clauses only. Every other objection is an open question for the Chairman, so no second round runs until the Chairman has answered them.

#### CRT (`red-team-lead`)

**Limits:** I couldn't dispatch adversarial-prompter, so no jailbreak or injection tests were run. Both verdicts come from a static read.

**VERDICT 13: REJECT (revise)**
1. The line "no push to a protected branch" (pr13.diff:102) narrows §2.2 clause 7, which reserves every push to the User (CONSTITUTION.md:81). Reword it to "no push, merge or publish without the Chairman".
2. Bug fixes and dependency patches enter at G5 (diff:85-86). That skips CISO and CRT review, and the CEO assigns the class itself with no re-check. Require CISO review on every dependency change and a CAO check of the classification.
3. A baseline break is "a red" (diff:104) with no owning council. The skill holds only tests, not the security-scan or licence baselines (adopt/SKILL.md:82-97). Name CEVO as owner and hold all baselines.
4. Close (diff:113) lets the CEO mark `done` without requiring non-red gates. It also edits status in place, so use appended rows (§5.2 spirit).
5. The precondition (diff:66) is never verified. Run adopt's commit-drift check (adopt/SKILL.md:148) first.
6. Role cards: the new `_agency/cr/` scope (yaml:68) is fine. But the spec-as-is, system-map and user-doc updates (diff:107-109) have no owner in any write scope (yaml:126), and `write_scope_note` is stale (yaml:74).

**VERDICT 14**
**ADR-0009: REJECT.** It weakens existing gates.
- Clauses 7 and 8 are carved out (ADR-0009:60-61), but a mandate is nowhere barred from clearing a blocking red or bypassing G8. M2, M3 and M4 releases could skip §3.3 and CRT's unpinned-hash check. Add: "a mandate never waives a gate; every mandated release passes §8.6".
- The §2.2 preamble still says no prior consent counts (CONSTITUTION.md:72), and §9.4 says publishing and spending are irreversible. Amend both.
- "Lapses silently" (ADR-0009:45) contradicts §7.3's ban on silent clears and has no paired expiry ADR as in §8.4.
- It never says how the User signs a mandate. Require `user-meeting` and `inbox.json` plus an approval timestamp. Otherwise an agent-written ADR can pass as a mandate.
- G9 is named (ADR-0009:34) but has no `skills/gates` redline, and "public" is undefined. A staging deploy can be internet-reachable.
- M5 and M6 are only "listed" (ADR-0009:32). The §2.6 text already allows spend. Exclude money and egress in the redline until a separate decision.

**ADR-0010: REJECT.** The intent is sound, but the evidence rules weaken the gate.
- The red check reads CEO-written `status.json` (release_check.py:13, 107), so the CEO can omit a red. Read the council's own artifact instead.
- "Recorded" means any non-log write (release_check.py:104-106). That is gameable.
- The waiver test accepts any `waivedBy: user` string (release_check.py:112-114). It checks no ADR, expiry or scope, and ignores the non-waivable ASI and secret classes (CONSTITUTION.md:347). §8.6 line 50 must require a live `waiver-grant` ADR.
- `n/a` is self-declared (ADR-0010:50). Require a verifier record.
- The script exits 0 with flags (release_check.py:142-152), so it can't act as a gate.
- Acceptance is folded into CEVO (ADR-0010:53), but §3.3's CEVO triggers don't cover it (CONSTITUTION.md:131). Amend §3.3 too.
- `skills/gates:41` and `skills/waivers:15` conflict with the new rule that only the User waives an informing red at release.

#### CAO (`cao`)

**CAO verdict (§10.3 integrity and independence): ADR-0009 REJECT, ADR-0010 REJECT. Both can return once the fixes below are made.**

**ADR-0009**
1. **Redline anchor.** The hunk header says "The Sovereign (The User)" (ADR-0009:45). Base has "The Chairman of the Board (The User)" (CONSTITUTION:64). The clause 7 and 8 text matches base lines 80-81.
2. **Conflicting clauses.** The redline leaves §2.2's intro (CONSTITUTION:72, "prior consent in another decision"), §2.3 (:87, per-action ADR) and §9.4 (:375, spending and publishing are USER-ONLY) untouched. It also leaves §2.4 unaddressed. Amend or carve out each of them.
3. **Silent lapse.** ADR-0009:50 says a mandate "lapses silently". §7.4.3 and §11.6 (CONSTITUTION:311, :485) forbid silent clears and silent enforcement. Mirror §8.4's paired expiry ADR (:344).
4. **Independence.** ADR-0009:74 makes CAO a reviewer of mandate grants. CAO must also audit mandate receipts, and §3.5 (:150) bars auditing a decision you helped produce. Use CISO and the GC as reviewers, and keep CAO as receipt auditor only. Also state that the executor of M2-M4 cannot come from CAO, CEVO, CRT or CSRE (§3.5, :152-153).
5. **Scope mismatch.**
   - M1 and M7 (heartbeat, housekeeping) are not clause 7 or 8 actions (:32).
   - §2.6 caps "money" (:41), which enables M5 even though :32 says M5 needs its own decision. Exclude money explicitly.
6. **Missing pieces.**
   - Receipts are not on the §5.2 append-only list (:213-223).
   - `standing-mandate` is not a registered ADR kind.
   - The G9 change to skills/gates has no redline.
   - The rationale has no file:line citations (§5.1, :209).

**ADR-0010**
1. **Non-waivable classes.** §8.6.2 (ADR-0010:50-52) allows a User waiver for any red. §8.4 (CONSTITUTION:347) makes ASI-class and raw-secret findings never waivable. Add the carve-out.
2. **CEVO scope.** Acceptance becomes a CEVO red (ADR-0010:51), but §3.3's CEVO triggers (CONSTITUTION:131) are not amended. CEVO must also not write the acceptance items for work it evaluates (§3.5, :151).
3. **Script mismatch.** `release_check.py` always exits 0 (:152) and does not check phase gates. Its "recorded" test is any non-log write (:11-12, :104-105), which does not match "mechanical" (ADR-0010:56) or §8.6.1. Fix the script or soften the clause.
4. **Conforming edits.** skills/gates:41 and :122-128 still let the CEO waive informing reds. List this edit as a required follow-on. Define "release" and say whether §2.6 mandated releases (M2-M4) fall under §8.6.
5. **Citations.** The G1/G2 evidence (ADR-0010:20) has no file:line.

**Independence.** No auditor loses it in ADR-0010. In ADR-0009 only the CAO-reviewer role fails (point 4 above).

#### CEVO (`evaluation-lead`)

**CEVO verdict on ADR-0010: REJECT as drafted. I'd approve it once the fixes below are made.**

**What works**
- Item 3 (ADR-0010:53-54) puts acceptance failures under CEVO's existing veto. I can do that with no new council. It matches plan G8 (ADR-0010:21).
- Removing the CEO's informing-red waiver at release (ADR-0010:41) closes the E4 hole (ADR-0010:20).

**Gaps that weaken eval and regression gates**
1. **Acceptance is not defined.** CEVO's red triggers are only ≥5pp regression, skill-eval below threshold, and σ/μ > 0.15 (CONSTITUTION.md:131). The ADR doesn't add an acceptance trigger to that line. It also doesn't name where the "original requirements" are kept. Fix: amend line 131 to say that a failed acceptance item is a red. Say the eval set is derived from the original brief and OKRs at close, and never edited afterwards. My role card already forbids retroactive items.
2. **The mechanical check can't see eval reds.** `release_check.py` takes the colour from `status.json`, which the CEO writes (release_check.py:13-14, 107-111). It flags only a literal `red` (:120). A CEO who records `yellow` for a ≥5pp regression passes. Fix: §8.6 should require the verdict colour to come from the council's own file, such as `_vision/eval/<date>-<slug>-close.md`. A mismatch with `status.json` should fail the check.
3. **"Recorded" means any write.** Any non-log file written by a council agent counts as a verdict (release_check.py:12, 104-106). A scratch file would satisfy the check. Fix: require the specific eval artifact, with a gate line and a regression section.
4. **§8.6 item 1 (phase gates) is not implemented.** The script never reads phase gates. Item 1 is also unenforceable until it says what "its own verifier" means for each phase.
5. **Receipts from other runs can count.** With no `--project`, `under()` returns True for every path (release_check.py:67-69). Receipts from other projects or runs would satisfy a release. Fix: make `--project` and `--since` mandatory in gate mode.
6. **The ADR says "or its successor" (ADR-0010:56).** A weaker successor could replace the check without another amendment. Fix: name the script and require an amendment to change it.
7. **Yellow passes.** Item 2 blocks only red (ADR-0010:52). State that a regression above 5pp must be red, never yellow. That keeps my rule that regressions are never shipped green.

#### CISO (`security-lead`)

**CISO review, CONSTITUTION §10.3 (waivers, go-live, secrets, security posture)**

**ADR-0009: REJECT (revise and resubmit)**

1. **The mandate cap on the first release is real but vague.** ADR-0009:49-51 puts the first public release, production data deletion, new credentials and anything outside the cap out of mandate. It does not define "first public release". It also does not define "outside a mandate" for G9 (ADR-0009:34). Fix: define both terms.
2. **No secrets rules.** The ADR defers "scoped tokens" and "a narrow deploy tool" to a non-binding section (ADR-0009:72-76). CONSTITUTION §5.5 (:237) requires vault refs only. Fix: write into §2.6 that a mandate holds a vault ref only. The ref must be scoped to the named target and revoked when the mandate lapses or is revoked. A raw secret in a mandate or receipt is non-waivable (§8.4, :347).
3. **Silent lapse.** "Lapses silently" (ADR-0009:48) conflicts with §7.4 clause 1 and §11.6 (:310, :485). Fix: file a closing ADR or receipt on expiry, as waivers do (skills/waivers:46,50).
4. **Revocation and receipts are weak.** "Effective immediately" (ADR-0009:49) has no mechanism. Nothing says receipts must be append-only (§5.2, :211-225). Nothing says a failed use halts the mandate. Fix: add all three.
5. **Mandate class creep.** M2 (staging deploy) and M4 (patch updates) can still change security posture. M5 and M6 (money, egress) are listed in ADR-0009:21-28, but §2.6 has no clause that stops them being granted without their own decision. Fix: state that M5 and M6 are not grantable under §2.6.
6. **CISO review is missing.** The review roll names CISO (ADR-0009:86), but the redline gives CISO no veto over a mandate-covered release. Fix: SBOM, SLSA and a CISO non-red must be preconditions (§5.7, :245).

**ADR-0010: APPROVE with required fixes**

It tightens waivers. The CEO loses the informing-red waiver at release (ADR-0010:41), and a User-signed waiver is required (ADR-0010:50-51). This fits §3.3 and §8.4 (CONSTITUTION:135-140, 335-347).

1. **The gate must refuse non-waivable reds.** §8.6 clause 1 (ADR-0010:50) allows a "User-signed waiver" for any red. Fix: state that ASI-class and raw-secret findings are never waivable (§8.4, :347). `release_check.py:112-114` accepts any `waivedBy: user` entry. It does not check the waiver's expiry, its finding, or its project.
2. **Verdicts can be forged.** `release_check.py:104-106` counts any non-log write by a council agent as the verdict. That can be spoofed with any file, and a red verdict is never read from the council's own record. Fix: require a verdict file in a named location with a colour, not just a write.
3. **Fail-open.** `read_gates` returns `{}` on error (`release_check.py:82-83`). A missing or corrupt `status.json` then reads as no red. Fix: fail closed.
4. **Mandate/gate interaction.** State that a §2.6 mandate never bypasses §8.6.

Resolve the GC blocking question (ADR-0010:33) first. `skills/gates:39` conflicts with CONSTITUTION §3.4 (:144).
