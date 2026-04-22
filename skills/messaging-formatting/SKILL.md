---
name: messaging-formatting
description: Format messages for the delivery surface — Slack mrkdwn vs. Discord vs. Microsoft Teams vs. plain Markdown vs. email. Use when any agency specialist is about to post to a messaging platform (Slack, Discord, Teams) — status-writer, incident-comms, stakeholder-update, daily-briefing, release-announcement, standup, or any agent that writes a message a human will read inside a chat client. Blocks the "pasted CommonMark into Slack looks broken" class of bug.
version: 0.3.6
lineage: MIT-licensed content originally from qwibitai/nanoclaw@v1.2.53 (container/skills/slack-formatting/SKILL.md, © 2026 Gavriel). Rewritten and generalized for DevSecOps-Agency v0.3.6 — added CommonMark↔mrkdwn delta table, Discord/Teams/email variants, and agency cadence. See LICENSE.
---

# messaging-formatting — write for the surface, not the source

A CommonMark-shaped message will render broken in Slack. A Slack mrkdwn message will render garbled in Discord. A message written for a chat client will look wrong in an email digest. Different surfaces parse different dialects.

This skill makes it cheap to pick the right one. Before any `send_message` / `slack post` / `teams post` / `discord webhook` / `mailto` call, detect the target surface, then format for it — not for GitHub-flavored Markdown.

## Detection — run this first

Pick the surface from, in priority order:

1. **Explicit parameter.** The caller passed `surface: slack|discord|teams|email|commonmark`. Use it.
2. **Channel / JID / URL shape.**
   - Slack: JID or channel starts with `slack_`, `C0` (channel id), `U0` (user id), `D0` (DM), `G0` (MPIM); webhook host is `hooks.slack.com`.
   - Discord: host is `discord.com` or `discordapp.com`, webhook contains `/api/webhooks/…`.
   - Microsoft Teams: host is `*.webhook.office.com` or an MS Graph endpoint; channel id contains `@thread.v2`.
   - Email: recipient contains `@` and no colon-prefixed service id; SMTP / SES / SendGrid on the send path.
3. **Folder name fallback.** Group folder starts with `slack_`, `discord_`, `teams_`, `email_`.
4. **Default.** CommonMark (what GitHub, most docs, and most agency `.md` files use).

Write the detected value to your working memory as `surface: <name>` before composing. If you can't detect, **ask the caller** — silently defaulting to CommonMark inside a Slack post is the failure mode this skill exists to prevent.

## Surface dialects — the only rules you need

### Slack (mrkdwn)

