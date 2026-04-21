# vision-template — exact VISION.md skeleton

Paste-and-fill. No freestyle. The CEO writes every character below verbatim; only the angle-bracket tokens get replaced.

## Skeleton (empty)

```markdown
# devsecops-agency · vision

## Mission
<one sentence, present tense, 15 words max. Ends with a period.>

## Active OKRs (this quarter)
- [O1] <outcome statement — what changes in the world>
  - [KR1.1] <measurable, dated key result>
  - [KR1.2] <measurable, dated key result>
- [O2] <outcome statement>
  - [KR2.1] <measurable, dated key result>

## Non-goals
- <thing the agency will not do this quarter>
- <thing the agency will not do this quarter>

## Last updated
YYYY-MM-DD by <actor> — <one-line rationale>
```

## Skeleton (example filled)

```markdown
# devsecops-agency · vision

## Mission
Ship revenue-positive software products for Sir, autonomously, at 2 launches per quarter.

## Active OKRs (this quarter)
- [O1] Launch 2 revenue-positive products by 2026-07-31
  - [KR1.1] Product A reaches $100 MRR within 30 days of launch
  - [KR1.2] Product B reaches first paying user within 14 days of launch
  - [KR1.3] Median time-from-idea-to-launch stays under 21 days
- [O2] Zero Critical security findings shipped to production
  - [KR2.1] Every release has a clean CISO second-pass signoff
  - [KR2.2] Red-team council runs on 100% of launches
- [O3] Memory compounds across projects
  - [KR3.1] ≥ 3 `_memory/patterns/*.md` referenced per new project brief
  - [KR3.2] REM dreaming runs after every retro with ≥ 1 new MEMORY.md bullet

## Non-goals
- Regulated-industry products (healthcare, financial services) — out of scope for Q2
- Mobile-native apps — web-only this quarter
- Enterprise sales motion — self-serve only

## Last updated
2026-04-21 by ceo — bootstrap after first user top-5 meeting
```

## Caps (enforced at write time)

- Mission: ≤ 25 words, single sentence.
- OKRs (`O` blocks): ≤ 5.
- KRs per O: ≤ 3.
- Non-goals: ≤ 5.
- Total file: ≤ 60 lines of markdown including blank lines.

If the caps are exceeded, the oldest O rolls off into `_vision/history/<today>.md` before the new O is written. `history/` entries are append-only and carry the full O + KR block verbatim plus a one-line reason.

## What belongs in `history/`

- Every edit to `VISION.md` (even a typo fix) writes a paired `history/<today>.md` entry.
- Entry shape:
  ```
  ## YYYY-MM-DD HH:MM — <actor>
  Change: <one line>
  Before: <verbatim removed block, if any>
  After: <verbatim added block, if any>
  Why: <one line rationale, preferably with ADR reference ADR-NNNN>
  ```
- Never write a `history/` entry without a paired ADR if the change is material (mission rewrite, OKR add/remove, non-goal add/remove).
