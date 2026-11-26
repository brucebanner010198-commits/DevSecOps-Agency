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
  - the release passes only when each blocking council's own verdict, and every informing council's gate, is not red, or is waived by the User;
  - every §3.3 council has recorded its own verdict;
  - acceptance failures go to CEVO's existing veto;
  - the CEO loses the informing-red waiver at release.

**Whether Legal (GC) blocks** is a separate choice for the Chairman. `skills/gates` treats GC as blocking today, and the Constitution lists Legal as informing.

## Redline (§10.2), option (b)

```diff
@@ §3.3 Blocking councils (strict veto)
-- **CEVO** (evaluation-lead) — ≥ 5 percentage-point regression vs. baseline, skill-eval below threshold, variance σ/μ > 0.15.
+- **CEVO** (evaluation-lead) — ≥ 5 percentage-point regression vs. baseline, skill-eval below threshold, variance σ/μ > 0.15, or a failed item of the project's acceptance set (§8.6).
```

```diff
@@ §3.4 Informing-only councils
 Every council not in §3.3 is informing-only. Informing chiefs raise ADRs, publish reports, contribute to gates — but they do NOT veto ship on their own authority.
+At the release gate (§8.6), an informing red can be waived only by the User; the CEO MAY NOT waive it.
```

```diff
@@ §8.4 Waivers
-A waiver is the only way to clear a blocking-council red without fixing the finding. Waivers:
+A waiver is the only way to clear a blocking-council red without fixing the finding, and, at the release gate (§8.6), the only way to clear an informing-council red. Waivers:
```

```diff
@@ Article VIII — Governance
+### §8.6 Release gate
+
+Every release falls under this section, including a release within a standing mandate
+(§2.6). A release passes only when, for the release candidate:
+
+1. each §3.3 blocking council has written its own verdict file in the project folder
+   (CISO `security-report.md`, CEVO `close-eval.md`, CRT `red-team.md`, CAO
+   `close-audit.md`) during this run, and was the last to write it. The file carries a
+   `gate:` line of `green`, `yellow` or `red`; a blocking council never returns `n/a`.
+   A verdict that disagrees with `status.json` fails the gate;
+2. every council's gate, blocking or informing, is `green`, `yellow` or `n/a`, or is
+   `red` and covered by a valid waiver: a `waiver-grant` ADR (§8.4) approved by the
+   User, for that council, project and finding, not yet expired. For a blocking council
+   the finding is one named in its verdict file. A §8.4 non-waivable finding (ASI-class
+   or a raw secret) is never waived here;
+3. a `yellow` verdict lists its open items, and the release record carries them;
+4. acceptance is part of CEVO's verdict. The acceptance set is derived from the User's
+   original request and the project OKRs at intake, and written to `acceptance.md`
+   exactly once, by the CEO, before any verdict. No evaluation-council agent writes it
+   (§3.5). A failed item is a CEVO red;
+5. a regression of 5 percentage points or more is always red, never yellow.
+
+The check is mechanical: `scripts/release_check.py --gate` computes items 1, 2, 4 and 5,
+and the presence of item 3's open items, from the receipts and the project records. A red
+verdict lists each finding with its class, and each finding needs its own waiver. CEVO's
+verdict carries the regression figure and one result per acceptance item. The check fails
+closed: a missing or unreadable `status.json`, a missing verdict or any flag fails the
+gate, and the check requires `--project` and `--since`. Whether the release record
+carries a yellow's open items is audited by CAO, by reading. Changing what the script
+checks needs an amendment. A release without a passing check is a §11.3 CAO red.
```

## Effect on other root documents and skills (§10.2)

| Document | Effect |
| --- | --- |
| `GOVERNANCE.md` | The waiver row for informing reds changes its approver from CEO to User, at release. |
| `skills/gates` | GC stays informing, as §3.4 lists it; its rule is no longer called blocking. The CEO can no longer override an informing red at release. Done in this PR. |
| `skills/waivers` | Covers an informing red at release. Done in this PR. |
| `skills/ceo` | Intake writes `acceptance.md` once; the CEO's card gains `acceptance.md`. Done in this PR. |
| `scripts/release_check.py` | Gains `--gate`, as above, with tests. Advisory mode is unchanged. Done in this PR. |
| `skills/gates` | States the verdict contract the script reads (paths and line shapes). Done in this PR, after round 2, so not yet reviewed. |
| `security-lead`, `evaluation-lead`, `red-team-lead`, `cao` prompts; `skills/ship-it/references/status-schema.md` | Not done. Each chief must write its verdict in the contract's shape and place, and `status.json` must carry `gates.byCouncil`. Land with the amendment. |
| `MISSION.md`, `VALUES.md`, `RESILIENCE.md` | None |

