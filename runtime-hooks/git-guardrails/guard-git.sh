#!/usr/bin/env bash
# guard-git.sh — block dangerous git operations before they execute.
#
# Backs the v0.6.1 git-guardrails runtime hook (the 8th hook in the Agency).
# Trigger: preToolUse on any Bash invocation matching `^git ` (Claude Code's pattern format).
# Mode: block (default — exit 2 = refuse) or warn (log to stderr, exit 0).
#
# The blocked patterns map to operations that destroy work or that should require
# explicit User approval per the Agency's USER-ONLY actions (Constitution §2.2 includes
# "publish externally" — `git push` is the operational form of that).
#
# Bypass attempts file a `runtime-hook-bypass` ADR per TRUST.md §2.7. Hooks are non-optional.

set -euo pipefail

GUARD_MODE="${GUARD_MODE:-block}"

# Read tool input as JSON from stdin (Claude Code preToolUse hook contract).
INPUT="$(cat || true)"

# Extract the actual command. Use python (always available in our sandbox) rather
# than jq (less ubiquitous on user machines).
COMMAND="$(echo "$INPUT" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(d.get('tool_input', {}).get('command', ''))
except Exception:
    pass
" 2>/dev/null || true)"

# If we couldn't parse the command, do not block — fail open.
# A separate hook (governance-audit) catches malformed tool calls.
if [[ -z "$COMMAND" ]]; then
  exit 0
fi

# Pattern list. Each pattern is checked against the full command string with
# extended-regex match. The patterns cover four categories:
#
# 1. Force-push and history-rewrite operations (destroy remote history)
# 2. Hard reset operations (destroy uncommitted local work)
# 3. Working-tree wipes (destroy untracked files; not recoverable from reflog)
# 4. Branch deletions and force-restores (destroy branches and unstaged changes)
#
# Patterns are intentionally broad — better to block a benign variant than miss a
# destructive one. Sovereign can run blocked operations directly outside the agent.

DANGEROUS_PATTERNS=(
  # Force pushes (any form)
  '\bgit push.*--force\b'
  '\bgit push.*--force-with-lease\b'
  '\bgit push.*-f\b'
  '\bgit push --mirror\b'

  # Plain push (USER-ONLY per Constitution §2.2 "publish externally" — explicit
  # User approval required; agent can prep the commit but not the push)
  '^git push( |$)'
  '^git push origin'
  '^git push --tags'

  # Hard reset (destroys uncommitted work; reflog can recover commits but not
  # working-tree changes)
  '\bgit reset --hard\b'
  '\bgit reset --keep\b'

  # Working-tree wipes (NOT recoverable; -f means force, -d means include dirs)
  '\bgit clean -f\b'
  '\bgit clean -fd\b'
  '\bgit clean -fdx\b'
  '\bgit clean -dx\b'

  # Branch deletion (force form bypasses merge check)
  '\bgit branch -D\b'
  '\bgit branch --delete --force\b'

  # Force restore / checkout that wipes uncommitted changes
  '\bgit checkout \. \b'
  '\bgit checkout \.$'
  '\bgit restore \. \b'
  '\bgit restore \.$'
  '\bgit restore --staged --worktree\b'

  # Filter-branch / filter-repo (history rewrite — destroys other contributors'
  # commit refs)
  '\bgit filter-branch\b'
  '\bgit filter-repo\b'

  # GC with aggressive prune (can destroy unreferenced objects)
  '\bgit gc --aggressive --prune=now\b'
  '\bgit reflog expire --expire=now --all\b'
)

# Walk patterns; first match wins.
for pattern in "${DANGEROUS_PATTERNS[@]}"; do
  if echo "$COMMAND" | grep -qE -- "$pattern"; then
    MSG="git-guardrails: BLOCKED — '$COMMAND' matches dangerous pattern '$pattern'."
    REASON="This operation can destroy work that is not recoverable from git reflog, or it requires User-only authorization per Constitution §2.2 (publish externally). The Sovereign can run this operation directly outside the agent if intended."
    echo "$MSG" >&2
    echo "$REASON" >&2
    if [[ "$GUARD_MODE" == "block" ]]; then
      # Exit code 2 = the Claude Code preToolUse contract for "refuse this tool call"
      exit 2
    else
      # warn mode: log + allow
      exit 0
    fi
  fi
done

exit 0
