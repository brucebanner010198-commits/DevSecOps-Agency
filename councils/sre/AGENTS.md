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
