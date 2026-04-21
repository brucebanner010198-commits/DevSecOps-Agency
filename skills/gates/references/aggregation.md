# Gate aggregation — worked examples

Four walk-throughs that cover the corner cases.

## Example 1 — clean green

Reports collected at project close:

| Council       | Gate   | Followups |
| ------------- | ------ | --------- |
| research      | green  | 0         |
| product       | green  | 0         |
| architecture  | green  | 0         |
| security      | green  | 0         |
| execution     | green  | 0         |
| quality       | green  | 0         |
| devops        | green  | 0         |
| docs          | green  | 0         |
| legal         | green  | 0         |

Rule 4 applies: no red, no yellow → **project gate: `green`**.

## Example 2 — documented yellow

| Council       | Gate   | Followups                                                |
| ------------- | ------ | -------------------------------------------------------- |
| research      | green  | 0                                                        |
| product       | green  | 0                                                        |
| architecture  | green  | 0                                                        |
| security      | yellow | 1: medium STRIDE item with mitigation (open)             |
| execution     | green  | 0                                                        |
| quality       | yellow | 1: one flaky test with fix plan                          |
| devops        | green  | 0                                                        |
| docs          | green  | 0                                                        |
| legal         | green  | 0                                                        |

Rule 3 applies: no red, at least one yellow → **project gate: `yellow`**. The `followups` list in `status.json > gates.followups` gets both entries and `/devsecops-agency:retro` will surface them.

## Example 3 — blocking red, user waives

| Council       | Gate   | Followups                                               |
| ------------- | ------ | ------------------------------------------------------- |
| research      | green  | 0                                                       |
| product       | green  | 0                                                       |
| architecture  | green  | 0                                                       |
| security      | red    | High STRIDE item with partial mitigation                |
| execution     | green  | 0                                                       |
| quality       | green  | 0                                                       |
| devops        | green  | 0                                                       |
| docs          | green  | 0                                                       |
| legal         | green  | 0                                                       |

Security is blocking. CEO cannot waive alone. Flow:

1. CEO writes `inbox.json` entry: `"security-red-auth-rate-limit"` with options (fix now / fix in v1.1 with feature flag / ship with explicit acceptance).
2. User picks "fix in v1.1 with feature flag."
3. CEO writes `waiver` entry to `chat.jsonl`:
   ```json
   {"ts":"<iso>","scope":"board","from":"ceo","to":"security-lead","type":"waiver","gate":"red","reason":"user accepted: ship behind flag, fix in v1.1","waivedBy":"user","inboxItem":"security-red-auth-rate-limit"}
   ```
4. Aggregator treats the waived red as yellow and appends a `followups` entry with `severity: "high"` and `state: "open"`.
5. Rule 3 applies → **project gate: `yellow`**.

If the user had rejected the waiver, the project would ship as `red` or (more likely) the CEO would loop back to security-lead for fix attempt 2.

## Example 4 — n/a and skipped council

| Council       | Gate   | Note                                                    |
| ------------- | ------ | ------------------------------------------------------- |
| research      | green  |                                                         |
| product       | green  |                                                         |
| architecture  | green  |                                                         |
| security      | green  |                                                         |
| execution     | green  |                                                         |
| quality       | yellow | one a11y medium with ticket                             |
| devops        | green  |                                                         |
| docs          | n/a    | internal-only utility; user opted out of public docs    |
| legal         | n/a    | no third-party dependencies; no user data               |

n/a rows are skipped. Remaining: 6 green + 1 yellow.

Rule 3 → **project gate: `yellow`**. `byCouncil.docs` and `byCouncil.legal` record `"n/a"` in `status.json` and the command-center renders them grey (not green).

## Fix-loop supersession

If a Chief re-reports for the same (council, phase):

```
# Attempt 1 at 14:02
{"ts":"2026-04-20T14:02:00Z","from":"security-lead","phase":"verify","type":"report","gate":"red", ...}

# Fix loop at 14:38
{"ts":"2026-04-20T14:38:00Z","from":"security-lead","phase":"verify","type":"report","gate":"yellow", ...}
```

Both rows stay in `chat.jsonl` (append-only is sacred). The aggregator uses the latest by timestamp per `(council, phase)` — here the yellow. The `metrics.fixLoops` counter increments by 1.

## Anti-patterns

- **Averaging colors.** There is no arithmetic mean. Use the worst-matching rule, not a sum.
- **Hiding a red.** If a Chief wants `yellow` but the matrix says `red`, it is `red`. Waive it explicitly or fix it.
- **Emitting yellow with empty `followups`.** Yellow without a documented ticket is a bug in the Chief's report. Bounce it back.
- **Skipping a council without an `n/a` entry.** Every council must emit one report per phase it's in scope for, even if just `n/a` with a reason.