| Construct      | Correct                         | Common mistake (renders wrong)   |
| -------------- | ------------------------------- | -------------------------------- |
| Bold           | `*text*`                        | `**text**` (renders as literal)  |
| Italic         | `_text_`                        | `*text*` (that's bold)           |
| Strikethrough  | `~text~`                        | `~~text~~`                       |
| Inline code    | `` `text` ``                    | same                             |
| Code block     | ` ```text``` ` (no language)    | triple-backtick with `lang` tag  |
| Link           | `<https://x|label>`             | `[label](https://x)`             |
| Auto-link      | `<https://x>`                   | bare URL works but may truncate  |
| User mention   | `<@U01234567>`                  | `@name` (does not notify)        |
| Channel ref    | `<#C01234567>` or `<#C…\|name>` | `#channel`                       |
| Here / channel | `<!here>`, `<!channel>`         | `@here`                          |
| Bullet         | `• item` or `- item`            | `1. item` (numbered lists fail)  |
| Quote          | `> text`                        | same                             |
| Heading        | **none** — use `*bold line*`    | `## Heading` (prints literally)  |
| Table          | **none** — use aligned code block | `\| a \| b \|` (prints literally) |
| Horizontal rule | **none** — use a blank line    | `---` (prints literally)         |
| Emoji          | `:white_check_mark:` shortcodes | Unicode also works but shortcodes render consistently |

**Maximum message length:** 40,000 chars; blocks API capped at 50 blocks; attachment fallback text at 3,000 chars. If you are about to exceed, split or thread instead of truncating.

### Discord

Discord speaks a superset of CommonMark — so CommonMark mostly works, with exceptions:

| Construct     | Discord                                       | Note |
| ------------- | --------------------------------------------- | ---- |
| Bold          | `**text**`                                    | (unlike Slack) |
| Italic        | `*text*` or `_text_`                          | |
| Underline     | `__text__`                                    | (not available in Slack) |
| Strikethrough | `~~text~~`                                    | |
| Inline code   | `` `text` ``                                  | |
| Code block    | ` ```lang\ntext\n``` `                        | language tag DOES work |
| Link          | `[label](https://x)`                          | (opposite of Slack) |
| User mention  | `<@123456789012345678>`                       | Discord user IDs are numeric |
| Role mention  | `<@&123456789012345678>`                      | |
| Channel ref   | `<#123456789012345678>`                       | |
| Spoiler       | `\|\|text\|\|`                                    | |
| Bullet        | `- item`                                      | numbered `1.` also works |
| Heading       | `# text`, `## text`, `### text`               | renders as visual headings |
| Table         | **none** — use code block                     | |
| Emoji         | `:name:` (server emoji) or Unicode            | custom emoji use `<:name:id>` |

**Maximum message length:** 2,000 chars (4,000 for Nitro). Above that, split into multiple messages or use an attached file.

### Microsoft Teams

Teams cards (via Incoming Webhook / MS Graph) accept a subset of Markdown plus Adaptive Cards. For plain `text` fields:

| Construct     | Teams                                         | Note |
| ------------- | --------------------------------------------- | ---- |
| Bold          | `**text**`                                    | |
| Italic        | `*text*` or `_text_`                          | |
| Code block    | ` ```text``` `                                | no language tag |
| Link          | `[label](https://x)`                          | |
| Bullet        | `- item`                                      | |
| Heading       | `# text`                                      | supported in cards |
| User mention  | `<at>Display Name</at>`                       | requires mentions array in payload |
| Line break    | **double space** + newline, or `<br/>`        | single newline ignored in some card types |

Teams strips most HTML except the allowed subset (`<b>`, `<i>`, `<s>`, `<a>`, `<br/>`, `<at>`, `<code>`, `<pre>`). Pictures and tables need Adaptive Cards — don't try to fake them with Markdown.

**Maximum message length:** 25 KB per card body.

### Email (HTML / plain)

Emails render in roughly 30 different clients with inconsistent Markdown support. Rules that work everywhere:

- Compose in plain text OR HTML. Don't mix Markdown and HTML — most clients will show the raw `*bold*`.
- Subject line ≤ 78 chars (RFC 5322 soft limit) and should stand alone — assume it will be the only thing the reader sees in their inbox preview.
- In HTML bodies, keep tables inline-styled — Outlook strips `<style>` blocks.
- No emoji shortcodes — only Unicode (✅) or PNG images.
- Preserve original line wrapping — don't auto-wrap to 72 cols, modern clients reflow.

### CommonMark (the fallback / docs / GitHub / agency `.md` files)

Standard GitHub-Flavored Markdown. This is what everything else in the agency (`_vision/`, `AGENTS.md`, SKILL bodies) uses. `**bold**`, `[label](url)`, `` ```lang\ncode\n``` ``, `- bullet`, `| table |`, `## Heading`. Nothing surprising.

## Composition pattern

```
1. detect surface (explicit ▶ id-shape ▶ folder ▶ ask) → surface = slack|discord|teams|email|commonmark
2. write the SEMANTIC message first (plain sentences)
3. apply the dialect table above to add emphasis, links, mentions, code
4. check length limit for the surface; split/thread if over
5. send
```

Do not compose in CommonMark and then "convert" — the conversions lose information (Slack has no heading primitive, Discord has no underline equivalent in Slack, email has no `:rocket:`). Compose in the target dialect from the start.

## Worked examples

### Example 1 — status update, Slack

```
*Release v0.3.6 — Green*

_April 22, 2026_

• *Packaged:* devsecops-agency-0.3.6.plugin (SHA-256 pending)
• *Shipped:* <https://github.com/…/releases/tag/v0.3.6|GitHub Release v0.3.6>
• *Next:* user verification, then v0.3.7 planning

:white_check_mark: All gates green | cc <!here>
```

### Example 2 — same status update, Discord

```
**Release v0.3.6 — Green**

*April 22, 2026*

- **Packaged:** `devsecops-agency-0.3.6.plugin` (SHA-256 pending)
- **Shipped:** [GitHub Release v0.3.6](https://github.com/…/releases/tag/v0.3.6)
- **Next:** user verification, then v0.3.7 planning

✅ All gates green
```

### Example 3 — same status update, email plain-text

```
Subject: DevSecOps-Agency v0.3.6 released (all gates green)

v0.3.6 is out.

- Packaged: devsecops-agency-0.3.6.plugin
- Release: https://github.com/…/releases/tag/v0.3.6
- Next: user verification, then v0.3.7 planning

All gates green.
```

## Anti-patterns that cost the most debugging time

1. **Pasting CommonMark into Slack.** `**bold**` prints as `**bold**`. `[label](url)` prints literally. Tables print as pipe-soup. Always re-format.
2. **Numbered lists in Slack.** Slack parses numbered lists inconsistently. Use bullets (`•` or `-`) or write `1. …` as literal text inside a bullet: `• 1. First item`.
3. **Bare @name mentions.** Do not notify. Always use `<@USERID>` for Slack, `<@numeric_id>` for Discord, `<at>Name</at>` + payload for Teams.
4. **Headings in Slack.** There is no heading primitive. Use `*bold line*` on its own line.
5. **Tables anywhere except CommonMark.** Fall back to a code block with aligned columns.
6. **Code block language tags in Slack.** ` ```python ` emits literal `python` before the block. Drop the lang tag for Slack; keep it for Discord and CommonMark.
7. **Long messages without splitting.** Slack hard-caps at 40,000; Discord at 2,000. Over the limit fails silently on webhooks and errors on Web API calls.
8. **Unescaped `<` or `&` in Slack.** Slack interprets `<…>` as a link/mention. If you need literal angle brackets, use `&lt;` / `&gt;`; for ampersand, `&amp;`.

## Integration points

- `status-writer`, `incident-comms`, `standup-writer`, `stakeholder-update`, `daily-briefing`, `release-announcement` — any specialist that ends a shift by posting to a human channel.
- `board-meeting`, `council-meeting` — meeting minutes posted back to the room.
- `notify` — push-notify on completion; picks surface from the channel descriptor.
- `escalate`, `ladder` — escalation messages need correct at-mentions or they silently fail to notify.

Any agent that writes a message a human will read in a chat client should either (a) invoke this skill and pass `surface=…`, or (b) receive pre-formatted text from a caller that already did.

## What this skill never does

- Does not write the *content* of the message — that's the calling specialist's job. It owns dialect only.
- Does not strip formatting from an incoming user message — that's a separate concern (sanitization lives in `injection-defense`).
- Does not attempt to render emoji, images, or attachments — those go through the sending MCP / webhook with a structured payload.
- Does not "auto-convert" CommonMark → Slack. Compose in the dialect.

## License

Lineage: MIT-licensed source content from `qwibitai/nanoclaw@v1.2.53` (`container/skills/slack-formatting/SKILL.md`). © 2026 Gavriel. Rewritten and extended in this repo under DevSecOps-Agency's license. See `LICENSES/MIT-nanoclaw.txt` at the repo root.
