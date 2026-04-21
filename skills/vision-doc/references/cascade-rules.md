# cascade-rules — which 3 OKRs get selected for which phase

The CEO runs this selection before every Chief dispatch. No OKR bullet ships to a dispatch without a relevance check.

## Inputs

- `VISION.md > ## Active OKRs` — all active KR lines.
- `_vision/projects/<slug>.md > ## Project OKRs` — per-project KR lines, if present.
- The dispatch: Chief slug, phase name, task title.

## Selection algorithm

1. **Build the KR pool.** Flatten all KR lines from workspace VISION + project VISION into one list. Each line tagged with its owner and source.
2. **Tokenise.** Strip markdown, lowercase, split on whitespace + `-`, drop stop-words.
3. **Score each KR line** against the dispatch context:
   - dispatch context = Chief slug + phase name + task title + the relevant council's `## Must` header.
   - score = Jaccard similarity between KR tokens and context tokens.
4. **Apply owner bonus.** If the KR's owner == dispatch Chief, add `+0.1` to score.
5. **Apply phase bonus.** Phase-specific keywords boost matching KRs:
   - Discovery → market, users, research, wedge, competitor
   - Design → architecture, api, data-model, threat-model
   - Build → implementation, code, integration
   - Verify → test, qa, coverage, performance, a11y
   - Ship → deploy, ci, observability, rollback
   - Document → docs, readme, tutorial
   - Close → ship, retro, memory
6. **Sort descending**, pick **top 3**.
7. **Always include** any KR that is at `red` on its last score (regression watch) even if outside top-3 — swap into slot 3 if present.

Cap: always exactly 3 bullets in the dispatch slice. If fewer than 3 KRs are active, pad with `- (no active KR applies — proceed on first-principles)`.

## Non-goal selection

Separately from KR selection, prepend **0–2 non-goals** to the dispatch slice if their tokens overlap the task title with Jaccard ≥ 0.3. Non-goals that do not match are omitted — do not spray irrelevant non-goals into every dispatch.

## Example: CRO dispatched for Discovery on a "student expense tracker" task

KR pool:
- [KR1.1] Product A reaches $100 MRR within 30 days of launch (owner: cpo)
- [KR1.2] Product B reaches first paying user within 14 days (owner: cpo)
- [KR1.3] Median time-from-idea-to-launch stays under 21 days (owner: ceo)
- [KR2.1] Every release has a clean CISO second-pass signoff (owner: ciso)
- [KR2.2] Red-team council runs on 100% of launches (owner: ciso)
- [KR3.1] ≥ 3 patterns cited per new project brief (owner: ceo)

Context tokens (Discovery phase, CRO, "student expense tracker"):
`discovery, cro, market, users, research, wedge, competitor, student, expense, tracker`

Scores (after bonuses):
1. [KR3.1] — "per new project brief" → project/brief overlap → 0.35 (ceo owner bonus applies weakly)
2. [KR1.1] — "product A … MRR" → weak overlap, but revenue-per-launch is CRO-relevant → 0.25
3. [KR1.3] — "time-from-idea-to-launch" → 0.22

Selected slice:
```
## Vision slice (read-only, for alignment)
Mission: Ship revenue-positive software products for Sir, autonomously, at 2 launches per quarter.
Relevant OKRs:
- [KR3.1] ≥ 3 memory/patterns/*.md cited per new project brief
- [KR1.1] Product A reaches $100 MRR within 30 days of launch
- [KR1.3] Median time-from-idea-to-launch stays under 21 days
Non-goals that apply: (none matched — dispatch proceeds without non-goal constraints)
```

## Drift detection

If the same KR scores < 0.1 against every dispatch for 2 consecutive phases across all projects this quarter, the CEO flags it in the next retro as "possibly stale — consider rolling to history." The retro decides, not the dispatch loop.

## Never

- Ship more than 3 KR bullets.
- Ship a KR bullet in a format other than `- [KR<n.n>] <text>`.
- Omit the `Mission:` line.
- Ship a non-goal that did not score ≥ 0.3.
- Compute relevance from the Chief slug alone — always include phase + task title.
