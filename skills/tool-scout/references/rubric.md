# tool-scout rubric — 7 dimensions

Each dimension scored green / yellow / red. Missing info defaults to red.

## 1. Provenance

- **green**: official publisher, signed, SLSA level ≥ 2.
- **yellow**: reputable community fork, signed, clear maintainer identity.
- **red**: anonymous publisher, unsigned, or publisher reputation unknown.

## 2. Scope

- **green**: minimum-viable scopes; tool advertises what it needs, nothing more.
- **yellow**: broader scopes than strictly needed, but can be narrowed via config.
- **red**: kitchen-sink scopes (e.g. `*` OAuth), admin-level access requested for a read task.

## 3. Abuse-surface

- **green**: prompt-injection impact is bounded (read-only; no side effects that move money / send comms / delete data).
- **yellow**: impact is recoverable (send email that can be recalled; create draft that needs approval).
- **red**: prompt-injection can trigger unreversible harm (send money, delete prod data, post publicly).

## 4. Reversibility

- **green**: all actions undoable within the tool itself.
- **yellow**: actions undoable with manual intervention (e.g. restore from backup).
- **red**: actions not undoable (deleted blob, sent SMS, published tweet).

## 5. Secret-handling

- **green**: no secrets held by the tool; auth via OIDC / short-lived tokens.
- **yellow**: secrets held, rotation cadence documented, rotation automatable.
- **red**: long-lived secrets required; rotation undocumented or manual; secrets logged.

## 6. Maintenance

- **green**: commits within 90 days, security advisories resolved promptly, clear release cadence.
- **yellow**: commits within 1 year, some open advisories but none critical.
- **red**: dormant (> 1 year since last commit), unresolved critical advisories, or no advisory process.

## 7. Integration-cost

- **green**: standard transport (HTTP/stdio), well-documented, clean error codes.
- **yellow**: non-standard transport but adapter exists; documented; adapter cost < 1 engineering day.
- **red**: undocumented, unstable API, or adapter cost > 3 engineering days.

## Critical conditions (auto-red regardless of other scores)

- Reversibility `red` + Abuse-surface `red` + Secret-handling `red` = auto-red overall.
- Any dimension with missing information that the scout can't verify via the tool's own docs.
- Any tool that requests network exfil + file-write + remote-exec in one scope.
