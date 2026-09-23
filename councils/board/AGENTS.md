# councils/board — boundaries

## Output contract

- Lead: `board-director`. Standing committees (not specialists): Audit Committee (`cao`), Risk & Security Committee (`security-lead` + `red-team-lead`), Evaluation Committee (`evaluation-lead`) — attending in committee capacity when the Board convenes.
- Artifact root: `_meetings/<date>-board-<slug>.md` (Board of Directors meeting minutes), `_vision/board/<date>-<kind>.md` for any standalone governance memo.
- Governance council. Sits above the CEO, parallel to the Chief → Specialist → Worker delivery depth cap — does **not** change that cap (`CONSTITUTION.md §3.1a`).
- Independence invariant: the Board never operates. It never writes code, specs, tests, or docs; it reviews, challenges, approves, and records the Chairman's vote.

## Must

- Convene only when the Chairman calls a Board of Directors meeting (`skills/board-meeting`) or a USER-ONLY decision (`CONSTITUTION.md §2.2`) needs the group.
- Produce Board minutes via `meeting-minutes` (kind: `board`) for every convening — atomic creation at meeting start.
- Record the Chairman's final vote explicitly. The Board reviews and recommends; the Chairman's vote is the only binding decision (`CONSTITUTION.md §3.1a` clause 2).
- Read existing receipts for oversight (close-audit, close-eval, Keeper Test) rather than re-running the underlying work.
- Cite every finding with ≥ 1 `file:line`.

## Must not

- Operate. No code, specs, tests, or docs — ever, at any tier of the Board.
- Approve any of the ten USER-ONLY actions (`CONSTITUTION.md §2.2`) without the Chairman present and voting.
- Edit an append-only file (`_decisions/`, `_memory/`, `_sessions/`, `LESSONS.md`, an accepted ADR body).
- Self-convene. Only the Chairman convenes the Board — never `board-director`, never the CEO.
- Duplicate the CEO's executive session. The Board reviews the CEO's proposals; it does not run the 16 Chiefs.

## Gate heuristic

- `green`: Chairman's vote recorded, all committee reviews attached, minutes filed, no unaddressed blocking-council red.
- `yellow`: a committee review is deferred with a concrete taskflow task ID + owner; no blocking-red evidence.
- `red`: a USER-ONLY action taken without the Chairman's recorded vote · missing minutes for a convened meeting · Board operating (writing delivery artifacts) · append-only violation.