**Residuals.**
- The waiver ADR, its `approver: user` and its `class:` are written by the CEO, so the script cannot prove the User signed it or that the class is right. Signed receipts (Phase 2b) would; they wait for the Chairman's choice of a signing identity.
- An informing council has no named verdict file, so its red is read from `status.json`, which the CEO writes, and its waiver is matched on council and project only.
- Phase colours (`byPhase`) are derived from the councils' gates and are not checked separately.
- The receipts come from the guard hook, which sees only the file-write tools. An agent with a shell could rewrite a verdict after the council's receipted write, and the script would not see it.
- So the gate does not close E4 for informing councils: a CQO or GC red recorded as green in `status.json` passes. Round-2 question 4 below proposes their own verdict files.

## Rollback

Remove §8.6, the added §3.3 trigger and the added §3.4 sentence by a second amendment, and revert the conforming edits. Advisory mode of the script stays.

## Review roll (§10.3)

CAO and CRT (mandatory), CEVO (this touches eval and acceptance), and CISO (this touches waivers).

## Evidence added after round 1

Run N4 (2026-11-26, `docs/vision/CEO-ENTRY-REVIEW.md`) went end to end on a tip calculator. CEVO gave yellow with none of the three project goals proven, and no rule stopped a yellow close. The CEO closed it "blocked" only because the tests had not run.

## Chairman's decisions on the round-1 questions (2026-11-26 UTC)

**In the chat interface,** the Chairman was asked to "Accept the recommended options in drafts #13 and #14, then run their second review", and replied "Accept all defaults". So the recommended option of each round-1 question is now the decision, and the redline above carries it.

This is not approval of the amendment (§10.4). The Chairman approves the final text after the second review.

| # | Round-1 question | Decision |
|---|---|---|
| 1 | Where does a verdict's colour come from? | Each blocking council's own verdict file, with a `gate:` line, last written by that council in this run. A blocking council never returns `n/a`. A mismatch with `status.json` fails |
| 2 | Fail closed, and is it a gate? | Yes: `--gate` exits non-zero on any flag, a missing or corrupt `status.json` fails, and `--project` and `--since` are required |
| 3 | What is a valid waiver? | A live `waiver-grant` ADR approved by the User for that council, project and finding (for a blocking council, a finding named in its verdict file), never for a §8.4 non-waivable class. §8.4 is amended so a waiver can also clear an informing red at release |
| 4 | Acceptance under CEVO | §3.3's CEVO triggers gain a failed acceptance item. The set is written to `acceptance.md` exactly once, by the CEO at intake, before any verdict, and never by the evaluation council |
| 5 | Does yellow pass? | Only with its open items listed. A regression of 5 points or more is always red |
| 6 | "Or its successor" | Removed. The script is named, and changing what it checks needs an amendment |
| 7 | Conforming edits | `skills/gates` and `skills/waivers` changed in this PR |
| 8 | Does GC block? | No. GC stays informing; `skills/gates` is fixed |
| 9 | Mandated releases | Always under §8.6 |

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

### Round 2 (2026-11-26 UTC, read-only, each agent on its own tier, full files, $1.19)

Round 2 checked whether the text and the script implement the Chairman's decisions faithfully. All four reviewers rejected it. Their verdicts are pasted unedited below, followed by the response. No round 3 has run: the Chairman approves the final text first.

#### CRT (`red-team-lead`): REJECT

I'm finishing the read-only review now. I've read both ADRs, the script, its tests, the guard, the role cards and the diff, and I'm writing up the fidelity check and the new findings. I ran no code and dispatched no one. This is a static read.

## Round-1 objections and accepted options

**ADR-0009, mine**
- **Mandate never waives a gate:** implemented (ADR-0009:88-89).
- **Preamble and §9.4:** implemented (ADR-0009:96-97, 129-130).
- **Silent lapse:** text implemented (ADR-0009:78-79). No agent is named to file the expiry ADR.
- **How the User signs:** only partly implemented. See finding 5.
- **G9 and "public":** implemented. G9 has a redline and "public" is defined (ADR-0009:118-124).
- **M5 and M6:** excluded (ADR-0009:50-51, 62-63).

**ADR-0010, mine**
- **Verdict colour from the council's own file:** implemented for the four blocking councils (release_check.py:238-258).
- **"Recorded" meaning any write:** implemented. The check now needs a named verdict file with a `gate:` line.
- **`waivedBy` string accepted as a waiver:** partly implemented. See findings 1 and 2.
- **Exit code:** implemented (release_check.py:312).
- **§3.3 CEVO trigger:** implemented (ADR-0010:323-325).
- **`skills/gates` and `skills/waivers` conflicts:** fixed.
- **`n/a`:** blocking councils can no longer return it. That is acceptable.
- **Accepted options 3 to 9:** implemented as written, except where the findings below say otherwise.

