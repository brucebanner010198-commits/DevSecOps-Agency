# Start a Claude Code session as the agency's CEO agent (see scripts/agency.sh).
# Alternative: a project .claude/settings.json with { "agent": "devsecops-agency:ceo" }.
& claude --agent devsecops-agency:ceo @args
exit $LASTEXITCODE
