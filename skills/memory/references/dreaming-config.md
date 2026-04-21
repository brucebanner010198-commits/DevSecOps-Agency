# dreaming-config — knob defaults

Defaults ported from openclaw `MemoryLightDreamingConfig` / `MemoryDeepDreamingConfig` / `MemoryRemDreamingConfig`. Tune only when you have a reason.

## Light

| Knob                 | Default | Meaning                                                     |
| -------------------- | ------- | ----------------------------------------------------------- |
| `lookback_days`      | 1       | Only consider phase artifacts created in the last N days.   |
| `dedupe_similarity`  | 0.85    | If a new bullet's cosine/token similarity to an existing bullet in today's file ≥ this, merge instead of append. (Approximate via substring + shared-token heuristic — no embedding needed at this tier.) |
| `max_bullets`        | 7       | Hard cap per phase. If the phase produced more than 7 real facts, pick the 7 highest-value. |
| `required_categories`| `[facts, risk, decision, pattern]` | Each bullet prefixed with one category.       |

Tune `max_bullets` up for Phase 2 (Design) and Phase 4 (Verify) which tend to produce more facts. Never tune it above 12.

## Deep

| Knob                                  | Default | Meaning                                                                                  |
| ------------------------------------- | ------- | ---------------------------------------------------------------------------------------- |
| `recency_half_life_days`              | 14      | Weight recent artifacts more when two conflicting facts exist. Half-weight after 14 days. |
| `recovery_enabled`                    | true    | If the project was marked `blocked` or the close-out is partial, attempt recovery — pull what you can. |
| `recovery_trigger_below_health`       | 0.6     | "Health" = completed phases / 7. Below 0.6 triggers recovery mode (more tentative bullets, marked `[tentative]`). |
| `recovery_auto_write_min_confidence`  | 0.75    | Tentative bullets only get written if ≥ this confidence. Below, skip and note in `chat.jsonl`. |
| `required_sections`                   | `[What shipped, What worked, What was gated, Recurring risks, Reusable decisions]` | Always write all five sections, even if empty. Empty ones get `_(none)_`. |

## REM

| Knob                   | Default | Meaning                                                                              |
| ---------------------- | ------- | ------------------------------------------------------------------------------------ |
| `min_pattern_strength` | 0.7     | Approximate heuristic: pattern appears in ≥ 2 project files AND contradicts no `MEMORY.md` entry. |
| `max_new_bullets`      | 10      | Per REM run. Prevents `MEMORY.md` from exploding.                                    |
| `sections_writable`    | `[Preferences (from user), Recurring risks, Proven stacks, Anti-patterns, Open questions]` | Never add a new top-level section in REM — only append under existing ones. |

## When to re-dream

- Light: always, every phase.
- Deep: always, every project close. If a Deep run fails (agent errors out mid-write), re-run it — append-only rules mean it's safe.
- REM: when ≥ 3 new `patterns/*.md` files exist since last REM. Tracked in `_memory/index.json.lastRem`.

## What not to write

- Secrets, tokens, emails, customer PII — redact before write (see `write-policy.md`).
- Speculation without a source artifact path.
- A fact already present verbatim in the target file (dedupe).
- Negative facts about the user ("user was slow to respond", "user unclear"). Memory is about the work, not the operator.
