#!/usr/bin/env bash
# labels-check.sh — block cloud resource provisioning that omits the four required labels.
#
# Backs COST-AWARENESS.md §2.1 ("100 % labeled resources").
# Required labels: env, team, app, project (configurable via REQUIRED_LABELS env var).
#
# Trigger: preToolUse on Bash invocations matching gcloud / aws / az / terraform-apply.
# Mode: warn (default — log to stderr, exit 0) or block (exit non-zero → tool call refused).
#
# Implementation status (v0.5.6): scaffolding. The regex matchers below catch the
# obvious "no --labels flag at all" case for gcloud, plus the "no tags = " for
# Terraform plan output. They do NOT validate that all four required keys are present
# — that requires parsing the actual command tokens. Full implementation tracked in
# the v0.6.0 wave (per CHANGELOG.md).

set -euo pipefail

GATE_MODE="${GATE_MODE:-warn}"
REQUIRED_LABELS="${REQUIRED_LABELS:-env,team,app,project}"
TOOL_INPUT="${1:-}"

# Read tool input from stdin if not supplied as argument.
if [[ -z "$TOOL_INPUT" ]]; then
  TOOL_INPUT="$(cat || true)"
fi

# Bail out fast on commands that don't provision resources.
if ! echo "$TOOL_INPUT" | grep -qE '(gcloud (compute|container|run|sql|alloydb|storage)|aws (ec2|rds|s3 mb|eks)|az (vm|aks|sql|storage)|terraform apply)'; then
  exit 0
fi

# Heuristic 1: gcloud commands without --labels=
if echo "$TOOL_INPUT" | grep -qE '^gcloud (compute|container|run|sql|alloydb)' \
   && ! echo "$TOOL_INPUT" | grep -qE -- '--labels='; then
  echo "cost-gate/labels-check: gcloud command provisions a resource without --labels= (required: $REQUIRED_LABELS) per COST-AWARENESS.md §2.1" >&2
  if [[ "$GATE_MODE" == "block" ]]; then
    echo "cost-gate/labels-check: refused (mode=block)" >&2
    exit 1
  fi
fi

# Heuristic 2: aws commands without --tags
if echo "$TOOL_INPUT" | grep -qE '^aws (ec2 run-instances|rds create-db-instance|s3 mb|eks create-cluster)' \
   && ! echo "$TOOL_INPUT" | grep -qE -- '--tags'; then
  echo "cost-gate/labels-check: aws command provisions a resource without --tags (required: $REQUIRED_LABELS) per COST-AWARENESS.md §2.1" >&2
  if [[ "$GATE_MODE" == "block" ]]; then
    exit 1
  fi
fi

# Heuristic 3: terraform apply with no labels block in plan
if echo "$TOOL_INPUT" | grep -qE '^terraform apply'; then
  if ! grep -qE '(labels|tags|default_labels|default_tags)\s*=' "$(pwd)"/*.tf 2>/dev/null \
     && ! grep -qE '(labels|tags|default_labels|default_tags)\s*=' "$(pwd)"/**/*.tf 2>/dev/null; then
    echo "cost-gate/labels-check: terraform apply but no labels/tags assignment found in *.tf (required: $REQUIRED_LABELS) per COST-AWARENESS.md §2.1" >&2
    if [[ "$GATE_MODE" == "block" ]]; then
      exit 1
    fi
  fi
fi

exit 0
