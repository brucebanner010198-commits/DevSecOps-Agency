---
name: 'Cost Gate'
description: 'Enforces COST-AWARENESS.md §2.1 (label compliance on cloud-resource provisioning) and §2.11 (>50% MoM spend-spike detection with same-day User notification).'
tags: ['cost', 'finops', 'preToolUse', 'scheduled', 'csre']
---

# Cost Gate Hook

Implements the runtime enforcement promised in `COST-AWARENESS.md` v1.0 (v0.5.5). Two scripts:

- **`labels-check.sh`** — wired to `preToolUse` on Bash invocations matching `gcloud|aws|az|terraform apply`. Refuses or warns on cloud-resource provisioning that omits the four required labels (`env`, `team`, `app`, `project`).
- **`spike-detector.sh`** — wired to a daily `scheduled` trigger. Reads cost data, compares current month to previous, and writes a `cost-spike` row to `inbox.json` for any project showing a >50% MoM increase.

## Why this hook exists

Cost discipline without runtime enforcement is theatre. `COST-AWARENESS.md` §2.1 + §2.11 commit the Agency to specific behaviors; this hook is one of the two ways those commitments stay honest (the other is CAO's monthly audit).

Backed by `COST-AWARENESS.md` (v1.0, v0.5.5) and `councils/sre/AGENTS.md` (v0.5.5 cost-discipline invariant).

Owner: **CSRE**. CAO countersigns at the quarterly cost scorecard publish.

## Configuration

| Variable | Default | Notes |
|---|---|---|
| `GATE_MODE` | `warn` | `warn` (log to stderr, exit 0) or `block` (exit non-zero, refuse the tool call). |
| `REQUIRED_LABELS` | `env,team,app,project` | Comma-separated list of labels every cloud resource MUST carry. |
| `COST_DATA_SOURCE` | `manual-csv` | `gcp-bq` / `aws-cur` / `azure-cme` / `manual-csv`. The cloud-native adapters are scaffolding in v0.5.6 — full implementation lands in v0.6.0. |
| `COST_DATA_PATH` | `_vision/cost/manual-billing.csv` | Path used by `manual-csv` mode. CSV with header `project,month,spend_usd`. |
| `SPIKE_THRESHOLD_PCT` | `50` | MoM percentage increase that triggers a spike row. |
| `WINDOW_DAYS` | `30` | Comparison window. |

## Implementation status

v0.5.6 ships **scaffolding** for both scripts:

- `labels-check.sh` runs three regex heuristics (gcloud no-`--labels=`, aws no-`--tags`, terraform-apply no-`labels=` / `tags=` block in any `.tf`). It does NOT validate that all four required keys are present — that requires command-line tokenizer work, scheduled for v0.6.0.
- `spike-detector.sh` ships with the `manual-csv` adapter (CSV-driven, lets a project verify the wiring with a fixture). The `gcp-bq` / `aws-cur` / `azure-cme` adapters require billing-export credentials and ship in v0.6.0.

Both scripts are wired in v0.5.6 in `warn` mode. Mode `block` is opt-in per project (set `GATE_MODE=block` in the project's hook config or env).

## Hook chain

The cost-gate hook is the seventh runtime hook in the Agency (alongside `secrets-scanner`, `tool-guardian`, `governance-audit`, `dependency-license-checker`, `session-logger`, `commit-gate.sh`). Per `TRUST.md` §2.7, runtime hooks are non-optional — bypassing this hook with `--no-verify` or equivalent files a `runtime-hook-bypass` ADR.

## Local testing

```bash
# Test labels-check on a synthetic gcloud command
echo 'gcloud compute instances create my-vm --zone=us-central1-a' \
  | GATE_MODE=warn ./runtime-hooks/cost-gate/labels-check.sh

# Test spike-detector with a fixture CSV
mkdir -p _vision/cost
cat > _vision/cost/manual-billing.csv <<EOF
project,month,spend_usd
demo,2026-03,100.00
demo,2026-04,160.00
EOF
COST_DATA_SOURCE=manual-csv ./runtime-hooks/cost-gate/spike-detector.sh
# → "SPIKE — project=demo prev=2026-03=$100.00 curr=2026-04=$160.00 (+60.0% ≥ threshold 50%)"
```
