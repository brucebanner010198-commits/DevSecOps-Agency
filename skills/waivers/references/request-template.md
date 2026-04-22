# waivers/references/request-template.md

Exact format for the waiver request. Used in step 2 of `skills/waivers/SKILL.md`.

## Template

```markdown
# Waiver request: <short slug>

- **Finding id:** `<finding-id>`  (red-team row / CAO entry / CEVO report / CISO gate row)
- **Artifact:** `<path to the artifact the red lands on>`
- **Project:** `<project slug>`
- **Originating council:** `<security | evaluation | red-team | audit>`
- **Originating chief:** `<CISO | CEVO | CRT | CAO>`
- **Severity:** `<critical | high | medium>`
- **Requested by:** `<council-lead agent name>`
- **Owner (remediation):** `<agent name>`
- **Expiration:** `YYYY-MM-DD`  (hard calendar date — not "until ship", not "30 days", not "when we can")

## Impact (what the chief said would break)

<one to three bullets, verbatim from the finding where possible>

## Reason to waive

<two to four bullets. Must argue why fixing first would be worse than shipping with the red. Generic "we're in a hurry" is not a valid reason — the request will be denied on procedural grounds.>

## Remediation plan

1. <step>
2. <step>
3. <step>

<Each step concrete enough to verify. The expiry check on YYYY-MM-DD reads this plan and confirms each step's ADR exists.>

## Alternatives considered

- Fix first, delay ship: <cost>
- Revert to prior version: <cost>
- Park at Rung 7: <cost>

<If no alternatives are listed, the request is incomplete.>

## Independence check

- Requesting agent council: `<council>`
- Approving chief council: `<council>`
- User is final approver: yes (this field is boilerplate — if no, the request is invalid)

Confirms proposer ≠ approver (VALUES §3).
```

## Validation rules

The skill fails-fast on any of these:

1. `Expiration:` not a valid ISO date, OR more than 90 days from today, OR earlier than 1 day from today.
2. `Finding id:` not resolvable to a row in the four source ledgers.
3. `Remediation plan:` fewer than 2 steps, OR any step lacks a verb.
4. `Alternatives considered:` missing or empty.
5. `Independence check:` missing or self-approving.
6. The finding is tagged `ASI-class` or `raw-secret` — those are not waivable (see `SKILL.md §Anti-patterns`).

## Short-form for trivial waivers

Waivers covering `medium`-severity findings with < 14 day expiration can use a 5-line short form:

```markdown
# Waiver short-form: <slug>
- finding: <id>  expiration: YYYY-MM-DD
- impact: <one line>
- reason: <one line>
- remediation: <one line>
- owner: <agent>
```

Short-form still routes through the full proposer → reviewer → approver chain; it only compresses the write-up. Critical/high findings always use the full template.
