# Fix-loop — the 2-attempt cap

Every `(council, phase)` pair gets at most **2 fix-loops** after the initial dispatch. On attempt 3 the task is `blocked` and the user decides.

Motivation: unbounded fix-loops are how AI systems burn tokens without converging. A hard cap forces the CEO to escalate with a clear options list instead of thrashing.

## The counting rule

- Initial dispatch: `fixAttempts == 0`.
- First fix-loop: `fixAttempts == 1`.
- Second fix-loop: `fixAttempts == 2`.
- Would-be third fix-loop: task transitions to `blocked` instead. The `metrics.fixLoops` counter increments by 1 for each `needs-decision → in-progress` transition (so max 2 per task).

## Dispatch template (fix-loop)

When issuing a fix-loop, the CEO writes a `fix-loop` entry to `chat.jsonl` that echoes the Chief's `red` report and lists specific corrections:

```json
{
  "ts": "<iso>",
  "scope": "board",
  "from": "ceo",
  "to": "<chief>",
  "type": "fix-loop",
  "phase": "<phase>",
  "attempt": 1,
  "prevReportTs": "<iso of the red report>",
  "corrections": [
    "the PII classification is missing for `users.email` — add it per `councils/architecture/AGENTS.md`",
    "the compliance.md must cite `council/security/AGENTS.md > Must` row 3"
  ],
  "retainArtifacts": ["threat-model.md"],
  "deadline": null
}
```

Rules:
- `corrections[]` must name specific Must/Must-not rows or specific lines in the prior artifact. No "try harder" or "improve quality."
- `retainArtifacts[]` names the files the Chief should keep (not rewrite). Anything not listed is free to regenerate.
- `attempt` matches what `fixAttempts` will be after this loop runs (so 1 or 2).

## Escalation template (after 2 failed fix-loops)

When `fixAttempts == 2` and the Chief still reports `red`, the task goes `blocked` and the CEO writes an `inbox.json` entry:

```json
{
  "id": "inbox-0004",
  "openedAt": "<iso>",
  "taskId": "t-0007",
  "council": "security",
  "phase": "verify",
  "chief": "security-lead",
  "summary": "auth rate-limit still High after 2 fix-loops",
  "whatWorks": "JWT signing, token expiry, refresh flow all pass STRIDE/OWASP",
  "whatsStillRed": "rate limit on /login can be bypassed by rotating source IPs via the reverse-proxy header",
  "options": [
    {"id": "A", "label": "Fix now — add IP-binding to session + cloud-WAF rule (adds ~1 day)",  "recommended": true},
    {"id": "B", "label": "Ship behind a feature flag, fix in v1.1 (opens a ~7-day window of risk)"},
    {"id": "C", "label": "Ship as-is with user-accepted risk (highest risk, fastest)"}
  ],
  "ceoRecommendation": "A. Cost is cheap relative to an auth bypass; the WAF rule alone blocks the vector."
}
```

The CEO does not proceed until the user answers. Command-center surfaces this.

## On user response

| User choice        | Task transition                            | Aggregator effect                             |
| ------------------ | ------------------------------------------ | --------------------------------------------- |
| Pick option A (fix) | `blocked → in-progress` (fresh `fixAttempts=0` for the new plan) | gate stays `red` until the re-run             |
| Pick option B/C with waiver | `blocked → done`                  | `gates.waivers` entry; `followups` entry with severity                   |
| Cancel the task    | `blocked → cancelled`                      | phase may not be completable; CEO explains    |

Note: when the user picks a fix path, the CEO creates a **new task** (not a third fix-loop on the old one) with `kind: "escalation-response"`. This preserves the cap — a user-chosen fix path is not the same as the Chief trying a third time unsupervised.

## Anti-patterns

- **Silent retry.** Running the Chief a third time without writing a `fix-loop` or `escalate` entry. Looks like progress, actually burns tokens.
- **Fix-loop with vague corrections.** "Please improve the threat model" → the Chief produces roughly the same artifact. Use specific Must/Must-not row references.
- **Dropping retained artifacts.** If the first attempt got the threat model right and only missed compliance.md, the fix-loop should retain the threat model. Losing it wastes context-window and invites drift.
- **Skipping the inbox entry.** After 2 failed loops, `blocked` without `inboxItem` is a bug. Command-center will show the task as blocked but the user won't see why.
- **Recounting user-chosen fixes as fix-loops.** The 2-attempt cap is per Chief-autonomous run. User-directed retries count as new tasks.

## Quick reference

```
attempt 0  →  Chief first try.                        gate in {green,yellow,red}
attempt 1  →  fix-loop #1 if attempt 0 was red.       gate in {green,yellow,red}
attempt 2  →  fix-loop #2 if attempt 1 was red.       gate in {green,yellow,red}
attempt 3+ →  FORBIDDEN. Task is `blocked`. User decides next move.
```

That's the whole rule.
