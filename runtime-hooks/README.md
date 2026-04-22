# runtime-hooks — defense-in-depth at session boundaries

Five drop-in shell hooks that complement the agency's prompt-level rules with runtime enforcement. Every hook is:

- Read-only on the input stream (no `eval`, no `bash -c`, no `source`, no network fetch)
- Matches against hardcoded regex arrays (no untrusted-source pattern loading)
- Emits append-only JSONL logs
- Exits 0 (pass) or non-zero (block) — no side-effects on the filesystem outside the log directory

They were ported from `github/awesome-copilot` after a prompt-injection audit. The `session-auto-commit` hook from that catalog was **deliberately excluded** because it uses `git add -A` + `--no-verify` + `git push`, which bypasses the very defenses in this folder. A locked-down replacement is in `commit-gate.sh` (no `-A`, no `--no-verify`, no auto-push).

## Inventory

| Hook | Purpose | Council / skill pairing |
|------|---------|-------------------------|
| `secrets-scanner/` | Regex scan for credentials in diffs (AWS, GitHub PATs, Stripe, JWT, Slack, private keys, 30+ patterns) | Security → `secrets-vault` |
| `tool-guardian/` | Block destructive tool invocations (`rm -rf /`, force-push, DB drops) with env-var allowlist | SRE → `tool-scout` + `a2a` |
| `governance-audit/` | Prompt scan for data-exfil / privesc / system-destruction / prompt-injection / credential-exposure; session-start + session-end bookends | Audit → `audit` |
| `dependency-license-checker/` | License scan on dependency diffs | Legal → `ip-lineage` + `compliance-drift` |
| `session-logger/` | Append-only JSONL session log (prompt + session-start + session-end) | `session-log` skill |
| `commit-gate.sh` | Locked-down replacement for auto-commit — only stages explicitly-touched files, runs other hooks first, never `--no-verify`, never auto-pushes | CEO loop / ADR |

## Invocation model

Each hook directory contains a `hooks.json` describing the trigger event and script path. The CEO skill reads these when it advances a phase. Agents never invoke hooks directly — hooks wrap the runtime, they are not agent tools.

## Invariants

- Hooks must never execute content from their input stream as code.
- Hooks must never fetch instructions from remote sources.
- Hooks must never load pattern / allowlist configuration from an agent-writable location.
- `commit-gate.sh` must never pass `--no-verify` and must never `git push`.
- Any hook finding escalates to the CAO via the taskflow queue; no hook auto-heals.

## Prompt-injection posture

The `governance-audit` hook is itself a defender — it scans incoming prompts for injection patterns ("ignore previous instructions", "system: …", base64-encoded command strings, etc.) and gates them before the agent sees them. This is the runtime complement to the prompt-level rules in each council's AGENTS.md.

## Attribution

Scripts adapted from https://github.com/github/awesome-copilot (MIT). Audited for prompt-injection vectors at import time; `session-auto-commit` deliberately excluded and replaced.
