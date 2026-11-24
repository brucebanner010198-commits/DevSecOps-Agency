#!/usr/bin/env bash
# Start a Claude Code session as the agency's CEO agent.
#
# Starting as the agent (not only through the /devsecops-agency:ceo skill)
# is what makes the CEO's role card bind: its tool list and model apply to
# the main session, and hooks see agent_type "devsecops-agency:ceo" on its
# calls. A plugin cannot set this default itself. The alternatives are this
# launcher, `claude --agent devsecops-agency:ceo`, or a project setting:
#   .claude/settings.json  ->  { "agent": "devsecops-agency:ceo" }
set -euo pipefail
exec claude --agent devsecops-agency:ceo "$@"