## Findings

**VERDICT: REJECT**

1. **One waiver clears a whole red verdict, and the finding match is a substring match** (release_check.py:244, 257). `waived_here` is true if any waived finding id appears anywhere in the verdict text. A red verdict with findings rt-01 and rt-02 passes when only rt-01 is waived. A CEO-written waiver with `finding: a` or `finding: 1` matches any file. ADR-0010:68-70 says the waiver is "for that … finding".
   - Fix: require every high-or-worse finding id in the file to be waived, and match ids as whole tokens.
   - The tests never cover a multi-finding red or a short id (test_release_check.py:821-834).

2. **The non-waivable check fails open** (release_check.py:69, 201). A waiver with no `class:` passes. `ASI-03` or `asi-llm01` also passes, because only the exact strings `asi`, `asi-class` and `raw-secret` are blocked. The CEO writes `class:`, so omitting it is enough.
   - Fix: require a non-empty `class:`. Refuse anything starting with `asi` and anything secret-like.

3. **An informing red is only as good as `status.json`, but the text claims more** (release_check.py:266-268, ADR-0010:52).
   - The CEO writes `status.json`. A red can be recorded as yellow or left out, and no flag is raised.
   - Any waiver for that council clears the red, whatever the finding (release_check.py:267).
   - The §3.4 sentence "the CEO MAY NOT waive it" and §8.6 item 2 ("for that council, project and finding") are therefore not enforced. The residuals at ADR-0010:99 admit part of this.
   - Fix: either soften the redline to match, or require an informing-council verdict artifact.

4. **The "last writer" and "this run" evidence is weaker than the redline says** (ADR-0010:62-66, release_check.py:241-243, guard.py:42-44).
   - Receipts come from the hook, and the guard says shell commands are not inspected. Any agent with a shell can rewrite a verdict file or `acceptance.md` after the council's receipted write. The script reads file content and never binds it to a hash, so the check still passes.
   - `--today` (release_check.py:303) is caller-supplied. Passing a past date makes an expired waiver live.
   - Fix: remove `--today` from the CLI. State the shell limit in §8.6 or in the residuals.
   - Also, the text never says who runs `--gate`. Nothing makes the CEO run it, and the only consequence is a later CAO red (ADR-0010:82-83).

5. **The User's approval of a mandate is evidenced by a file every agent can write** (ADR-0009:66-70, guard.py:88).
   - `inbox.json` is in `SHARED_WRITES`, so every agent can write it. It is not on the append-only list, so past entries can be edited.
   - "An agent-written ADR alone is never a mandate" therefore has no check behind it. A forged `inbox.json` entry plus an ADR passes.
   - Revocation "effective immediately" still has no mechanism, and no agent is named to file the expiry ADR.
   - Fix: require `inbox.json` to be append-only for the user entry type, or defer mandates until signed receipts exist.

6. **ADR-0009 depends on ADR-0010 and does not say so** (ADR-0009:8, 88-89, 123-124).
   - §2.6 and G9 cite §8.6 and §8.4's waiver rule. If ADR-0009 is approved alone, those references point at nothing, and "a mandate never waives a gate" has no gate to reference.
   - The `related:` field omits ADR-0010.
   - Fix: add a dependency line. Make ADR-0009 take effect only with or after ADR-0010.

7. **§8.6 items 3 and 5 are stated but not implemented** (ADR-0010:57, 62; release_check.py:259, 175-176).
   - Any bullet under "## Open items", including `- none`, counts as listed open items.
   - Yellow is not checked for informing councils.
   - Nothing checks that "the release record carries" the open items.
   - The 5-point regression rule is only the verdict author's job. Nothing compares a number.
   - Fix: reject `none` bullets. Either soften the redline or add a regression field that the script checks.

8. **"Release" is still undefined** (ADR-0010:59). This was an earlier CAO request. A rollback under M3 (ADR-0009:32) needs four fresh blocking verdicts under §8.6 in the same run. That may not be workable in an incident, and the ADR does not say. Define "release", and say whether a rollback needs a fresh run.

9. **The verdict parser takes the first `gate:` line anywhere in the file** (release_check.py:169-171). A council quoting an old `gate: green` in a finding excerpt earlier in the file would set the colour. Low severity. Fix: read only a front-matter or first-heading `gate:` line.

