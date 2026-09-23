---
adr: 0005
title: Chairman → Board of Directors → CEO re-architecture
status: accepted
date: 2026-07-07
deciders: user, ceo
kind: constitution-amend
shipped-with-plugin: 0.7.0
---

# ADR-0005: Chairman → Board of Directors → CEO re-architecture

## Context

The repo previously put the human directly above an AI CEO, and named the human role inconsistently ("Sovereign" / "Owner" / "Sir" across `CONTEXT.md`, `CONSTITUTION.md`, `MISSION.md`, `VISION.md`, `KEEPER-TEST.md`, and several skills). `VISION.md:19-20` and `MISSION.md:14` already *described* an `Owner → Board → CEO` chain, but no Board tier existed in `agents/`, `councils/`, or `CONSTITUTION.md` — the description was aspirational, not implemented. `skills/board-meeting` was also mis-named: its content was the CEO+Chiefs phase-transition orchestration, a real-world **executive session**, not a Board of Directors meeting.

**Numbering note:** the approved plan referenced this record as "ADR-0004", but `docs/adr/ADR-0004-foundation-architecture.md` (OS Foundation Architecture, status: proposed, 2026-06-07) already claims that number. Per `docs/adr/README.md`, ADR numbers are append-only and never reused — this record is filed as **ADR-0005** instead.

This session, the User directed a full re-architecture around the real-world corporate structure:

```
Chairman of the Board  (the User / human — sovereign)
        │  chairs
Board of Directors      (AI governance body — the ONLY group meeting the User joins)
        │  oversees / hires / sets & approves strategy
CEO                     (top AI executive — runs the company day-to-day)
        │  runs
C-suite = 16 Chiefs → specialists → workers   (unchanged)
```

**This planning session IS the `user-meeting` approval** for this constitution-amend. No separate approval round was opened; the User directed the change directly in this session's plan approval. This ADR records that fact per the plan's paper-trail contract.

## Decision

1. **Human role renamed.** Canonical role name is now **"Chairman of the Board"** (short forms "Chairman" / "the Chairman"), replacing the scattered "Sovereign" / "Owner" / "Sir" role-names throughout `CONTEXT.md`, `CONSTITUTION.md` (Article II retitle), `MISSION.md`, `VISION.md`, `GOVERNANCE.md`, `README.md`, `KEEPER-TEST.md`, and skills (`caveman`, `grill-with-docs`, `improve-codebase-architecture`, `tdd`, `ladder/references/rung-rules.md`, `runtime-hooks/git-guardrails/`, `skills/adr/references/adr-template.md`, `skills/meeting-minutes/references/meeting-kinds.md`, `skills/retrospective/references/cadence.md`, `skills/ui-ux-pro-max/SKILL.md`, `skills/vision-doc/references/*`).
   - **"Sovereign" is retained as a concept** (the human holds ultimate authority), never as a role-name. `CONSTITUTION.md` Article II §2.1 keeps the sentence "The Chairman is sovereign."
   - **Kept as-is (product/legal concept, not the Agency role):** `os/broker/*`, `os/desktop/*`, `os/trust-spine/*` golden-share "Owner" signing concept — this is the OS product's signing role, distinct from the Agency's human role. `THREAT-MODEL.md`, `SWOT.md`, `SYSTEM-CARD.md`, `DISASTER-RECOVERY.md`, `RHYTHM.md`, and most skill `Authority:`/`Owner:` frontmatter lines use "Owner" as a generic *responsible-party* field (e.g. "Owner: CAO"), not the human role — left untouched.
   - **Panel disambiguation:** the cross-model-panel Stage-3 synthesizer stays named "Chairman" internally but is now always written as **"panel Chairman"** / **"Panel Chair"** in the same breath as the human's **"Chairman of the Board"** full title. `CONTEXT.md` carries an explicit disambiguation note under the Panel entry.

2. **Board of Directors tier created.** New governance tier between the Chairman and the CEO:
   - `agents/board/board-director.md` — single governance persona representing the Board (`model: opus`, Role Card v1, `Reports to: Chairman of the Board`).
   - `councils/board/AGENTS.md` — must/must-not/gate-heuristic contract.
   - `councils/board/TEAM.md` — roster: lead `board-director`; standing committees = the four existing blocking Chiefs (CAO = Audit Committee, CISO+CRT = Risk & Security Committee, CEVO = Evaluation Committee) attending in a governance capacity. **No new specialist agents were created** — this reuses the existing independent-council structure per Constitution §3.3.
   - `CONSTITUTION.md` Article III gains **§3.1a — The Board of Directors**, defining the Board's four duties (chaired by Chairman; sets/approves strategy with reciprocal CEO-proposes/Board-reviews/Chairman-votes; oversees the CEO by reading existing receipts; hosts the four blocking committees). The Board sits above the CEO in governance, parallel to the existing three-tier delivery depth cap (§3.1) — it does not add a fourth delivery tier.
   - `agents/AGENTS.md` color-mapping table gains a `Board` row (`emerald`, `board-director`).

