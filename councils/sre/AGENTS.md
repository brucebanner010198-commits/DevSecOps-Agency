# SRE Council

Runs the runtime boundary. Guards tool adoption, untrusted-input execution, model-routing safety, and cross-agency integration.

## Roster

- **sre-lead** (CSRE) — Chief. Convenes the council. Signs off on all verdicts.
- **mcp-registry-scout** — Vets new MCPs before adoption.
- **a2a-adapter** — Builds cross-agency adapters with default-deny scope guards.
- **sandbox-runner** — Executes untrusted tool calls in ephemeral sandboxes.
- **model-routing-override** — Owns emergency model reroutes during vendor outages.

## Independence invariant

SRE is a boundary guard, not a builder. No SRE specialist ever writes product code. If SRE is dispatched on a delivery task, rollback + file an independence-breach ADR. Mirrors Audit / Evaluation / Red-Team independence.

## When CEO convenes

- Every project that ships a runtime (web, daemon, scheduled job).
- Any Chief-requested MCP / external-tool adoption.
- Any vendor / model outage that blocks active work.
- Any cross-agency integration request.
- Quarterly portfolio-sweep for MCP inventory hygiene.

## Output shape

Reports live under `_vision/sre/<date>-<kind>.md`. Every `red` verdict files an ADR. Every routing override files an opening + closing ADR.

## Invariants

- Every tool adoption has a scout report.
- Every sandbox is ephemeral.
- Every override is time-boxed with a cap.
- Every A2A call is scoped + rate-limited + audited.
- Downgrades are forbidden long-term.
- Boundary guards never cross into delivery.
- **Cost discipline (added v0.5.5).** CSRE owns [`COST-AWARENESS.md`](../../COST-AWARENESS.md) and signs off on every project's `<slug>/cost-estimate.md` (Phase 6 gate, non-waivable per COST §2.4) and `<slug>/cost-reconciliation.md` (within 30 days of go-live, COST §2.5). CSRE runs the monthly idle-resource sweep (COST §2.6), the quarterly rightsizing review (COST §2.7), and the daily spike detector (COST §2.11). Cost-driven architecture changes that would downgrade Security or Design are auto-routed to CISO + CRT + User per COST §2.12 and `VALUES.md` §12.

## Convening triggers added in v0.5.5

- Phase 6 deploy gate — review `<slug>/cost-estimate.md`; sign or block.
- Phase 7 close — verify `<slug>/cost-reconciliation.md` within 30 days.
- Daily — review `inbox.json` for `cost-spike` priority entries (>50% MoM).
- Monthly — run the idle-resource sweep, file `_vision/rhythm/monthly-<YYYY-MM>.md` cost-sweep section.
- Quarterly — rightsizing review + commitment-coverage decision per project; publish `_meetings/cost-scorecard-YYYY-QN.md` alongside the trust scorecard.

## Skills added in v0.5.5 (cloud capability port)

CSRE now invokes the following skills when a project touches cloud infrastructure (imported from [`google/skills`](https://github.com/google/skills) under Apache-2.0; see [`LICENSES/APACHE-2.0-google-skills.txt`](../../LICENSES/APACHE-2.0-google-skills.txt)):

- [`skills/waf-cost-optimization`](../../skills/waf-cost-optimization/SKILL.md) — Google Cloud Well-Architected Framework Cost Optimization pillar (4 principles + product list + 10-item validation checklist).
- [`skills/networking-observability`](../../skills/networking-observability/SKILL.md) — SRE-style log-and-metric investigation with explicit anti-theater boundary rules ("no discrepancy loops", "conclusive acceptance of inactivity", "ban on auxiliary scripting").

CTO additionally owns the deployment-runtime skills ([`cloud-run-basics`](../../skills/cloud-run-basics/SKILL.md), [`gke-basics`](../../skills/gke-basics/SKILL.md)); CISO + CTO jointly own [`gcp-auth`](../../skills/gcp-auth/SKILL.md) (service-account hygiene, Workload Identity Federation, no service-account-key downloads).

## Added v0.5.6 — WAF reliability + chaos engineering + cost-gate hooks

CSRE now operates against the nine WAF-reliability principles folded into [`RESILIENCE.md > SLOs and error budgets`](../../RESILIENCE.md) and [`RESILIENCE.md > Chaos engineering`](../../RESILIENCE.md). Operationally:

- **Every shipped project carries a `<slug>/observability/slo.md`** with user-focused SLIs + SLO targets + error-budget policy. CSRE signs off; CQO instruments.
- **Quarterly chaos game day** runs per the procedure in [`skills/drill/SKILL.md > Chaos game days`](../../skills/drill/SKILL.md). Q2 slot is fixed two weeks before the trust-scorecard publish (2026-07-15 for the upcoming cycle). Independence rule: the council that owns the subsystem under test cannot run its own game day; CSRE rotates the lead role across COO / CRT / CAO.
- **`runtime-hooks/cost-gate/`** (new in v0.5.6) implements the runtime enforcement promised by `COST-AWARENESS.md` v1.0:
  - `labels-check.sh` — `preToolUse` on `gcloud` / `aws` / `az` / `terraform apply`. Refuses or warns on cloud-resource provisioning that omits the four required labels (`env`, `team`, `app`, `project`) per COST §2.1.
  - `spike-detector.sh` — daily `scheduled` trigger. Reads cost data, compares current vs. previous month per project, writes a `cost-spike` row to `inbox.json` for any project showing a >50% MoM increase per COST §2.11.
  - Both run in `warn` mode by default in v0.5.6; `block` mode is opt-in per project. Cloud-native billing-export adapters (gcp-bq, aws-cur, azure-cme) ship in v0.6.0 — v0.5.6 ships the `manual-csv` adapter for development verification.

Hook-bypass remains a `runtime-hook-bypass` ADR per `TRUST.md` §2.7.

## Added v0.6.1 — git-guardrails (the 8th runtime hook)

CSRE owns [`runtime-hooks/git-guardrails/`](../../runtime-hooks/git-guardrails/) — `preToolUse` hook on `^git ` Bash invocations that blocks (exit 2) destructive git operations before they execute. Pattern set covers force-pushes, plain pushes (USER-ONLY per Constitution §2.2 "publish externally"), hard resets, working-tree wipes, branch force-deletes, force restores, history rewrites, and aggressive GC.

The 8 runtime hooks now: secrets-scanner, tool-guardian, governance-audit, dependency-license-checker, session-logger, commit-gate, cost-gate (v0.5.6), git-guardrails (v0.6.1). Per `TRUST.md` §2.7, all hooks are non-optional; bypass attempts file a `runtime-hook-bypass` ADR.

Smoke-tested against six synthetic inputs at v0.6.1 ratification: 3 BLOCK cases (`git push origin main`, `git reset --hard HEAD~3`, `git clean -fd`) all returned exit 2; 3 ALLOW cases (`git status`, `git log --oneline -10`, `git commit -m hello`) all returned exit 0.

Customization: if a project has a legitimate need for a blocked pattern (e.g. a release-bot owning force-pushes to a release branch), file a `git-guardrails-exception-<reason>` ADR with CSRE + CRT countersign before adding a project-local exception. Do NOT remove patterns from the central hook without an Agency-wide ADR.
