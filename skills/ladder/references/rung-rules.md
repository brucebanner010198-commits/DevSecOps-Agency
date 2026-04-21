# rung-rules — per-rung owners, budgets, entry/exit signals

Authoritative table. Every ladder climb is measured against this file.

## Rung 0 — Retry with refreshed context

- **Owner:** Originating specialist.
- **Entry:** Task red-or-yellow on first attempt where failure cause is context-thin (timeout, truncated dispatch, missing file read, hallucinated path).
- **Action:** Re-dispatch with: fresh session-log tail, fresh `brief.md` re-read, explicit path listing, scope-guard reminder.
- **Budget:** 1 attempt.
- **Exit-success:** Report green or yellow-ship.
- **Exit-fail → climb:** Second red → Rung 1.
- **ADR required:** No (this rung is absorbed into the normal retry envelope).

## Rung 1 — Fix-loop

- **Owner:** Originating Chief (tasked specialist reports to Chief).
- **Entry:** Rung 0 failed, OR task is red-not-ship on normal dispatch.
- **Action:** Per `skills/taskflow/references/fix-loop.md` — Chief issues targeted fix dispatch with remediation brief.
- **Budget:** 2 attempts (existing taskflow cap).
- **Exit-success:** Post-fix report green.
- **Exit-fail → climb:** 2nd fix-attempt still red → Rung 2.
- **ADR required:** No on entry (this is the existing default path). Yes on exit to Rung 2 (rung-transition ADR).

## Rung 2 — Alternate approach within scope

- **Owner:** Originating Chief.
- **Entry:** Fix-loop exhausted; same goal reachable via a different technical path inside the same phase scope.
- **Action:** Chief convenes a council mini-meeting to brainstorm alternates. Picks 1 and re-dispatches as a fresh task (new `taskId`; old task stays `blocked`).
- **Budget:** 1 alternate attempt. (If alternate also fails, do NOT try a second alternate at Rung 2 — climb.)
- **Exit-success:** New task green.
- **Exit-fail → climb:** Alternate fails → Rung 3.
- **ADR required:** Yes — rung-transition ADR entering Rung 2, documents the alternate chosen.

## Rung 3 — Cross-council escalation

- **Owner:** A different Chief (not the originating one). Route per `references/ladder-matrix.md`.
- **Entry:** Rung 2 failed; problem plausibly belongs to, or is unblockable only by, a different council.
- **Action:** Originating Chief writes a `handoff.md`. Second Chief convenes their council, treats the problem as inbound. Cross-council board mini-meeting may be invoked.
- **Budget:** 2 attempts by the receiving council (per the fix-loop cap applied within their scope).
- **Exit-success:** Receiving council ships a fix.
- **Exit-fail → climb:** Receiving council cannot resolve → Rung 4.
- **ADR required:** Yes — rung-transition ADR names both councils and the handoff artifact.

## Rung 4 — Hire / repurpose a specialist

- **Owner:** COO (People-ops). Executes via `skills/roster` + `hiring-lead` + `skill-creator`.
- **Entry:** Rung 3 failed; diagnosis says the agency lacks a specialist of the required shape — OR existing specialist's prompt is structurally wrong for the problem.
- **Action:** COO runs `roster` flow — Hire a new specialist, or Repurpose an idle one, or Prompt-upgrade an existing one. New / updated specialist picks up the blocked task.
- **Budget:** 1 hire attempt + 2 fix-loop attempts by the new specialist (= 3 total).
- **Exit-success:** New / repurposed specialist ships a fix.
- **Exit-fail → climb:** Hire executed and still red → Rung 5.
- **ADR required:** Yes — rung-transition ADR + the standard roster-mutation ADR(s) (Hire / Repurpose / Prompt upgrade).

## Rung 5 — Scope pivot (same mission, different path)

- **Owner:** CPO (Product) + CEO.
- **Entry:** Rung 4 failed; original product scope is provably unattainable under current tech / cost / time constraints, but the mission-level goal survives.
- **Action:** CPO rewrites `brief.md` scope section. CEO convenes a user-meeting (`skills/user-meeting`) to propose the pivoted scope. User approves before execution resumes.
- **Budget:** 1 pivot proposal. User answers yes / no / rework-once.
- **Exit-success:** User approves; pivoted scope re-enters pipeline at the phase where it became unblockable (usually Research or Product).
- **Exit-fail → climb:** User rejects pivot without a counter-proposal → Rung 6. (User counter-proposal = accept, replan at Rung 5.)
- **ADR required:** Yes — rung-transition ADR + scope-amendment ADR.

## Rung 6 — User consult (irreducible)

- **Owner:** User (with CEO as scribe).
- **Entry:** Rung 5 failed, OR the blocker is provably user-only from the start (credentials, payment authorization, legal waiver, irreducible product judgment, blocking-council red with no technical workaround).
- **Action:** CEO writes a single-question `user-meeting` (minutes `kind: user`). Question is yes/no or bounded multiple-choice. Options include: waiver, scope narrowing, park, cancel.
- **Budget:** 1 question. Timeout = 7 days (CEO calendar). No answer → auto-advance to Rung 7.
- **Exit-success:** User answers; task resumes at the appropriate earlier rung per the answer.
- **Exit-fail → climb:** User declines to waiver AND declines to pivot AND declines to cancel — OR 7-day timeout → Rung 7.
- **ADR required:** Yes — rung-transition ADR + user-decision ADR + meeting minutes.

## Rung 7 — Parking lot (documented defer)

- **Owner:** CEO.
- **Entry:** All prior rungs exhausted, OR Rung 6 timed out, OR user explicitly parked.
- **Action:** CEO writes `_vision/parking/<slug>.md` capturing:
  - The original mission + why it's parked.
  - Every rung attempted + outcome.
  - All artifacts preserved (pointers to `_sessions/`, `_memory/`, worktree branches — nothing deleted).
  - **Reconsider-trigger:** explicit condition under which the task revives (new tech available, policy change, user returns with budget, etc.).
- **Budget:** Terminal. No further rungs.
- **Exit-success:** Parked state written; reconsider-trigger recorded; task leaves active portfolio.
- **Exit-fail:** N/A — Rung 7 cannot fail because "park" is the outcome.
- **ADR required:** Yes — terminal parking ADR. Parking-lot tasks surface in every subsequent portfolio audit until the reconsider-trigger fires or user cancels.

## Rung skip rules

- **Upward skip** requires an ADR that names both the rung skipped and the rung entered, with a justification fitting one of these exceptions:
  - Rung 6 required by nature (user credentials / legal waiver / irreducible user judgment) — CEO may enter Rung 6 directly.
  - Scope pivot (Rung 5) required by nature (user explicitly asked for pivot) — CEO may enter Rung 5 directly.
  - Rung 4 Hire required by nature (user specifically asked for a new specialist type) — COO may enter Rung 4 directly.
- **Downward descent** (tried Rung N, going back to Rung N-M) is allowed with an ADR explaining the new information that reopens earlier rungs.

## Budget totals

If a task climbs the full ladder without skipping: 1 + 2 + 1 + 2 + 3 + 1 + 1 = 11 attempts across 7 rungs before parking. Plus Rung 0's opportunistic retry = 12.

Portfolio audit flag: any task burning > 8 attempts without a terminal outcome is CAO-escalated.
