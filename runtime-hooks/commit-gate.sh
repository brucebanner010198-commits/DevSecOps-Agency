#!/bin/bash

# commit-gate.sh — locked-down replacement for awesome-copilot's session-auto-commit.
#
# Differences from the upstream auto-commit hook:
#   - Stages ONLY files listed in $COMMIT_FILES (no `git add -A`)
#   - NEVER passes --no-verify (pre-commit hooks must run)
#   - NEVER auto-pushes (push is the CEO's decision, gated on board-meeting signal)
#   - Refuses to commit if secrets-scanner, tool-guardian, or governance-audit
#     have a "threat" line in the latest session log
#
# Environment variables:
#   COMMIT_FILES      - Space-separated list of explicitly-touched file paths (required)
#   COMMIT_MESSAGE    - Full commit message (required)
#   COMMIT_GATE_LOG   - Directory for gate logs (default: .github/logs/copilot/commit-gate)
#   SKIP_COMMIT_GATE  - "true" to disable (for recovery only, logs a WAIVER line)
#
# Exits:
#   0 — commit created (or skipped cleanly)
#   2 — blocked by another hook's findings
#   3 — missing required env var
#   1 — unexpected error

set -euo pipefail

LOG_DIR="${COMMIT_GATE_LOG:-.github/logs/copilot/commit-gate}"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/gate.log"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

log_line() {
  printf '{"timestamp":"%s","event":"%s","detail":%s}\n' "$TIMESTAMP" "$1" "$2" >> "$LOG_FILE"
}

if [[ "${SKIP_COMMIT_GATE:-}" == "true" ]]; then
  log_line "waiver" "\"SKIP_COMMIT_GATE=true; commit bypassed — record an ADR\""
  exit 0
fi

if [[ -z "${COMMIT_FILES:-}" ]]; then
  log_line "error" "\"COMMIT_FILES unset; refusing to stage anything\""
  exit 3
fi

if [[ -z "${COMMIT_MESSAGE:-}" ]]; then
  log_line "error" "\"COMMIT_MESSAGE unset\""
  exit 3
fi

if ! git rev-parse --is-inside-work-tree &>/dev/null; then
  log_line "noop" "\"not in a git repo\""
  exit 0
fi

# Gate on prior hook findings in this session
for hook_log in \
    .github/logs/copilot/secrets/*.log \
    .github/logs/copilot/tool-guardian/guard.log \
    .github/logs/copilot/governance-audit/audit.log; do
  [[ -f "$hook_log" ]] || continue
  if grep -q '"threat_detected"\|"blocked"\|"critical"' "$hook_log" 2>/dev/null; then
    log_line "blocked" "\"threat-level finding in $hook_log; CAO must clear\""
    echo "commit-gate: blocked — prior hook recorded a threat in $hook_log" >&2
    exit 2
  fi
done

# Stage ONLY the explicit list
for f in $COMMIT_FILES; do
  if [[ ! -e "$f" && ! "$f" =~ \*|\? ]]; then
    log_line "warn" "\"missing path: $f\""
    continue
  fi
  git add -- "$f"
done

# No --no-verify. Pre-commit hooks MUST run.
if git commit -m "$COMMIT_MESSAGE"; then
  sha=$(git rev-parse HEAD)
  log_line "committed" "\"$sha\""
else
  log_line "commit_failed" "\"see stderr\""
  exit 1
fi

# Explicitly do NOT push. Push is a CEO-gated action.
exit 0