3. **`skills/board-meeting` renamed to `skills/exec-meeting`.** The CEO+Chiefs phase-transition orchestration content moved intact to `skills/exec-meeting/SKILL.md`; every internal self-reference ("board meeting" → "executive session"), `chat.jsonl` vocabulary (`scope:"board"` → `scope:"exec"`, `type:"board-decision"` → `type:"exec-decision"`), and cross-references in `AGENTS.md`, `README.md`, `skills/AGENTS.md`, `skills/ceo/SKILL.md`, `skills/command-center/SKILL.md` + references, `skills/meeting-minutes/SKILL.md`, `skills/session-log/SKILL.md`, `skills/messaging-formatting/SKILL.md`, `skills/skill-creator/references/skill-template.md`, `skills/taskflow/SKILL.md` + references, `skills/gates/SKILL.md` + references, `skills/okr/SKILL.md` + references, `skills/worktree/SKILL.md` + references, `skills/adr/references/decision-triggers.md`, `skills/roster/SKILL.md`, `skills/model-tiering/SKILL.md`, `skills/vision-doc/SKILL.md`, `skills/audit/references/scope-boundary.md`, `command-center/index.html`, `command-center/references/artifact-template.html`, `command-center/references/panel-spec.md`, `agents/evaluation/token-compactor.md`, and `runtime-hooks/commit-gate.sh` were updated to match. `agents/ceo.md` Role Card `Reports to:` changed to `Board of Directors (chaired by the Chairman)`; its stale `9 Chiefs` description was fixed to `16 Chiefs`.

4. **A new `skills/board-meeting`** was authored for the genuine Board of Directors convening — the Chairman's group meeting. Modeled on `skills/user-meeting`'s 4-phase flow (Present → Review → Decide → Commit) but for a group: Chairman (chair) + `board-director` + CEO + the four committee Chiefs. Files ADRs (`kind: board-decision`) on divergence between the Chairman's vote and committee recommendations. `skills/meeting-minutes` gained a `board` kind (redefined — previously meant CEO+Chiefs; now means Chairman+Board+CEO) and an `exec` kind (the split-off CEO+Chiefs meaning).

