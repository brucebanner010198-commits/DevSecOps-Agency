---
name: tool-scout
description: Vet a new MCP server or external tool before any agent adopts it. Produces a scout report with 7-dimension rubric + green/yellow/red verdict + constraint set. Dispatched by SRE Council on every Chief adoption request and quarterly for portfolio hygiene.
metadata:
  version: 0.3.0
---

# tool-scout

No agent adopts a new MCP / external tool without a scout report. Scout is owned by `mcp-registry-scout`; verdict binds the adoption.

## When to use

- Chief-requested MCP adoption (e.g. CMO wants a Meta Ads MCP).
- Chief-requested external-tool adoption (webhook API, CLI, SaaS).
- Quarterly sweep — re-scout all adopted tools for drift (new scopes requested? publisher changed?).
- Incident response — a tool misbehaved; re-scout to decide retire vs constrain.

## Process

1. **Read the request** — `_vision/sre/requests/<date>-<chief>-<tool>.md`: requestor, intended use, URL.
2. **Fetch the manifest** — README, source, OAuth-scope list, published SBOM if any.
3. **Score 7 dimensions** — see `references/rubric.md`.
4. **Verdict** — green / yellow with constraints / red.
5. **Write report** — `_vision/sre/<date>-scout-<tool>.md`.
6. **Hand to sre-lead** → CSRE + Chief decide.

## Verdict logic

- **green**: all 7 dimensions green/yellow, no reds. Adopt.
- **yellow**: ≤ 2 reds, all mitigable with the constraint set. Adopt with constraints.
- **red**: ≥ 3 reds OR any critical (unreversible + broad scope + no rotation). Do not adopt.

## Constraint set (yellow path)

- Sandbox-only execution — tool calls route through `sandbox-runner`.
- Scoped credentials — minimum-viable OAuth scopes, rotating creds.
- Rate limit — defaults per `references/rate-limits.md`.
- Audit — every call logged in `_vision/sre/tool-audit-<tool>.log`.
- Kill switch — CSRE can disable the tool without a new ADR.

## ADR triggers

- Every adoption (green or yellow) files an ADR citing the scout report.
- Every red files an ADR documenting the finding + alternative.
- Every quarterly re-scout that moves a tool green → yellow → red (or vice versa) files an ADR.

## Invariants

- Unvetted tools are not on any agent's toolkit.
- Scout writes the report; Chief + CSRE act.
- Reds don't become yellows to unblock a Chief.
- Unknown-info dimensions are reds by default.

## What never happens

- A specialist adopts a tool without scout.
- A Chief self-adopts without CSRE sign-off.
- A red scout gets stretched to yellow because the Chief is in a hurry.
- A tool outlives its adoption ADR.
