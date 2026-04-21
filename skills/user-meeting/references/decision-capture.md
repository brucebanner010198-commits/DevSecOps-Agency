# user-meeting — decision capture rules

Every commitment captured unambiguously. A decision the user can later say "I didn't mean that" is a bug in this skill.

## Capture format

In minutes `## Decisions` section, each decision is a single line:

```
- <verb> · <object> · <by when / under what condition> · source line: <minutes:line>
```

Examples:
- `approved · build <idea-slug-1> as project · ETA 8-12 weeks from 2026-05-01 · source line: minutes:42`
- `queued · <idea-slug-3> for next pipeline cycle · condition: current projects both green · source line: minutes:47`
- `rejected · <idea-slug-4> · reason: mission-stretch not a fit right now · source line: minutes:49`

No compound decisions. One line per commit.

## Constraint capture

`## Constraints` section, each as a testable assertion:

```
- ETA: <range> (assumptions: <list>)
- Budget: <amount or "standard">
- Must-not-have: <specific, not vague>
- Hard deadline: <date or "none">
- Scope out: <list of explicit exclusions>
```

Vague rules:
- "Keep it simple" → NOT acceptable. Push for specifics: "no auth", "no multi-tenant", "no billing". If user insists on "simple", capture verbatim and mark for pm-lead interpretation, then confirm interpretation with user before phase 4 close.
- "As fast as possible" → NOT acceptable as ETA. Push for a range.

## Reflect-back script

Before writing to minutes file, CEO says:

```
Let me play back what I heard:
- You picked <X> and <Y>.
- ETA <range>, starting <date>.
- Hard constraints: <list>.
- Things you explicitly don't want: <list>.

Is any of that off?
```

Edit until user confirms. Confirmation phrase (or paraphrase of "yes that's right") must appear in minutes.

## Ambiguity defaults

If user-stated constraint is ambiguous and CEO cannot force a resolution:

- Write the constraint verbatim.
- Add CEO's working interpretation.
- Flag as `needs-decision` task for the first Chief who will be affected.
- First Chief raises the interpretation question back to CEO (not the user) within phase 0 of their work. CEO escalates back to user only if the Chief cannot resolve.

## Disagreement capture

If user disagrees with CEO's recommendation or with `opportunity-ranker`:

```
`## Overrides`
- CEO recommended: <X>
- User selected: <Y>
- User's reason (verbatim): "<quote>"
- CEO's acceptance: accepted · ADR filed as ADR-NNNN
```

Never argue in minutes. Disagreement captured, CEO moves on.

## ETA phrasing

Always a range. Always anchored. Always with assumptions.

- OK: "8-12 weeks starting 2026-05-01, assumes backend-dev and frontend-dev at 0.5 FTE each, no external-blocker"
- NOT OK: "8 weeks"
- NOT OK: "end of Q2"
- NOT OK: "soonish"

If user commits to a range shorter than ranker's estimate, that's a `risk-acceptance` ADR and minutes note the delta.

## Action items

Every bullet in `## Action items` format:

```
- [ ] <action · owner (agent slug) · due <date or "ASAP">> — task: <taskflow ID, back-filled>
```

- Action must be imperative ("design schema", not "think about schema").
- Owner must be a real agent slug (see `agents/` dir).
- Due date required for anything user-visible. Internal tasks may use ASAP or "before phase 2 of project".
- Task ID back-filled after `taskflow.create`. Minutes file gets re-saved once back-fill done.

## What never goes in minutes

- Unsaid subtext ("I think the user seemed uncertain about...")
- Speculation on user motivation
- Internal debates between Chiefs that happened after the meeting
- Anything the user would read and say "that's not what I meant"
