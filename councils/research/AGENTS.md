# councils/research — boundaries

## Output contract

- Lead: `cro`. Specialists: market-researcher, tech-scout, literature-reviewer, user-researcher.
- Artifact root: `<slug>/research/`. Consolidated: `<slug>/research-brief.md`.
- Verdict: **build · don't build · pivot**. Gate: green/yellow/red.

## Must

- Cite every claim. Source URL, paper, or `_memory/patterns/<prior>.md:line`.
- Distinguish primary (interviews, usage tests) from secondary (articles, reports).
- Flag conflicts between sources; do not silently pick one.
- Check `_memory/patterns/` for keyword matches before starting new research. Inject top 3 matches.
- Name the wedge (one segment, one use case) before making any build/don't call.

## Must not

- Invent user quotes. If synthesised, tag `[synthesised]`.
- Extrapolate from 1 data point to a user segment.
- Ship a "build" verdict with unresolved risk in market or tech landscape.
- Pull literature older than 5 years unless it's a foundational text (state why).

## Gate heuristic

- `green`: wedge identified, ≥ 3 primary sources, tech stack viable, no hard blocker.
- `yellow`: wedge identified but one material unknown; document it as inbox item.
- `red`: no defensible wedge OR incumbent moat is clear and insurmountable.