10. **Residual items outside the diff:**
   - The guard's append-only list and the role-card change for mandate receipts are deferred to after approval (ADR-0009:139).
   - `hooks/guard.py:64-77` therefore does not protect `_decisions/mandates/*.jsonl` yet. That matches the ADR, but until it lands, §5.2's new line has no enforcement.

#### CAO (`cao`): REJECT

**ADR-0009 and ADR-0010 are not ready yet.** Every one of my round-1 objections on ADR-0009 is fixed. For ADR-0010 two are only partly fixed, and the script I reviewed has defects that weaken §8.4. This was a static read. I ran nothing. Line numbers refer to `review/change.diff`.

**ADR-0009: my round-1 points**
1. **Anchor.** Fixed. The hunk now reads "Chairman of the Board" (diff 59).
2. **Conflicting clauses.** Fixed. The redline carves out the §2.2 preamble, clause 7, §2.3 and §9.4, and leaves clause 8 alone (diff 94-131). §2.4 is used as the signing channel (diff 66).
3. **Silent lapse.** Fixed. A paired expiry ADR is filed, mirroring §8.4, and nothing clears silently (diff 78-79).
4. **Independence.** Fixed. CISO and GC review grants and CAO audits receipts only. No agent of CAO, CEVO, CRT or CSRE executes a mandated action (diff 71-73).
5. **Scope.** Fixed. Only M2, M3 and M4 can be granted, and M1, M5, M6 and M7 are out of scope.
6. **Missing pieces.**
   - The §5.2 receipts line and the G9 redline are present.
   - The ADR kinds are registered only in the effects table (diff 138), not edited yet. That is acceptable because conforming edits land after approval.
   - The rationale still has no file:line citations. This was not fixed (see finding 6).

**ADR-0009: accepted options**
- All eight rows are implemented faithfully in the redline, with the two exceptions below.
- Row 2: an agent-written ADR alone is never a mandate. The text implements this (diff 64-67).
- Row 6: a failed use suspends the mandate, but nothing records the suspension (finding 4).

**ADR-0010: my round-1 points**
1. **Non-waivable classes.** The redline carve-out is in (diff 355-356). The script implements it only partly (finding 3).
2. **CEVO scope.** The §3.3 trigger is amended (diff 325). `acceptance.md` is written once by the CEO, and the script enforces the writer and the ordering (diff 713-723). The CEO card and `hooks/role-cards.json` gain the file. This is fixed.
3. **Script mismatch.** Mostly fixed. `--gate` exits 1 on any flag. It requires `--project` and `--since`, and it fails closed on `status.json`. It reads each council's own verdict file and checks who wrote it last. Phase gates are dropped from §8.6 and disclosed as a residual, but the Options text still promises them (finding 7).
4. **Conforming edits.** `skills/gates`, `skills/waivers` and `skills/ceo` are edited, and mandated releases are explicitly under §8.6. But "release" is still undefined (finding 2), and the skill edits land ahead of the Constitution (finding 5).
5. **Citations.** Not fixed. The G1/G2 evidence (diff 307) has no file:line, and the N4 evidence names a file without a line.

**ADR-0010: accepted options**
- 1 (verdict file), 2 (fail closed), 4 (acceptance), 6 (no "or its successor") and 8 (GC informing) are implemented.
- 3 (waiver validity) is not faithful to "that council, project and finding" (finding 1).
- 5 (yellow, and a regression of 5 points or more is always red) is only half mechanical. The script checks open items, but the regression rule rests on CEVO's own `gate:` and `acceptance:` lines.
- 9 (mandated releases under §8.6) is stated, but it creates a conflict for M3 (finding 8).

**New or remaining defects**
1. **The script breaks the §8.4 one-finding rule.**
   - A blocking red passes if any one waived finding id appears anywhere in the verdict text (diff 688). A red with two findings is cleared by one waiver.
   - The match is a substring test, so `sec-7` also matches `sec-70`.
   - An informing red is cleared by any waiver for that council, with no check on the finding (diff 710-712).
   - Row 3 and §8.6 item 2 say "for that council, project and finding", so the script does not implement what the text promises. The ADR lists the informing case as a residual, but the blocking case is undisclosed.
   - The tests (diff 821-834) never cover a two-finding red.
2. **"Release" is undefined** (diff 344), although I asked for a definition in round 1. Also undefined: whether a patch or a rollback is a "release candidate", and what `--since` means for one.
3. **A missing `class:` counts as waivable.**
   - The script's non-waivable list is the exact tokens `asi`, `asi-class` and `raw-secret` (diff 590, 645). A waiver with no class, or with a class like `ASI-03`, passes.
   - The class is CEO-written. For a CRT red, the script should fail closed unless the waiver carries an explicit waivable class.
   - Only `raw-secret` is tested.
