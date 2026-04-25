#!/usr/bin/env bash
# spike-detector.sh — daily check for >50 % MoM spend increases on agency-managed projects.
#
# Backs COST-AWARENESS.md §2.11 ("same-day User notification on >50 % MoM spend jumps").
# Trigger: scheduled (daily) — typically wired to the daily heartbeat hook chain.
#
# Inputs:
#   COST_DATA_SOURCE — one of: gcp-bq, aws-cur, azure-cme, manual-csv (default: manual-csv)
#   COST_DATA_PATH    — path to billing data (CSV expected for manual-csv mode)
#   SPIKE_THRESHOLD_PCT — percentage MoM increase that triggers (default: 50)
#   WINDOW_DAYS       — comparison window (default: 30 days)
#
# Outputs:
#   - exit 0 with normal output: no spike
#   - exit 0 with warning to stderr + appended row to inbox.json: spike detected
#   - exit 1: data source unreachable (treat as compliance-drift per COST §2.11)
#
# Implementation status (v0.5.6): scaffolding for the manual-csv path. The gcp-bq /
# aws-cur / azure-cme paths require billing-export credentials and are scheduled for
# the v0.6.0 wave. The manual-csv path lets a project verify the wiring with a
# fixture CSV in development.

set -euo pipefail

COST_DATA_SOURCE="${COST_DATA_SOURCE:-manual-csv}"
COST_DATA_PATH="${COST_DATA_PATH:-_vision/cost/manual-billing.csv}"
SPIKE_THRESHOLD_PCT="${SPIKE_THRESHOLD_PCT:-50}"
WINDOW_DAYS="${WINDOW_DAYS:-30}"

case "$COST_DATA_SOURCE" in
  gcp-bq|aws-cur|azure-cme)
    echo "cost-gate/spike-detector: $COST_DATA_SOURCE adapter not yet implemented (v0.6.0 wave)" >&2
    exit 0
    ;;
  manual-csv)
    if [[ ! -f "$COST_DATA_PATH" ]]; then
      echo "cost-gate/spike-detector: $COST_DATA_PATH not found — no spike check possible. Per COST §2.11, treat as compliance-drift if a project is expected to have billing data." >&2
      exit 0
    fi
    ;;
  *)
    echo "cost-gate/spike-detector: unknown COST_DATA_SOURCE='$COST_DATA_SOURCE'" >&2
    exit 1
    ;;
esac

# Manual-CSV path: expects header `project,month,spend_usd` then rows.
python3 - <<'PY'
import csv, os, sys, datetime, json, pathlib

path = os.environ.get("COST_DATA_PATH", "_vision/cost/manual-billing.csv")
threshold = float(os.environ.get("SPIKE_THRESHOLD_PCT", "50"))
window_days = int(os.environ.get("WINDOW_DAYS", "30"))

by_project = {}
with open(path, newline="") as f:
    for row in csv.DictReader(f):
        proj = row["project"]
        month = row["month"]
        spend = float(row["spend_usd"])
        by_project.setdefault(proj, {})[month] = spend

inbox_rows = []
for proj, months in by_project.items():
    sorted_months = sorted(months)
    if len(sorted_months) < 2:
        continue
    prev_m, curr_m = sorted_months[-2], sorted_months[-1]
    prev_v, curr_v = months[prev_m], months[curr_m]
    if prev_v <= 0:
        continue
    pct = ((curr_v - prev_v) / prev_v) * 100.0
    if pct >= threshold:
        line = f"cost-gate/spike-detector: SPIKE — project={proj} prev={prev_m}=${prev_v:.2f} curr={curr_m}=${curr_v:.2f} (+{pct:.1f}% ≥ threshold {threshold}%)"
        print(line, file=sys.stderr)
        inbox_rows.append({
            "ts": datetime.datetime.utcnow().isoformat() + "Z",
            "priority": "cost-spike",
            "project": proj,
            "prev_month": prev_m, "prev_spend_usd": prev_v,
            "curr_month": curr_m, "curr_spend_usd": curr_v,
            "increase_pct": round(pct, 2),
            "threshold_pct": threshold,
            "source": "cost-gate/spike-detector.sh",
            "ref": "COST-AWARENESS.md §2.11",
        })

# Append findings to inbox.json (create if missing).
if inbox_rows:
    inbox_path = pathlib.Path("inbox.json")
    existing = []
    if inbox_path.exists():
        try:
            existing = json.loads(inbox_path.read_text())
            if not isinstance(existing, list):
                existing = []
        except json.JSONDecodeError:
            existing = []
    existing.extend(inbox_rows)
    inbox_path.write_text(json.dumps(existing, indent=2))
    print(f"cost-gate/spike-detector: appended {len(inbox_rows)} cost-spike row(s) to inbox.json", file=sys.stderr)
PY

exit 0
