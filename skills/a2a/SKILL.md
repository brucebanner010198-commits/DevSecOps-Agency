---
name: a2a
description: Agent-to-Agent protocol adapter pattern. Every cross-agency call (our agents calling external, or external calling ours) routes through an adapter with default-deny scope guards + rate limits + audit logs. Dispatched by SRE Council on every A2A integration request.
metadata:
  version: 0.3.0
---

# a2a

Cross-agency calls cross a trust boundary. The adapter is the boundary.

## When to use

- External agent wants to call tools hosted in our agency.
- Our agents need to call tools hosted in another agency.
- Partner integration request from CSO / CMO / CBO.

## Process

1. **Read the request** — who + why + advertised tools + advertised scopes.
2. **Draft the adapter manifest** — allowed tools, denied tools (everything else), rate limits, audit log path.
3. **Build scope guard** — every call goes through the adapter; the guard enforces allowlist + ratelimit + identity check.
4. **Smoke suite**:
   - One allowed call → success.
   - One denied call → deny.
   - One over-limit call → 429.
5. **Deploy** — adapter runs as a sidecar / proxy; direct calls bypassing it are a critical finding.
6. **Document** — `_vision/sre/a2a-<partner>.md` with manifest + smoke results.

## Manifest shape

```yaml
partner: acme-agency
identity:
  mtls_fingerprint: <hash>
  jwt_issuer: acme.example.com
  jwt_audience: our-agency
allowed_tools:
  - file_issue
  - read_issue
denied_tools: "*"  # everything else
rate_limits:
  file_issue: 10/min, 100/day
  read_issue: 60/min, 1000/day
timeout_s: 30
audit_log: _vision/sre/a2a-acme.log
```

## Defaults

- Default-deny every tool. No `*` allows.
- Default rate: 60/min + 1000/day per tool.
- Default timeout: 30 s.
- Default identity: mTLS preferred; JWT with short TTL acceptable.
- Auto-pause tool if error rate > 5% over 1h.

## ADR triggers

- Every adapter launch.
- Every adapter teardown.
- Every auto-pause.
- Every scope expansion (adding a new allowed tool).

## Invariants

- Adapters live as long as their adoption ADR. Chief cancels → adapter tears down same turn.
- Audit log is append-only + hash-only (no bodies).
- Auto-pause is reversible but files an ADR both ways.

## What never happens

- Wildcard allowlist.
- Anonymous A2A (no identity verification).
- Bodies in the audit log.
- An adapter outlives its adoption.