4. **§2.6 suspension and revocation leave no trace.**
   - One failed use suspends a mandate, but no receipt or ADR records the suspension or its lifting (diff 81-82).
   - That is the same silent-state problem I raised on expiry.
   - Add a suspension or revocation receipt.
5. **The skill edits take effect early.**
   - `skills/gates` and `skills/waivers` now cite §8.6 and say the CEO "cannot override" an informing red. The in-force Constitution has no §8.6, and §3.4 lets the CEO do exactly that (diff 916-923, 936).
   - The live skills therefore contradict the in-force Constitution. ADR-0009 defers its conforming edits until approval, so the two ADRs are inconsistent.
   - `GOVERNANCE.md` is not edited at all (diff 375).
6. **A few smaller gaps.**
   - §8.4's "reviewed by the blocking Chief" has no reviewer for an informing waiver.
   - §8.6 does not say who runs `--gate`. If the CEO runs it, the result is self-attested. Name CAO or CI, so CAO's §11.3 red has a defined trigger.
   - The §8.4 90-day cap and the paired `waiver-expiry` ADR are not checked by the script.
   - The "yellow … release record carries them" requirement is not checked.
   - The file:line citations asked for in round 1 (ADR-0009 rationale, ADR-0010 G1/G2) are still missing.
7. **The Options text is stale.** Option (b) still promises "each phase gate green by its own verifier" (diff 313), but the redline dropped it.
8. **M3 rollback conflicts with §8.6.**
   - §8.6 asks for fresh verdicts from all four councils "during this run", plus an `acceptance.md` that was written once.
   - A rollback to the last verified release cannot satisfy that.
   - The mandate then either cannot be used in an incident or invites a bypass.
   - State that a rollback to a release that already passed §8.6 reuses its record, or say plainly that it needs fresh verdicts.

VERDICT: REJECT

1. `scripts/release_check.py` (diff 688, 710-712; tests diff 821-834): require the waiver to match the red's finding exactly, one waiver per finding. Add a two-finding test.
2. ADR-0010 §8.6 (diff 344): define "release", and say how patches, rollbacks and `--since` are handled.
3. `scripts/release_check.py` (diff 590, 645): fail closed on a missing class and on `ASI-*` classes. Add a test for each.
4. ADR-0009 §2.6 (diff 81-82): require a receipt or ADR for suspension and revocation.
5. `skills/gates` and `skills/waivers` (diff 916-936) and `GOVERNANCE.md`: hold these edits until approval, or state their dependency on §8.6.
6. ADR-0010 §8.4 and §8.6 (diff 335-338, 364-368): name the informing-waiver reviewer and the `--gate` runner. Add the missing citations.
7. ADR-0010 Options (diff 313): align it with the redline.
8. ADR-0009 §2.6 and ADR-0010 §8.6: resolve the M3 rollback conflict.

#### CEVO (`evaluation-lead`): REJECT

I'm checking the round-1 CEVO objections against the final ADR text, the script and its tests. That check is finished, so this is my verdict.

**CEVO round-2 verdict on ADR-0010.** The ADR and its mechanical gate cover most of my round-1 objections. Two of them (4 and 7) are only partly met, and the script has an exploitable gap in how it matches waivers.

**My round-1 objections**
- **1, acceptance undefined: implemented, with one gap.**
  - The §3.3 trigger now includes a failed acceptance item (ADR-0010:40).
  - `acceptance.md` is written once by the CEO at intake, before any verdict, and never by the evaluation council (:73-76; release_check.py:269-279).
  - I had asked for derivation at close. Intake is the Chairman's choice and is stricter, so I accept it.
  - The gap is that `acceptance: pass` is a bare line (release_check.py:262-265). Nothing ties it to the items in `acceptance.md`.
- **2, colour from the council's own file: implemented.** The verdict must come from the council's own file and match `status.json` (release_check.py:254-256, ADR-0010:62-66). The file is the project-folder `close-eval.md`, not the `_vision/eval/` path I suggested. That is acceptable, and the CEVO role card grants it (role-cards.yaml:548).
- **3, "recorded" meant any write: implemented.** The check now needs the named file, a valid `gate:` line, and the council as last writer after `--since` (release_check.py:243-253).
- **4, phase gates: resolved by removal.** Item 1 is gone from §8.6. Phase colours are disclosed as unchecked (ADR-0010:100). I accept that.
- **5, other runs' receipts: implemented.** `--project` and `--since` are required, and the script returns 2 without them (release_check.py:299-302; test at test_release_check.py:203-206).
- **6, "or its successor": implemented.** The phrase is removed, and changing the check needs an amendment (ADR-0010:82).
- **7, regression of 5pp or more must be red: partly met.** The text says so (ADR-0010:77). The script cannot enforce it. The CEVO verdict has no regression line, and nothing checks one. A CEVO yellow that hides a regression passes if it lists any open item. This is the one regression rule my council exists to keep, and the ADR's residuals don't mention it.

