# `board` council — TEAM

> Living team card. Updated whenever the roster changes. Paired with [`AGENTS.md`](./AGENTS.md) which declares the council's contract.

## Remit

The AI governance body chaired by the Chairman of the Board. Oversees the CEO, sets and approves strategy/goals (reciprocal: CEO proposes, Board reviews, Chairman votes), and hosts the blocking committees as standing committees.

## Convened when

Only when the Chairman calls a Board of Directors meeting (`skills/board-meeting`), or a USER-ONLY decision (`CONSTITUTION.md §2.2`) needs group review.

## Lead

- **`board-director`** — opus — represents the Board body in a convened meeting; governance-only, never operates.

## Standing committees (not specialists)

No new specialists are hired for this council. The four existing blocking Chiefs attend a convened Board meeting in a **governance capacity**, distinct from their normal delivery-path chief role:

| Committee                  | Chief(s)                                          | Council home        |
| --------------------------- | -------------------------------------------------- | -------------------- |
| Audit Committee              | `cao`                                              | `councils/audit`      |
| Risk & Security Committee     | `security-lead` (CISO) + `red-team-lead` (CRT)     | `councils/security`, `councils/red-team` |
| Evaluation Committee          | `evaluation-lead` (CEVO)                           | `councils/evaluation`  |

## Worker tier

Not applicable. The Board governs — it does not shard delivery work into workers. This council declares no worker patterns.

## Council norms

The council's must / must-not contract is authoritative in [`AGENTS.md`](./AGENTS.md). This file only records who currently staffs the council.

## Depth-cap note

The Board tier sits above the CEO in governance, parallel to the Chief → Specialist → Worker delivery depth cap (`CONSTITUTION.md §3.1`). Convening the Board does not add a fourth delivery tier and does not require a `fanout-depth-override` ADR.
