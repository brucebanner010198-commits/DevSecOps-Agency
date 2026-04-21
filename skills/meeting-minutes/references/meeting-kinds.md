# meeting-kinds — full table

| Kind                       | Chair  | Typical attendees                        | Mandatory minutes? | Typical cadence            |
| -------------------------- | ------ | ---------------------------------------- | ------------------ | -------------------------- |
| `user`                     | CEO    | CEO + user                               | Yes, always        | On top-5 pitch / escalation/ retro |
| `board`                    | CEO    | CEO + ≥ 2 Chiefs                         | Yes, always        | Phase transitions (Discovery → Design etc.) |
| `council-<council>`        | Chief  | Chief + specialists                      | Conditional (see below) | Phase kick-off, fix-loop triage |
| `red-team`                 | CISO   | CISO + red-team agents (Wave 6)          | Yes, always        | Pre-Ship gate, post-deploy sampling |
| `audit`                    | CAO    | CAO + audit specialists (Wave 3)         | Yes, always        | Quarterly + on-demand      |
| `retro`                    | CEO    | CEO + user (optional)                    | Yes, always        | Post-ship on every project |

## Conditional: council minutes

Blocking councils — **always mandatory** minutes:
- `council-security` (CISO)
- `council-legal` (GC)

Informing councils — minutes **only if**:
- A waiver is being considered, OR
- The council is escalating to CEO, OR
- The council is formally planning scope (kick-off of a new council skill).

Otherwise informing councils log only to `chat.jsonl`. Keeps the `_meetings/` directory scoped to actual decision-making moments.

## Suffixing rule

If two meetings of the same kind happen the same day:
- Add `-am` / `-pm` if time-of-day differs meaningfully.
- Add `-1` / `-2` otherwise.
- Three or more same-kind same-day → `-1` / `-2` / `-3`.

## Attendee roles (free text, but conventional)

- `user` — Sir (the human user).
- `ceo`, `cro`, `cpo`, `cto`, `ciso`, `cqo`, `vp-eng`, `vp-ops`, `cko`, `gc` — Chief slugs.
- `coo`, `cao`, `cmo`, `cfo`, `cso`, `eval-lead`, `sre-lead` — future Chief slugs (Waves 2–7).
- `<specialist-slug>` — any agent filename under `agents/`.

## Decision routing by kind

- `user` meetings → decisions often become OKRs (vision-doc edit) or project picks (new slug). ADRs filed for every idea pick and ETA commit.
- `board` meetings → decisions often become phase advances or roster changes. ADRs for roster changes and non-obvious phase deltas.
- `council-security` / `council-legal` → decisions often become waivers or gate overrides. ADRs mandatory.
- `red-team` → decisions become CVE-like findings + remediation tasks. ADRs for any "accept-risk" outcome.
- `audit` → decisions become remediation tasks + process ADRs.
- `retro` → decisions often retire OKRs (user) or propose roster changes. ADRs for each.

## Meeting-length expectations

- `user` — aim short, 5–15 min equivalent of dialogue; minutes ≤ 120 lines.
- `board` — 5–10 topics; minutes ≤ 150 lines.
- `council-*` — 1–3 topics; minutes ≤ 80 lines.
- `red-team` / `audit` — finding-dense; minutes cap still 180 lines; overflow → appendix file referenced from minutes.
- `retro` — topic-rich; split into multiple minutes if > 180 lines.