**Accepted options.** Options 1 to 9 are all implemented in the ADR text and the conforming edits (`skills/gates`, `skills/waivers`, `skills/ceo`, role cards). Two of them are only as strong as the script behind them: option 3 on waivers (findings 1 and 2) and option 5 on yellow and regression (finding 3).

**New findings and defects**

VERDICT: REJECT

1. **Waiver matching is by substring.** `release_check.py:244` uses `fid in text`. A waiver for `sec-7` clears a red whose file merely contains "sec-70", "not sec-7", or any mention of the id. One waived finding also clears the whole red, however many other findings the file lists. The line should match a structured finding id, and every red finding should need its own waiver. Add tests for both cases.
2. **A missing `class:` passes.** `release_check.py:201` only rejects classes that are listed as non-waivable. A waiver with no `class:` is accepted, so the §8.4 non-waivable carve-out is optional for whoever writes the ADR. The check should fail closed and require a class from a known set. Add a test for the missing-class case, since the test at test_release_check.py:150 covers only an explicit `raw-secret`.
3. **The regression rule is not mechanical.** ADR-0010:77 is unenforced, as in objection 7 above. Require a `regression: <max Δpp>` line in `close-eval.md`. The gate should fail if that value is 5 or more and `gate:` is not `red`. Add a test for it. Otherwise ADR-0010:79-81 ("the check is mechanical") overclaims, and the residuals at :97-100 should say so.
4. **`acceptance: pass` is self-declared.** release_check.py:262-265 never compares the verdict with `acceptance.md`. Require one `item <id>: pass|fail` line per `acceptance.md` item. The gate should fail on a missing or extra id, and on any fail with a non-red gate.
5. **Informing reds are read from `status.json`.** This is disclosed (ADR-0010:99). It still means the CEO can record green for an informing red, which was the E4 hole. The ADR should say plainly that the gate does not close E4 for informing councils until they have their own verdict files. It should not describe the hole as closed. That would be the honest residual.
6. **"Last writer" relies on receipts.** If shell or Bash writes to a verdict file aren't receipted, `release_check.py:241-243` can't see them, and a verdict could be edited unseen. Either state that the guard receipts all writes, or list this as a residual.
7. **`acceptance.md` can never be corrected.** The check fails if it was written more than once (release_check.py:272-273). A legitimate fix at intake blocks the release permanently. Say how an intake correction is recorded, for example a superseding ADR, or accept the rigidity in the ADR. The role card for `eval-designer` ("derive at close") should also be reconciled with the intake-time set. The role-cards diff only adds the CEO write scope (role-cards.yaml:283).

Findings 1 to 4 must be fixed before I would approve. Findings 5 to 7 are residual disclosures or small edits.

#### CISO (`security-lead`): REJECT

**Round 2, CISO (§10.3: waivers, go-live, secrets, security posture)**

**Scope and limits.** This is a static read. I read both ADRs, `release_check.py`, the CEO and verdict-file entries in `role-cards.yaml`, and the `guard.py` append-only list. I only grepped `test_release_check.py` for test names and did not run it. I did not read the `skills/gates`, `skills/waivers`, `skills/ceo` or `GOVERNANCE.md` edits, so I make no claim about them.

**My round-1 objections**

*ADR-0009*
- **1, definitions: implemented.** "First public release" is defined at ADR-0009:65-68. "Outside a mandate" is covered by "any action outside its cap" and by the G9 redline at :100-106.
- **2, secrets: implemented.** A mandate holds a vault reference only. The reference is scoped to the named targets and revoked when the mandate ends. A raw secret is a §8.4 non-waivable finding (:56-57).
- **3, silent lapse: implemented** (:60-61). A paired expiry ADR is filed.
- **4, revocation, receipts and failed use: partly implemented.**
  - Append-only receipts are done: the §5.2 redline is at :92-93 and the failed-use suspension at :63-64.
  - The revocation mechanism is still missing (see finding 4).
  - The §5.2 redline and the guard/role-card edits take effect only after approval (:121, :126). That is acceptable if the Chairman is told. As the text stands, the §5.2 line names a path the guard does not yet enforce.
- **5, class creep: implemented.** "Only these classes can be granted" (:44-46), and :33 excludes M5 and M6.
- **6, CISO precondition: implemented in text.** SBOM, SLSA and a non-red CISO verdict are required before each use (:58-59). Nothing checks them mechanically.

