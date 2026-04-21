# user-meeting — top-5 narration script

Script is opinionated. CEO may adapt phrasing to current user preference (see `_memory/MEMORY.md > ## Preferences`), but the structure is fixed.

## Opening (≤ 30 seconds)

```
Five ideas surfaced this cycle. Strategy council ranked them by RICE plus
narrative. I'll walk each under 60 seconds — you can stop me anywhere.

Goal of this meeting: you pick 1 or 2 to build next. Everything else I can
queue for later or kill outright. Your call.

Ready?
```

## Per-idea card (≤ 60 seconds)

```
Idea <N>: <name>.

<Elevator pitch verbatim from positioning-strategist.>

Wedge: <one line from positioning>.
Who wants this: <audience line>.

Numbers: TAM <$X>, SOM <$Y>, effort <weeks range>. Confidence <L/M/H>,
basis <cite>.

Proof: <fact 1>. <fact 2>.

Risks: <risk 1 · mitigation>. <risk 2 · mitigation>.

Composite score <0-5>.

Questions on this one?
```

Pause. Answer or note the question. Move on when user says "ok" or "next".

## Bridge between cards (optional)

Use only if user seems fatigued:

```
Three down, two to go. Want a minute?
```

## After all five (≤ 90 seconds)

```
Quick recap: <N names in composite order>.

If you want my read: <CEO recommendation, one sentence, citing one reason>.
But it's your call.

Which are you drawn to?
```

Wait. Do not suggest until user speaks.

## If user asks "which do you think?" before all cards done

```
I have a read but I'd rather finish the cards first — it's quick and
sometimes the last one surprises people. Can we finish and then I'll give
my take?
```

If user insists, give the read and then finish the remaining cards.

## If user picks 3+

```
Great. We have capacity for 1-2 this cycle. Can you rank your 3? I'll
queue the lower-ranked for next pipeline — it won't rot.
```

## If user rejects all

```
Understood. Help me understand what would have made the list feel right —
a different segment? A different risk level? I'll rerun the pipeline with
that constraint and we can meet again when it's fresh.
```

Capture the constraint verbatim as `rejection_constraint` in minutes.

## If user hesitates (> 30s silent)

```
No rush. Want me to re-read any of them, or answer specific questions?
```

Never pressure. Hesitation is a signal.

## Closing (≤ 30 seconds)

```
Locked in: <picks verbatim>. ETA target <range>. I'll commit to
<specific deliverables> and flag <open risks> as we go.

Anything else before I dispatch?
```

Then: write minutes, file ADRs, create tasks, close the meeting.
