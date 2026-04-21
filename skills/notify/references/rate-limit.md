# rate-limit.md — dedupe, digest, opt-out

## Hard cap

- 5 notifies per project run (counted across all events).
- The 6th and subsequent trigger the **digest** behaviour: buffer the payloads, emit one combined notify at the next phase boundary with `note: "<N> events · see status.json > notifications"` and `refs` listing every buffered event.

## Dedupe

- Key: `(event, slug, note)`. If that exact triple has already fired this session, do not emit again.
- If `(event, slug)` has fired with a different `note`, emit the new one with a trailing `" (2nd time, N total)"`.

## Severity escalation

- An `info` event that fires twice for the same `(event, slug)` escalates to `warn` on the second emission.
- A `warn` event that fires twice stays `warn` but sets `refs` to the union of both occurrences.

## Opt-out

Two paths:

1. **Project-scoped.** `status.json > notifications.optOut: true`. Suppresses all transports for that slug.
2. **User-scoped.** A chat utterance like "stop pinging me", "quiet mode", "no notifications". CEO sets `_memory/MEMORY.md > ## Preferences (from user) · quiet mode`. New projects default to `optOut: true` until the user reverses.

Opt-out **still emits the `[notify]` line** on the CEO's final reply at close. This is non-negotiable — the close signal is the one thing the user always sees.

## Counters

The rate-limit skill keeps an in-memory counter per session:

```
sent: 3 / 5
buffered: 1
lastByEvent: { "task-blocked": 2, "gate-red": 1 }
```

On session close (CEO's Phase 7), emit any remaining buffered events as a single digest. Persist the final counters to `status.json > notifications.history[]` so the next project run can diff.
