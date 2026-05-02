---
name: 'Git Guardrails'
description: 'Blocks dangerous git operations (force-push, hard reset, working-tree wipes, branch deletes, history rewrites) before they execute. The 8th runtime hook in the Agency, added v0.6.1.'
tags: ['git', 'safety', 'preToolUse', 'sre', 'csre']
---

# Git Guardrails Hook

The 8th runtime hook in the Agency. Fires on `preToolUse` for any Bash invocation matching `^git ` and refuses (exit 2) when the command matches a dangerous pattern.

## Why this hook exists

The Agency's existing runtime hooks (secrets-scanner, tool-guardian, governance-audit, dependency-license-checker, session-logger, commit-gate, cost-gate) cover code-quality, secrets, governance, and cost. None of them block destructive git operations. A force-push, hard reset, or working-tree wipe can destroy work in ways that are not recoverable from `git reflog`.

`git push` specifically is the operational form of Constitution §2.2's "publish externally" USER-ONLY action — the Agency can prep commits, but the publish is the User's call.

## What gets blocked

Patterns are intentionally broad — better to block a benign variant than miss a destructive one. The Sovereign can run blocked operations directly outside the agent if intended.

| Category | Pattern examples | Why blocked |
|---|---|---|
| **Force pushes** | `git push --force`, `git push -f`, `git push --force-with-lease`, `git push --mirror` | Destroys remote history; can lose other contributors' commits |
| **All pushes** | `git push`, `git push origin`, `git push --tags` | USER-ONLY per Constitution §2.2 (publish externally) — Sovereign decides |
| **Hard resets** | `git reset --hard`, `git reset --keep` | Destroys uncommitted work; reflog recovers commits but not working-tree changes |
| **Working-tree wipes** | `git clean -f`, `git clean -fd`, `git clean -fdx`, `git clean -dx` | Untracked files NOT recoverable from reflog |
| **Branch force-deletes** | `git branch -D`, `git branch --delete --force` | Bypasses merge-check |
| **Force restores** | `git checkout .`, `git restore .`, `git restore --staged --worktree` | Wipes uncommitted changes |
| **History rewrites** | `git filter-branch`, `git filter-repo` | Destroys other contributors' commit refs |
| **Aggressive GC** | `git gc --aggressive --prune=now`, `git reflog expire --expire=now --all` | Destroys unreferenced objects, breaks reflog recovery |

## Configuration

| Variable | Default | Notes |
|---|---|---|
| `GUARD_MODE` | `block` | `block` (exit 2 — refuse the tool call) or `warn` (log to stderr, exit 0) |

## How it composes with the existing 7 hooks

| Hook | Trigger | This hook adds |
|---|---|---|
| secrets-scanner | sessionEnd | Catches raw secrets in modified files |
| tool-guardian | preToolUse | Vets new MCP tool adoption |
| governance-audit | sessionStart / sessionEnd / preToolUse | Append-only invariant + governance contracts |
| dependency-license-checker | preToolUse | Catches incompatible OSS licenses on new deps |
| session-logger | sessionStart / sessionEnd / preToolUse | Persists session state |
| commit-gate | preToolUse | Blocks commits that bypass other gates |
| cost-gate (v0.5.6) | preToolUse + scheduled | Cost label compliance + spike detection |
| **git-guardrails (v0.6.1)** | preToolUse | Destructive git ops + USER-ONLY push enforcement |

Hook chain order is enforced by the runtime — preToolUse hooks run in the order their `matchTool`/`matchPattern` directives match. Because `git-guardrails` matches `^git ` specifically, it fires before `commit-gate` (which matches a broader Bash pattern), so a destructive git command is blocked before commit-gate even sees it.

## Bypass posture

Bypass attempts (e.g. invoking the destructive command via `bash -c "git push origin main"` to dodge the matcher, or via `eval` evaluation, or via writing the command to a file and sourcing it) file a `runtime-hook-bypass` ADR per `TRUST.md` §2.7. The hook itself does not detect those bypasses — `governance-audit` does, in its session-end pass. This hook's job is to catch the obvious-and-honest cases at preToolUse time.

If the Sovereign wants to genuinely run a destructive command, the right path is to leave the agent session, run the command directly in their own terminal, and then resume the agent session. This is by design — destructive operations are the Sovereign's call, not the agent's.

## Local testing

```bash
# Should BLOCK (exit 2):
echo '{"tool_input":{"command":"git push origin main"}}' \
  | ./runtime-hooks/git-guardrails/guard-git.sh
echo "exit: $?"

echo '{"tool_input":{"command":"git reset --hard HEAD~3"}}' \
  | ./runtime-hooks/git-guardrails/guard-git.sh
echo "exit: $?"

# Should ALLOW (exit 0):
echo '{"tool_input":{"command":"git status"}}' \
  | ./runtime-hooks/git-guardrails/guard-git.sh
echo "exit: $?"

echo '{"tool_input":{"command":"git log --oneline -10"}}' \
  | ./runtime-hooks/git-guardrails/guard-git.sh
echo "exit: $?"
```

## Customization

If a project has a legitimate need for one of the blocked patterns (e.g. a release-bot that genuinely owns force-pushes to a release branch), the right path is:

1. File a `git-guardrails-exception-<reason>` ADR explaining the legitimate need
2. Add an exception line to the project's local copy of this hook (do not modify the central hook)
3. Have CSRE + CRT countersign the exception ADR

Do NOT remove patterns from the central hook without an Agency-wide ADR.

## Provenance

The dangerous-git-commands enumeration is common engineering knowledge — every git tutorial covers some subset of it. The Agency's specific set of patterns + the USER-ONLY-publish framing for `git push` is original to v0.6.1. The hook script itself is written in the Agency's bash + python style (reusing the same JSON-parsing approach as `runtime-hooks/cost-gate/spike-detector.sh`).

The `mattpocock/skills` repository (MIT, 2026) is the curator that surfaced the named slash-command framing for git-blocking-as-a-hook to the Agency in the v0.6.1 cycle.
