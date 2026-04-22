# `security` council — TEAM

> Living team card. Updated whenever the roster changes. Paired with [`AGENTS.md`](./AGENTS.md) which declares the council's contract.

## Remit

STRIDE + OWASP, threat model, code audit, pen-test, DLP, MCP defense, SBOM+SLSA, secrets lifecycle, compliance map.

## Convened when

Every project — first-pass after architecture, second-pass after execution.

## Lead

- **`security-lead`** — sonnet — Use this agent for the Security phase of a DevSecOps Agency project — both the up-front threat modelling pass and the post-build code audit pass.

## Specialists

| Agent | Tier | Purpose |
| --- | --- | --- |
| `threat-modeler` | `haiku` | Security Lead needs a STRIDE threat model and OWASP Top 10 coverage analysis derived from a product brief. |
| `code-auditor` | `haiku` | Security Lead needs a post-build audit verifying that mitigations from the threat model are actually present in the code. |
| `pen-tester` | `haiku` | CISO (security-lead) needs a hands-on security probe of the actually-implemented code — not the spec. |
| `compliance-officer` | `haiku` | CISO (security-lead) needs a compliance posture review — what frameworks apply, what controls are in scope, what's missing — given the data and deployment geography. |
| `dlp-scanner` | `sonnet` | Security council needs outbound Data Loss Prevention wired or audited — per-tool-call pre-egress scan, chain-of-tool correlation for split-secret detection, URL-path exfil check... |
| `mcp-defender` | `sonnet` | Security council needs MCP-specific defense wired or audited — pinned-hash registration of tool descriptions, drift detection, `<tool-description-data>` + `<tool-output-data>` e... |
| `sbom-slsa` | `haiku` | Security Council specialist (Wave 7). |
| `secrets-vault` | `haiku` | Security Council specialist (Wave 7). |

## Worker tier

Specialists may, when a task decomposes cleanly along a dimension (per-file, per-table, per-endpoint, per-dependency), spawn **workers** — a third tier below specialist. Workers inherit the parent specialist's tool set and model tier unless overridden. Default depth cap is three levels (Chief → Specialist → Worker); deeper fanout requires an ADR from the lead.

Worker declaration lives in the parent specialist's frontmatter:

```yaml
workers:
  - name: <slug>
    split: <dimension>    # e.g. per-file, per-endpoint, per-dep
    max_parallel: 8       # per-council cap, overrides optional
```

Fanout + aggregation is handled by `skills/fanout/` (see root README).

This council declares no worker patterns in v0.3.7. Extend here when one emerges.

## Council norms

The council's must / must-not contract is authoritative in [`AGENTS.md`](./AGENTS.md). This file only records who currently staffs the council.
