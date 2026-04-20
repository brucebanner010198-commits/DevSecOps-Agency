# Escalation Rules

Only return to the human when one of these triggers fires. Everything else — decide, document, move on.

## Triggers (must escalate)

1. **Missing credential** — an MCP/connector is required (e.g., GitHub, cloud provider) and not connected.
2. **Critical unmitigatable security risk** — `threat-modeler` or `code-auditor` flags a Critical risk and no mitigation is viable within the chosen stack.
3. **Irreversible external action** — publishing to a real registry, sending real email, writing to a real production database, creating a public repo.
4. **True intent ambiguity** — two interpretations of the idea would produce materially different products (not just stylistic differences).
5. **Hard budget cap** — chosen design requires paid infra the user hasn't opted into.
6. **Second fix loop failed** — same stage has gone around twice and still fails exit criteria.

## Triggers (must NOT escalate)

- Color / naming / copy preferences → pick sensible defaults
- Which specific library inside the agreed stack → pick the mainstream one
- Trade-offs between two equally valid patterns → pick, note the alternative in a comment
- Minor test failures with an obvious fix → fix them
- Missing "nice to have" that wasn't in the acceptance criteria → skip, log in `follow-ups.md`

## Inbox format

`inbox.json` in the project folder:

```json
{
  "open": [
    {
      "id": "q1",
      "raisedBy": "security-lead",
      "stage": "security",
      "question": "Threat model identifies risk of credential stuffing. Do you want rate-limiting + CAPTCHA (adds a dependency) or just rate-limiting?",
      "options": ["rate-limit only", "rate-limit + CAPTCHA"],
      "blocking": true,
      "raisedAt": "<iso>"
    }
  ],
  "answered": []
}
```

When an escalation is raised:

1. Write the question to `inbox.json > open`.
2. Append a `chat.jsonl` entry with type `escalate`.
3. Update `status.json.blockers` with the question id.
4. Surface the question via AskUserQuestion.
5. On answer, move the entry to `answered`, clear the blocker, append a `resume` chat entry, continue.
