---
name: secrets-vault
description: Secrets lifecycle — provisioning, rotation, expiry, scanning. Agents receive vault refs (never raw secrets); the runtime resolves refs at call time. Every cred has an expiry; rotation always has an overlap + verify step. Scans run weekly + on every close-phase. Owned by secrets-vault specialist on the Security Council.
metadata:
  version: 0.3.0
---

# secrets-vault

Secrets never touch agent context. Refs do.

## When to use

- Project start-phase — provision scoped creds for third-party APIs.
- Chief dispatch — agent needs a vendor API and doesn't yet have a ref.
- Weekly — scanner sweep across repo tree.
- Expiry near-deadline — rotation triggered by vault manifest.
- Real-leak finding — emergency rotation + ADR.

## Process (provision)

1. Issue least-privilege credential (minimum scopes for the project's use).
2. Store raw cred in vault (encrypted-at-rest, envvar-backed, never in repo).
3. Return **vault ref** to caller: `_vault:<project>-<tool>`.
4. Schedule rotation: 30 days default; 7 days for high-privilege scopes.
5. Log `_vision/security/secrets-<project>.md`.

## Process (rotate)

1. Identify expiring refs via the manifest.
2. Issue replacement cred.
3. Update ref to point at the replacement.
4. Verify downstream: one real call with the new ref.
5. If verify passes, revoke old cred after 24h overlap window.
6. If verify fails, rollback + file ADR.

## Process (scan)

1. Run `gitleaks` / `trufflehog` across the repo tree.
2. Additionally pipe the session's file diffs through `runtime-hooks/secrets-scanner/scan-secrets.sh` (30+ hardcoded patterns: AWS, GitHub PATs, Stripe, JWT, Slack, private keys). The hook emits JSONL findings; no eval, no network, no remote config.
3. Classify each finding: false-positive / real-leak / fixture.
4. Real leak → immediate rotation + ADR + CAO notify.
5. Fixture → verify it's clearly fake; if not, treat as real.
6. Write `_vision/security/<date>-scan.md`.

## Invariants

- Agents see refs. Never raws.
- Every cred has an expiry. Infinite-life creds = critical finding.
- Rotation = overlap + verify. Never cut-over without verification.
- Scanner runs every close + weekly. Skipping is an audit red.
- Real leaks rotate same-turn.

## ADR triggers

- Every cred provision at high-privilege scope.
- Every rotation that fails verify.
- Every real-leak finding.
- Every infinite-life cred carve-out (requires user approval).

## What never happens

- Raw secret in a report, ADR, or log.
- Cred reuse across projects.
- Scanner finding left past one turn unclassified.
- Admin scopes when narrower scopes work.
- Credential in the repo (even encrypted).
