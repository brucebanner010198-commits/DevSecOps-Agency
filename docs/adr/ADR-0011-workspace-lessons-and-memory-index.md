---
adr: 0011
title: The lessons ledger is a workspace record, and the memory index may be rewritten
status: accepted
date: 2026-11-25
deciders: user (Chairman)
kind: constitution-amend
related: docs/vision/CEO-ENTRY-REVIEW.md (F3, N1-e, Chairman's defaults 1 and 3), CONSTITUTION §5.2, §10
---

# ADR-0011: Workspace lessons ledger and memory index

## Status

**Accepted.** The Chairman's approval came first, and the §10.3 reviews came after it. CAO and CRT both approved in round 2, below, so the status is `accepted`.

**Approval (§10.4), 2026-11-25, in the chat interface.** The session that recorded it had no clock tool, so only the date is recorded, not the time. The two defaults were put to the Chairman as written below, in a list of seven:

> 1. **Lessons ledger.** Root `AGENTS.md` puts it in the plugin's own folder. Claude Code's docs say a plugin gets a new folder on every update and not to store data there. Default: keep it at `outputs/devsecops-agency/LESSONS.md` in each workspace. That needs a root-document amendment.
>
> 3. **Memory index (`index.json`).** The skill rewrites it as a structure, but the Constitution makes all of memory append-only. Default: an amendment that exempts it, as the vision document already is.

The Chairman's reply: "Accept all defaults".

## Context

**1. The lessons ledger has no writable home.**
- `AGENTS.md` points every close at the root `LESSONS.md`, and the CEO reads the plugin-root copy at session start.
- Writing it is refused. The guard keeps every write inside the launch folder (B1), and the plugin root is outside it.
- In run N1 the CEO read the plugin-root ledger but wrote a new `LESSONS.md` at the launch root (finding N1-e).
- Claude Code installs each plugin version in its own folder, and its documentation says not to keep state there. So a ledger in the plugin folder would not survive an update even if the guard allowed the write.

**2. The memory index cannot be append-only.**
- §5.2 makes `_memory/**` append-only.
- The `memory` skill rewrites `_memory/index.json` as a structure: cross-references and the `lastRem` marker.
- Only its `knobHistory[]` is written as an append (`skills/memory/references/novelty.md`).

## Decision

1. **Ledger location.** Each workspace keeps its ledger at `outputs/devsecops-agency/LESSONS.md`.
   - The plugin-root `LESSONS.md` stays as the schema and the seed. Agents read it and never write it.
   - A ledger read takes the plugin-root rows, then the workspace rows.
   - A missing workspace ledger is not an `identity-missing` abort while the workspace has no closed project. "No closed project" means no retro minutes exist at `outputs/devsecops-agency/_meetings/*-retro-*.md`; §5.8 writes them at every close. Once one exists, a missing workspace ledger is an abort, so a deleted ledger is caught.
   - The duplicate-slug check (`lessons-ledger`) and the carry-over check (`retrospective`) read both ledgers.
   - The ledger is still append-only (§5.2, guard B2).
2. **Memory index.** `_memory/index.json` is exempt from §5.2 and may be rewritten as a structure. Its `knobHistory[]` entries stay append-only. The guard enforces that limit: a rewrite is refused unless the old `knobHistory` is still, unchanged, at the start of the new one, and the new file is valid JSON (B2 "knob history", `hooks/guard.py`, with tests).

## Redline (§10.2)

```diff
@@ §5.2 Append-only (VALUES §4)
-- `_memory/**`
+- `_memory/**`, except `_memory/index.json`, which the `memory` skill rewrites as a structure; its `knobHistory[]` entries are append-only
```

```diff
@@ AGENTS.md, Identity + Learning (v0.3.8)
-- **[`LESSONS.md`](LESSONS.md)** — one append-only row per project close. Written via `skills/lessons-ledger/SKILL.md` after `skills/retrospective/SKILL.md` lands the retro minutes.
-- **Session-start invariant:** CEO reads `MISSION.md` + `VALUES.md` + latest 5 rows of `LESSONS.md` before deriving a project slug. Missing any = abort + file ADR `kind: identity-missing`.
+- **[`LESSONS.md`](LESSONS.md)** — one append-only row per project close. Written via `skills/lessons-ledger/SKILL.md` after `skills/retrospective/SKILL.md` lands the retro minutes. The rows are written to the workspace ledger, `outputs/devsecops-agency/LESSONS.md`. The plugin-root file is the schema and seed: read it, never write it. A ledger read takes the plugin-root rows, then the workspace rows (ADR-0011).
+- **Session-start invariant:** CEO reads `MISSION.md` + `VALUES.md` + latest 5 rows of `LESSONS.md` before deriving a project slug. Missing any of the three plugin-root files = abort + file ADR `kind: identity-missing`. A missing workspace ledger is not an abort while the workspace has no closed project, meaning no retro minutes `outputs/devsecops-agency/_meetings/*-retro-*.md` (§5.8 writes them at every close). Once one exists, a missing workspace ledger is an `identity-missing` abort too.
```

The skills that name the write follow the same rule: `ceo` (session start step 2, close step 5), `lessons-ledger` (output, write and duplicate-slug steps, and `references/append-contract.md`) and `rca`. `retrospective` reads both ledgers for its carry-over check. `rhythm` only reads "the quarter's rows" and takes the read rule from `AGENTS.md`.

## Effect on other root documents (§10.2)

- `MISSION.md` and `VALUES.md`: "every close appends ≥ 1 row to `LESSONS.md`" still holds; the row now lands in the workspace ledger. No text change.
- `GOVERNANCE.md`: the "Update `LESSONS.md` (append row)" matrix row is unchanged.
- `RESILIENCE.md`: no effect.
- The plugin-root `LESSONS.md` is not edited. It is append-only, and its header still describes the schema correctly.

## Rollback

Revert this ADR's merge commit. Workspace ledgers already written stay where they are, because they are append-only records; a later ADR would say whether to fold them back.

## Review roll (§10.3)

The reviews are pasted below unedited. Round 1 ran read-only (no writes, no dispatch, no shell) on each agent's own tier, from the diffs alone, because the proposed files were not in the review folder. Round 2 had the full files.

### Round 1, CRT (`red-team-lead`): REJECT

I couldn't open any of the plugin-root files. `${CLAUDE_PLUGIN_ROOT}` is not set in this environment, and a glob of the working folder found no `guard.py`, `ceo.md`, ADR-0011 or `CONSTITUTION.md`. Everything below comes from the four diffs alone. `adversarial-prompter` was not run, because I can't dispatch it.

## VERDICT A: REJECT (diffs 1–3)

1. **Guard-refusal skip clause** (`1-pr15-ceo.diff:16`, kept at `2-pr18-ceo.diff:12`). On a guard refusal the CEO must "skip that step… and continue". The clause has no carve-out for steps that carry a gate. Those include an ADR filing, the lessons row ("no row = the agency did not learn") and receipts. A guard block becomes a logged skip, so the guard no longer stops the run. The CEO should halt or escalate on a gate-bearing step.
2. **Skip-and-default clause** (`1-pr15-ceo.diff:17`). A step that needs a tool the CEO lacks is skipped, and "Where a skill says to ask the Chairman, use what the Chairman's message already says", then default into `brief.md`. This can stand in for the Chairman's consent on USER-ONLY actions (CONSTITUTION §2.2): amendments, waivers and the adopt-report approval. It needs an explicit exclusion.
3. **Intake step removed** (`1-pr15-ceo.diff:9`). "Run the intake conversation… until you have a one-paragraph product brief that survives contact with reality" became "run the `ceo` skill". Whether `skills/ceo` keeps that gate is unverified.
4. **Guard `lines kept`** (`3-pr19-prompt-and-guard.diff:35,65-72`).
   - If `_memory/**` was already in `APPEND_ONLY`, the new `elif` is never reached. Either the change does nothing, or it relaxes the existing prefix rule. I couldn't read the list, so this is unresolved.
   - Any line can now be inserted anywhere in memory files. That is a poisoning surface, and it needs the red-team's attention.
   - A non-UTF-8 current file skips the check (`current=None`). The existing append-only branch has the same gap.
5. **Adopt session-log path** (`3-pr19-prompt-and-guard.diff:10`). `_agency/_sessions/ceo/…` must still match the append-only and `SHARED_WRITES` patterns. I couldn't confirm that.
6. **Process.** Diffs 1 and 2 merged with no §5.3 review.

Not weakening: the `ts: null` rule (`3-pr19-prompt-and-guard.diff:97`), where the guard's receipt timestamp is authoritative.

## VERDICT B: REJECT (ADR-0011)

1. **`index.json` exemption is prose-only** (`4-adr-0011-amendment.diff:55`). The whole file is exempted, and `knobHistory[]` stays append-only only by a sentence. Nothing in the diff changes the guard to enforce that. `LINES_KEPT` covers only `MEMORY.md` and `memory/*` (`3-pr19…:35`). A structure rewrite can silently alter the knob audit trail, or drop the cross-references to patterns and lessons. The fix is a JSON-aware guard check that `knobHistory` keeps its prefix. The guard's handling of `index.json` also contradicts the amended §5.2 until it is changed.
2. **Missing-ledger abort removed** (`4-adr-0011-amendment.diff:108,153`). A missing workspace ledger is now never an `identity-missing` abort. A first run can't be told apart from a deleted or truncated ledger, so the loss of lessons goes undetected. The exemption should apply only when no prior close exists.
3. **Duplicate-slug and carry-over checks.** `lessons-ledger` step 4 rejects a slug that already has a row, and the retro runs a Jaccard check on the last 3 rows. Neither is updated to read both ledgers (`4-adr-0011-amendment.diff:190-192`).
4. **§10.3 review roll is empty** (`4-adr-0011-amendment.diff:143`). It says the reviews are "pasted below unedited", but nothing follows. The CHANGELOG says they are "recorded in the ADR" (`:63`), and the ADR is marked `accepted`. The amendment fails its own §10.3 gate.
5. **Consent is thin.** The Chairman said "Accept all defaults" in chat (`:88`). It is unclear whether that meets the explicit approval a §5.2 amendment needs under §2.2.

Strengthening: the plugin-root ledger becomes read-only, and the ledger stays append-only.

### Round 1, CAO (`cao`): REJECT

**Verdict: REJECT.** The §10.3 review roll is missing, so the amendment is incomplete under §10.2.

**Blocking**
1. **The review roll is empty.** `docs/adr/ADR-0011…md` (diff 4, lines 141–143) has the heading "Review roll (§10.3)" and the line "The reviews are pasted below unedited." Nothing follows, and the new file ends at line 143. No CAO or CRT review is recorded.
2. **The CONSTITUTION says otherwise.** The new amendment record (diff 4, line 63) states "The CAO and CRT reviews are recorded in the ADR." That is false. A root document would then cite a review that doesn't exist.
3. **The status is premature.** The ADR is marked `status: accepted` (diff 4, line 77) and ships in a release (`plugin.json` 0.7.1, CHANGELOG line 36 "Chairman-approved") before the §10.3 review. The ADR carries only the Chairman's approval. The CAO review is the independent check, and it cannot be assumed.

**§10.2 completeness**
- **Clause:** present (Decision, lines 103–110).
- **Redline:** present (lines 112–126).
- **Rationale:** present (Context, lines 90–101).
- **Effect on root documents:** present (lines 130–135).
- **Rollback:** present (lines 137–139).
- **Review roll:** **missing**.

**Redline against the files**
- The §5.2 redline matches the CONSTITUTION diff (line 55).
- The two AGENTS.md lines match (diff 4, lines 23–24).
- The skills `ceo`, `lessons-ledger` and `rca` are described in prose only, but their diffs are consistent with that description.
- The proposed files at `${CLAUDE_PLUGIN_ROOT}` could not be read, because the variable doesn't resolve here. This check rests on the diff alone.

**Independence**
- No auditor's independence is lost. Auditors stay read-only, and the CAO's scope is unchanged.
- The §5.2 exemption does narrow what `memory-auditor` can check. It audits `_memory/**` for append-only violations, and `index.json` rewrites are now legitimate. The ADR doesn't say how it detects tampering with `knobHistory[]` entries. It also doesn't update `memory-auditor`'s checks.
- The ADR names guard B2 as enforcing append-only (line 109) but doesn't say whether `hooks/guard.py` exempts `index.json`. If B2 still blocks the rewrite, the exemption does nothing. If B2 doesn't, the exemption goes unenforced.
- `lessons-ledger/references/append-contract.md` still has the duplicate-slug check ("Reject if slug already has a ledger row", `SKILL.md` line 191). Its scope isn't stated for the plugin-root and workspace ledgers.

**To reach APPROVE**
- Run the CAO and CRT reviews and paste them into the roll.
- Set the ADR status to `proposed` until the roll is complete.
- Fix the line 63 wording.
- State how `knobHistory[]` is audited and what the guard does for `index.json`.
- Say which ledger the duplicate-slug check reads.

**ADR filing:** this finding should produce an ADR for an amendment that shipped without its §10.3 review. The same gap applies to diffs 1–3, which merged or are pending without a prompt-diff review.

### Response to round 1

| Objection | Response |
|---|---|
| Review roll empty; status `accepted`; CHANGELOG says the reviews are recorded (CAO 1–3, CRT B4) | The roll now holds the reviews. The status is `proposed` until both approve. The Schedule B and CHANGELOG lines are worded to be true at merge. |
| Consent is thin (CRT B5) | The approval is quoted above, with the defaults exactly as they were put to the Chairman. |
| `knobHistory` is prose-only; the guard does not say what it does (CRT B1, CAO) | The guard now enforces it: B2 "knob history", with tests for a rewrite, an append, a dropped history, an edited entry, a removed key and invalid JSON. |
| A deleted ledger looks like a first run (CRT B2) | Narrowed. The exemption holds only while no retro minutes exist. |
| Duplicate-slug and carry-over checks read one ledger (CRT B3, CAO) | Both now read both ledgers. |
| `memory-auditor` coverage (CAO) | `agents/audit/memory-auditor.md:30` never listed `index.json`, so its audit is unchanged. The guard now checks `knobHistory`. |
| Diffs 1–3: the skip rules have no carve-out (CRT A1, A2) | Fixed in PR #19. Mandatory steps (§3.3 gate verdict, §5.8 lessons row, the ADR for a material decision) are never skipped; the CEO stops, files it in `inbox.json` and reports blocked. A recorded default never stands in for a USER-ONLY action (§2.2). Probe S2 ($0.18) confirmed all three cases. |
| Intake removed (CRT A3) | Not removed. `skills/ceo/SKILL.md` keeps it as playbook section 2, "Intake" (line 148), writing `brief.md > ## Intake`. |
| "Lines kept" may relax an existing rule (CRT A4) | `APPEND_ONLY` never held `MEMORY.md` or `memory/*` (`hooks/guard.py` at `1c5ac82`, line 69 has only `_memory/patterns/*`). Before PR #19, a full rewrite of either passed, so the mode tightens. An undecodable current file is now refused in both B2 branches. |
| Adoption session-log path unconfirmed (CRT A5) | `test_adoption_session_log_is_allowed_and_append_only` in `hooks/test_guard.py`. |
| Diffs 1 and 2 merged without a §5.3 review (CRT A6, CAO) | True. This round is that review, after the fact. |

### Round 2, CRT (`red-team-lead`): APPROVE (verdict A, prompt-diff; verdict B, this amendment)

**VERDICT A (CONSTITUTION §5.3, `agents/ceo.md` since PR #15 and PR #19): APPROVE**

I did not run `adversarial-prompter`, because I can't dispatch it. `skills/red-team/references/prompt-diff-review.md` isn't in the review folder, so I used §5.3 and my own checklist. This review is also after the merge.

- **The skip rules no longer weaken a gate.** `ceo.md:33-34` still say to skip a refused step or a missing tool. `ceo.md:35` now carves out the §3.3 gate verdict, the §5.8 lessons row and the ADR for a material decision. For those the CEO stops, files it in `inbox.json` and reports blocked. `ceo.md:36` stops a recorded default from standing in for a USER-ONLY action (§2.2). This closes my round-1 objections A1 and A2.
- **Intake is kept** (A3). The `ceo` skill holds it, which I take from the ADR's cited "playbook section 2, line 148". I did not open `skills/ceo/SKILL.md`.
- **The new `lines kept` rule tightens the guard.** `APPEND_ONLY` (`guard.py:64-77`) has only `_memory/patterns/*`. So `MEMORY.md` and `memory/*` were unguarded before. Now `guard.py:264-273` refuses a changed, removed or reordered line, and also a file that isn't UTF-8. My A4 concern is resolved. Inserting lines anywhere is still a poisoning surface, but it is narrower than before. `keeps_lines` (`guard.py:117-123`) is a correct ordered-subsequence check.
- **The adopt session-log path is covered** (A5). `_agency/_sessions/*` matches `_sessions/*` (`guard.py:67, 80`), and `test_adoption_session_log_is_allowed_and_append_only` tests it.
- **No Never or append-only rule is removed.** Residual, non-blocking: the carve-out names only three step classes. Other mandatory steps, such as a §5.3 review, still fall under "skip and continue".

**VERDICT B (CONSTITUTION §10.3, ADR-0011): APPROVE**

The amendment weakens no gate:
- `LESSONS.md` stays append-only (§5.2 line 223; `guard.py:66` also matches `*/LESSONS.md`).
- The §5.8 duty is met by the workspace ledger.
- `index.json` goes from unguarded to guarded (`guard.py:274-282`).

My round-1 objections:
- **B1, `knobHistory` prose-only: resolved.** The guard now checks it (`guard.py:132-147`), and there are tests. One residual: a current file that isn't JSON sets `before=[]` (`guard.py:136-145`), so corruption could reset the history. This is low severity.
- **B2, deleted ledger looks like a first run: resolved.** The exemption lasts only while no retro minutes exist. Side effect: if the ledger write is refused after the retro is written, every later session aborts. That fails closed, so it isn't a weakening.
- **B3, duplicate-slug and carry-over checks: resolved.** Both read both ledgers (`lessons-ledger` step 4, `carry-over-check.md`).
- **B4, empty review roll: resolved.** The roll holds round 1, and the status is `proposed` (ADR line 4). My verdict will make it complete.
- **B5, consent: mostly resolved.** The defaults are quoted verbatim. §10.4 wants an approval timestamp, and the ADR records only a date. That is a paperwork gap to fix.

On the CAO's `memory-auditor` objection: `memory-auditor.md:30` never listed `index.json`, so the response holds.

### Round 2, CAO (`cao`): APPROVE

**Verdict: APPROVE.** This is the CAO's §10.3 integrity and independence review of ADR-0011. I'm approving after reading the files in B-after against the ADR.

**§10.2 completeness.** All six elements are present in `ADR-0011…md`:
- Clause: Decision, lines 38–46.
- Redline: lines 48–62.
- Rationale: Context, lines 25–36.
- Effect on other root documents: lines 66–71.
- Rollback: lines 73–75.
- Review roll: lines 77–161. It now holds both round-1 reviews and a response table.

The status at line 4 is `proposed`, and line 15 makes `accepted` conditional on both approvals. That fixes my round-1 objection that the status was premature. The CHANGELOG (`B-after/CHANGELOG.md:7`) and the Constitution amendment record (`CONSTITUTION.md:610`) both say the verdicts are "in the ADR". That is true once these verdicts are appended.

**Redline against the files.** It matches:
- The §5.2 line in the ADR (line 53) equals `CONSTITUTION.md:215`.
- The two AGENTS.md lines (ADR lines 60–61) equal `AGENTS.md:20–21`.
- The skill edits match the ADR's list: `skills/ceo/SKILL.md:78,131,217`, `skills/lessons-ledger/SKILL.md:37,44,45`, `skills/rca/SKILL.md:168`, `skills/retrospective/SKILL.md:73`, `skills/retrospective/references/carry-over-check.md:12` and `skills/lessons-ledger/references/append-contract.md:13`.

**Independence.** No auditor loses it.
- Auditors are still read-only, and the CAO's scope is unchanged.
- `agents/audit/memory-auditor.md:30` lists only `MEMORY.md`, `memory/<date>.md`, `patterns/*` and `_sessions`. It never covered `index.json`, so the exemption removes nothing from its audit.

**My round-1 objections.**
1. Empty review roll: resolved (lines 77–161).
2. False statement in the Constitution record: resolved. It is true once the verdicts are appended.
3. Premature `accepted` status: resolved (lines 4 and 15).
4. How `knobHistory` is audited and what the guard does with `index.json`: resolved.
   - `hooks/guard.py:274–282` enforces a prefix-kept check, and `keeps_knob_history` is at `guard.py:132`.
   - `APPEND_ONLY` (`guard.py:75`) holds only `_memory/patterns/*`, so there is no conflict with the §5.2 amendment.
   - The tests are at `test_guard.py:428` onward.
5. Which ledger the duplicate-slug check reads: resolved. It reads both (`append-contract.md:13`, `lessons-ledger/SKILL.md:44`).

**Non-blocking residuals, none of which are reds:**
- `retrospective/SKILL.md:38,65`, `ceo/SKILL.md:76` and `append-contract.md:83` still say plain "LESSONS.md" or "in full". `AGENTS.md:20` governs and resolves them, but a taskflow tidy is warranted.
- After the fact, nothing audits `index.json`. Only the guard enforces `knobHistory` before the write. I suggest `memory-auditor` adds `index.json` to its scope.
- The "no closed project" test depends on retro minutes existing. That is acceptable, because `_meetings` is a record directory.

### Residuals carried forward (non-blocking)

- A current `index.json` that is not JSON is treated as having no `knobHistory`, so a corrupted file could reset it.
- The CEO's carve-out names three step classes; other mandatory steps, such as a §5.3 review, still fall under "skip and continue".
- `memory-auditor` does not audit `index.json` after the fact; only the guard checks it before the write.
- A few skill lines still say plain "`LESSONS.md`" (`retrospective/SKILL.md:38,65`, `ceo/SKILL.md:76`, `append-contract.md:83`); `AGENTS.md:20` governs them.
- `adversarial-prompter` (prompt-diff step 5) was not run, because the reviews were read-only with no dispatch.