*ADR-0010*
- **1, non-waivable reds: implemented in text** (§8.6.2, ADR-0010:70-71). The script only partly enforces it (finding 1).
- **2, forged verdicts: implemented.** Named verdict files (`release_check.py:66-67`), a last-writer check (`:243`) and a `status.json` mismatch check (`:255`).
- **3, fail-open: implemented.** A missing or corrupt `status.json` is flagged (`:214-215`), `--project` and `--since` are required (`:300`), and the exit code is 1 (`:312`).
- **4, mandate/gate interaction: implemented** (ADR-0010:59-60; ADR-0009:70-71).
- **GC question: decided** as informing (ADR-0010:129).

**Accepted options.** The redline implements all of them except the points under findings 2, 3 and 5. The script implements Decisions 1 to 3 and Decision 5's yellow rule, subject to the problems below.

**Findings**

VERDICT: REJECT

1. **One waiver can cover a whole red verdict, and the non-waivable carve-out is not enforced** (`release_check.py:244, 257`). A red verdict passes if any one waived finding id appears as a substring anywhere in the verdict file. The check does not look for other unwaived findings in the same file. A short id such as `1` or `F1` also matches inside `F10`. A verdict that names an ASI-class or raw-secret finding alongside one waivable finding therefore passes. That contradicts §8.6.2's "never waived here" and "for that … finding" (ADR-0010:68-71). Fix: give findings structured ids in the verdict file, such as a `findings:` list with a class. Require every red finding to have its own matching waiver. Fail on any non-waivable class in the verdict, whatever the waiver's front matter says.

2. **An informing red is covered by any waiver for that council** (`release_check.py:267`). The check is `not waived.get(council)`, so any live waiver for the council clears any informing red. ADR-0010:99 admits the matching is "council and project only". But Decision 3 in the table at :124 says "for that council, project and finding", and the text is not qualified for informing councils. State the weaker rule in §8.6.2 or in the decision table, or tighten the check.

3. **The check takes its own trust inputs from the command line** (`release_check.py:299, 303`). `--today` lets the caller back-date the clock, which revives expired waivers. `--since` set to an early date makes old writes count as "this run". §8.6 says the check is mechanical. Fix: drop `--today` outside tests, and derive `--since` from the project record, such as the intake or `acceptance.md` timestamp. Alternatively, state in §8.6 who supplies `--since` and that it must not predate `acceptance.md`.

4. **The `inbox.json` approval timestamp is forgeable, and ADR-0009 does not say so** (ADR-0009:48-51, :153). Mandate provenance rests on an `inbox.json` entry. `inbox.json` is a shared log that every agent may write (`guard.py:87`, `LOGS` at `release_check.py:64`), and the CEO can write the mandate ADR (`role-cards.yaml:279-285`). ADR-0010 carries a residual note on this (:97-98), but ADR-0009 has none. Add the same residual: until signed receipts exist, a mandate grant cannot be proved to be the User's. Also state the revocation mechanism. Revocation has no recorded form and no closing ADR (:62), and the paired expiry ADR covers only expiry (:60-61).

5. **ADR-0010 says more than the script checks** (ADR-0010:79-81; :72-77; :28).
   - §8.6 says "The check is mechanical … computes it". But clause 3 (the release record carries the yellow open items) is not checked. The script checks only that a list exists (`:259`).
   - Clause 5 (a regression of 5 points or more is always red) is not checked at all. A CEVO yellow with a 7-point regression passes.
   - Option (b) at :28 still promises "each phase gate green by its own verifier". §8.6 dropped that and the script skips it (:100).
   - Fix: either soften §8.6 to say which clauses the script enforces and which are for CAO to audit, or add the checks. Remove or correct the sentence at :28.

6. **The "last writer" evidence covers only the file-write tools** (`release_check.py:63, 223`). Writes by shell or other tools leave no receipt, and `guard.py:44` already says an agent with a shell can edit the receipts. §8.6.1's "was the last to write it" is only as strong as that guarantee. State the limit in ADR-0010's residuals. CEO has `shell: null` and no verdict file in its write scope, which is good (`role-cards.yaml:277-283`).

7. **ADR-0009: M4 patch updates can include a push or publish, which is unbounded in the text** (ADR-0009:44-46). The mandate covers "a §2.2 clause 7 action", and clause 7 includes a GitHub push and a third-party broadcast. Round-1 CRT raised pushes to protected branches. Say that M4 covers deploying a verified patch to the named target. Say that a push or merge to a protected branch, or a publish to a package registry, is outside any mandate.

