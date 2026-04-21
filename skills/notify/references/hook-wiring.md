# hook-wiring.md — notify transport wiring

How the notify skill reaches the user across the surfaces the plugin can be running in.

## Surface priority

1. Cowork `Stop` / `SubagentStop` hooks.
2. Claude Code desktop push settings.
3. Terminal fallback: single `[notify] ...` line at the top of the CEO's final reply.

## 1. Cowork hooks

Cowork exposes `Stop` and `SubagentStop` hook surfaces. Wire them in the plugin manifest under `.claude-plugin/plugin.json` or `settings.json` when packaging:

```json
{
  "hooks": {
    "SubagentStop": [
      {
        "match": "ceo",
        "notify": {
          "channel": "cowork",
          "template": "[notify] {event} · {slug} · {note}"
        }
      }
    ],
    "Stop": [
      {
        "notify": {
          "channel": "cowork",
          "template": "[notify] session closed · {slug}"
        }
      }
    ]
  }
}
```

The actual hook surface in the user's environment is read from `env.COWORK_HOOK_CHANNEL` if set, or defaults to the CEO's final reply.

## 2. Desktop push (Claude Code)

If the user has desktop push configured and the environment exposes `CLAUDE_CODE_DESKTOP_NOTIFY=1`, the notify skill issues a single shell command:

```bash
# only invoked by an execution-tool-bearing agent; notify itself does not hold Bash.
# the CEO forwards the payload to devops-lead, which has Bash, or uses a local `osascript` / `notify-send` wrapper configured by the user.
```

Desktop push is best-effort. If the command fails or the env var is unset, fall through to the terminal fallback.

## 3. Terminal fallback

Always works. The CEO's final reply to the user starts with `[notify] <event> · <slug> · <note>` followed by a blank line and then the normal closing summary.

## Security note

- Never include secrets, tokens, or PII in the `note`.
- Never send the full artifact content — only the relative path and line number.
- If an event would require the notify message itself to contain PII (e.g. "leaked email X in logs"), rewrite the note to a pointer: `"PII leak in security/pentest-report.md:42 — see file"`.