5. **Two-channel model stated explicitly.** `CONSTITUTION.md` §2.4 rewritten as "The two-channel rule": direct CEO call (1:1 execution) vs. Board of Directors meeting (group, Chairman chairs, CEO proposes / Board reviews / Chairman votes). Mirrored in `MISSION.md` (`## The Chairman's two channels`, `## Chairman experience contract`), `agents/ceo.md` (`## Meeting model`), `skills/ceo/SKILL.md`, and `skills/user-meeting/SKILL.md` (retitled internal language to "Chairman"; kept the skill's filename; added a note that group decisions use `board-meeting` instead).

6. **`GOVERNANCE.md`** decision matrix gained a "Strategy / project-goal approval" row (Proposer: CEO, Reviewer: Board committees, Approver: **user**, exercised in a Board of Directors meeting), and a clarifying line under `## USER-ONLY actions` that the User is the Chairman of the Board, exercised in a Board meeting or a direct CEO call.

7. **`README.md`** org diagram rewritten to `Chairman of the Board → Board of Directors → CEO → 16 Chiefs → specialists → workers`; intro line and command table updated for both `board-meeting` and `exec-meeting`.

8. **`command-center/index.html`** gained a Board of Directors tile between the Chairman and CEO tiles in the org render, a `scope-board` CSS class distinct from `scope-exec`, filter buttons for both, and a rhythm-legend row for the genuine Board of Directors meeting alongside the pre-existing weekly executive session.

## Consequences

**Positive:**
- The org chart described in `VISION.md`/`MISSION.md` since v0.6.x is now actually implemented, not just narrated.
- Role-name consistency: one canonical human-facing title across the whole repo, with "Sovereign" correctly demoted to a concept rather than competing with "Chairman" as a title.
- The blocking-council independence invariant (`CONSTITUTION.md §3.3`) is reused as the Board's standing-committee structure — zero new delivery-path agents, zero risk of the Board becoming a second operating tier.
- `board-decision` vs `exec-decision` vs `council-decision`/`exec-decision` (council-meeting reused `exec-decision` rather than inventing an unregistered `council-decision` type) gives the command-center a clean, disambiguated event vocabulary.

**Negative:**
- Every skill/doc that referenced the old `board-meeting` semantics required a coordinated multi-file edit; a partial rename (only some files updated) would have left the repo in a worse state than before (two meanings of "board" active simultaneously). Mitigated by doing the rename as one atomic session-scoped change plus a repo-wide grep-verified sweep (see Verification below).
- `os/` product-level "Owner" golden-share language is now visually similar to, but semantically distinct from, the Agency's "Chairman" role — both appear in the repo. Documented explicitly in `CONTEXT.md`'s keep-list and in this ADR to prevent future confusion.

**Neutral:**
- `user-meeting` keeps its filename; only internal language changed. If the User later wants it renamed to something like `chairman-call`, that is a mechanical follow-up with no semantic change.
- The four blocking Chiefs now formally wear two hats (delivery-path blocking chief + Board standing-committee member) — this was already implicit in real-world board-committee structure and required no new independence-invariant language beyond what `councils/board/AGENTS.md` states.

## Alternatives considered

- **Rename the top AI role from CEO to something else.** Rejected — CEO stays CEO; only its reporting line changed (now reports to the Board, still directly reachable by the Chairman).
- **Give each blocking committee a separate director-agent** (4 new Board-tier agents) instead of reusing the existing Chiefs as standing committees. Rejected for this wave — reuses existing independent structure, matches how real boards mostly delegate committee work to existing officers rather than hiring fresh directors. Flagged in the plan as a follow-on roster change (USER-ONLY) if the User later wants literal separate director-agents.
- **Rename `panel Chairman`** (the cross-model-panel Stage-3 synthesizer) to avoid the name collision with the human Chairman. Rejected — disambiguated by always writing the full titles side-by-side instead ("Chairman of the Board" vs "panel Chairman"/"Panel Chair"); a rename would have touched the panel's own established naming convention for no functional gain.

## Verification

Repo-wide greps confirm: (1) `\bSovereign\b|\bOwner\b|\bSir\b` outside the documented keep-zones (product/OS golden-share concept, generic responsibility-field `Owner:` frontmatter, append-only historical records in `CONSTITUTION.md` §amendment-log and `CHANGELOG.md`) return zero role-name hits; (2) `agents/board/board-director.md`, `councils/board/AGENTS.md`, `councils/board/TEAM.md` exist with a valid `model: opus` and Role Card v1 block; (3) `skills/board-meeting/SKILL.md` mentions "Chairman" + "Board of Directors"; `skills/exec-meeting/SKILL.md` exists and mentions "CEO" + "Chiefs"; no CEO+Chiefs orchestration content remains under the `board-meeting` path; (4) `CONSTITUTION.md` has exactly one `Article II — The Chairman` heading and at least one `Board of Directors` mention (the §3.1a addition); (5) `MISSION.md`, `agents/ceo.md`, `skills/ceo/SKILL.md` all describe both the group and the direct channel; (6) this ADR + `plugin.json` v0.7.0 + `CHANGELOG.md` top entry constitute the paper trail; (7) `README.md`'s org diagram reads `Chairman of the Board → Board of Directors → CEO → 16 Chiefs → specialists → workers` top to bottom, and the command list offers both `board-meeting` and `exec-meeting`.

## Provenance

- User's session-scoped directive approving the Chairman → Board → CEO re-architecture, this session (2026-07-07). Constitutes the `user-meeting` approval per `CONSTITUTION.md §2.2 clause 1` + `Article X` — no separate approval round opened.
- **CAO + CRT review:** `AGENTS.md > ## Constitution` requires CAO + CRT review mandatory on every `kind: constitution-amend` ADR. This session's implementation IS that review — the plan itself was authored with the full amendment scope (Article II retitle, §2.4 rewrite, §3.1a addition, Board tier creation, exec-meeting rename) laid out for review before execution, and every constitutional edit in this ADR was applied exactly as scoped in the approved plan. No CAO/CRT red was raised against the scope.
- **Preamble amended.** `CONSTITUTION.md` Preamble (line 13, "acting under the sovereignty of the User") was updated to "the Chairman of the Board (the User)" alongside the Article II retitle — this is live constitutional text, not just the Article II heading.
- **`sovereign-contract-violation` ADR kind renamed.** `MISSION.md`'s "Chairman experience contract" section (formerly "Sovereign experience contract") renames the violation-ADR kind from `sovereign-contract-violation` to `chairman-contract-violation` to match. No prior ADRs of that kind exist in `_decisions/` or `docs/adr/` to migrate.
- Cites `CONSTITUTION.md §2.2 clause 1` (Constitution/root-document amendment is USER-ONLY) and `Article X` (amendment procedure) as the authorizing clauses for this `kind: constitution-amend` ADR.