8. **Minor.** `--since` is a string comparison (`release_check.py:243`), so a `Z` suffix and a `+00:00` suffix compare wrongly. Normalise the timestamps before comparing. A relative `path` in a receipt resolves against the script's working directory, not the launch folder (`:222-224`). That fails closed, but it is a spurious failure.

I'd approve once findings 1, 3, 4 and 5 are fixed. Findings 2, 6 and 7 can be fixed in the same pass.

#### Response to round 2: the script (fixed in this branch)

| Finding | Response |
|---|---|
| One waiver clears a whole red, and the match is a substring (CRT 1, CAO 1, CEVO 1, CISO 1) | A red verdict lists `finding: <id> class: <class>` lines. Every finding needs its own waiver, matched by exact id. A red with no findings listed fails. |
| A missing `class:` passes, and `ASI-03` passes (CRT 2, CAO 3, CEVO 2) | Fails closed. An empty class, any `asi…` class and any class naming a secret are never waivable, in the waiver and in the verdict. The council's own verdict sets the finding's class, so the CEO's `class:` cannot downgrade it. |
| `--today` back-dates the clock; an early `--since` counts old writes (CRT 4, CISO 3) | `--today` is removed from the command line. "This run" starts at the later of `--since` and the CEO's write of `acceptance.md`. |
| The regression rule is not mechanical (CEVO 3, CAO, CISO 5) | `close-eval.md` carries `regression: <max points>`. A missing line fails, and 5 or more must be red. |
| `acceptance: pass` is self-declared (CEVO 4) | `close-eval.md` carries one `item <id>: pass\|fail` line per `acceptance.md` item. Missing or extra ids fail, and a failed item must be red. |
| `- none` counts as an open item (CRT 7) | Empty bullets (`none`, `n/a`, `nothing`, `-`) do not count. |
| The first `gate:` line anywhere is read (CRT 9) | Only a `gate:` line before the first heading counts. |
| Z and +00:00 compare wrongly; relative receipt paths (CISO 8) | Times are normalised to UTC before comparing. Relative paths resolve against the launch folder. |

Tests: 35 in `scripts/test_release_check.py`, including a two-finding red, short and substring ids, eight invalid-waiver cases and a non-waivable finding.

#### Response to round 2: the text (changed in this ADR)

- **Options (b)** now matches the redline (CAO 7, CISO 5).
- **§8.6** states what the script checks and what CAO audits by reading: whether the release record carries the open items (CRT 7, CISO 5).
- **Residuals** now name the shell limit (CRT 4, CEVO 6, CISO 6). They also say that the gate does not close E4 for informing councils (CEVO 5).
- **The skill edits** (CAO 5) are on this draft branch only. The branch merges with the amendment, after the Chairman approves the final text, so nothing takes effect early. `GOVERNANCE.md` is edited in that same PR.
- **The eval-designer card** says to derive the set "at close" (CEVO 7). Its conforming edit, deriving the set from `acceptance.md`, lands with the amendment.
- **Citations** (CAO 5): the G1/G2 evidence is `docs/vision/RUN-1-REPORT.md`, and N4 is `docs/vision/CEO-ENTRY-REVIEW.md`, "Run N4".

#### Round-2 questions for the Chairman

Each has a recommended option. None is decided here.

1. **What is a release, and does a rollback need a fresh gate?** (CRT 8, CAO 2 and 8.) *Recommended:* a release is any deploy of a build to a target outside the agency's own machine. A rollback (M3) to a build that already passed §8.6 reuses that build's gate record, and appends a receipt that names it.
2. **Who runs `--gate`?** (CRT 4, CAO 6.) *Recommended:* CAO's `gate-auditor`, which writes the result into `close-audit.md`, and CI where the repository has it. The CEO never runs it for its own release.
3. **Can `acceptance.md` be corrected?** (CEVO 7.) *Recommended:* only by the Chairman. A correction is a new `acceptance.md` filed with a `user-decision` ADR before any verdict, and the gate's "written once" rule counts from that ADR.
4. **Informing councils.** (CRT 3, CEVO 5, CISO 2.) *Recommended:* say plainly that the gate does not close E4 for informing councils, because their reds are read from `status.json`. Give CQO and GC their own verdict files in a later amendment.

#### Dry check against a real run (after round 2, $0)

`--gate` was run against the records of run N4 (tip calculator). It failed with six flags: no `acceptance.md`, and no verdict file for any of the four blocking councils. The councils had written their verdicts elsewhere: CEVO `eval/close-eval.md`, CRT `red-team/pre-release.md`, CISO `security/code-audit.md`, and CAO under `_vision/audit/`. `status.json` kept its gates flat, with no `byCouncil` key. So no real run can pass the gate until the four chiefs' prompts and the status schema follow the contract now stated in `skills/gates`. Those edits are listed above.
