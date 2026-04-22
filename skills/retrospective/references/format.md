# retrospective/references/format.md

The 10 sections of `_meetings/<slug>-retro-<YYYY-MM-DD>.md`. Each shown with section rules and a worked example.

## Header

```
# <slug> — retrospective (<YYYY-MM-DD>)

- **Outcome:** shipped / blocked / parked-rung-7
- **Kind:** project-close / portfolio / incident / wave
- **Attendees:** ceo, cao, cevo, crt  (list actual attendees; any absence noted)
- **Session IDs:** ceo=<id>, chief-<slug>=<id>, ...
```

## 1. `## Context`

Three lines, max. Slug, date range, one-line description of what was attempted.

Example:

```
## Context

- Project: invoice-splitter
- Dates: 2026-04-18 → 2026-04-21
- Goal: secure invoice-splitting web app for roommates, shipped to Vercel.
```

## 2. `## Timeline`

Phase-by-phase. One sub-bullet per phase outcome, cited to the session log.

Example:

```
## Timeline

- Discovery — green. Wedge: dorms. CRO report: `_sessions/cro/b8d2.jsonl:L42`.
- Design — yellow. Architecture docs thin on auth flow. CTO report: `_sessions/engineering-lead/77c1.jsonl:L67`.
- Build — green. Two fix-loops in backend-dev. `status.json > metrics.fixLoops = 2`.
- Verify — yellow. Perf test borderline. `qa-report.md:§perf`.
- Ship — green. Deployed to Vercel. `deploy/observability.md:§deploy-202604201247`.
- Doc/Legal — green. `docs/tutorial/getting-started.md`, `legal/licenses.md`.
- Close — this retro.
```

## 3. `## Worked`

≤ 5 bullets. Specific, cited. What behaviour the agency should repeat.

## 4. `## Gated`

≤ 5 bullets. Specific, cited. Where gates blocked and why.

## 5. `## Loops & rungs`

Explicit numbers.

```
- Fix-loops: 2 total (backend-dev × 2 at Build). `status.json:L142`.
- Rungs traversed: 0.  (Never escalated past fix-loop cap.)
- Rung-7 parked: none.
```

## 6. `## Lessons`

≤ 3 bullets. Each is a candidate row for `LESSONS.md > lessons`. Cited.

Rule: the lesson must describe *behaviour to replicate or avoid*, not "we learned X." Bad: "We learned more about auth." Good: "OAuth on Day 2 instead of Day 4 saved the CISO gate. Replicate. `_meetings/invoice-splitter-retro-2026-04-21.md:§Timeline`."

## 7. `## Reusable decisions`

≤ 2 bullets. Each cites an ADR worth reusing across projects.

Example:

```
- ADR-0042 — pick Vercel over Fly.io for < 10k MAU side-projects (saved 40 % deploy time). `_decisions/ADR-0042-vercel.md`.
```

## 8. `## What we'd change`

≤ 3 bullets. Actions, not aspirations.

Bad: "Be better at perf testing." Good: "Add a baseline perf run at Phase 3 entry, not Phase 4. `qa-report.md:§perf`."

## 9. `## Carry-over check`

Did any "what we'd change" from the last 3 `LESSONS.md` rows repeat in this project?

- **No carry-over** → one line: "No carry-over."
- **Carry-over detected** → list each repeat with a citation. File ADR `kind: repeat-lesson`.
- **Weak-positive** (Jaccard 0.5–0.7 on the change-text) → flag for review by CAO at next portfolio audit.

See `references/carry-over-check.md` for the threshold rules.

## 10. `## Follow-ups`

Every action item paired with a `taskflow` task ID. No orphan actions.

Example:

```
## Follow-ups

- Update `agents/quality/performance-tester.md` to run baseline at Phase 3 entry — task `t-0198`.
- Archive `_worktrees/qa-lead-2/` scratch dir — task `t-0199`.
```

## Length budget

≤ 10 minutes of reading, roughly 800–1200 words. Detail goes in `_memory/patterns/<slug>.md`. Retro is the executive summary of the project's learning; the pattern file is the textbook.
