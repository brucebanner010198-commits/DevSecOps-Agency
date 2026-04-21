# Red-Team Council — AGENTS.md (scoped)

Telegraph. Read before dispatching any Red-Team specialist.

## Chief

- `red-team-lead` (CRT). Sonnet. Black.

## Specialists

- `adversarial-prompter` · prompt-injection, jailbreak, indirect-injection, goal-hijack.
- `tool-abuse-tester` · unauthorized tool use, permission bypass, tool-chaining.
- `data-exfil-tester` · PII / credential / secret / memory-readback egress.
- `model-poisoning-scout` · memory + context-window + playbook poisoning signals.
- `supply-chain-attacker` · dependency, typosquatting, model-swap, MCP-provenance.
- `social-engineering-tester` · impersonation, authority-spoof, HITL overload.
- `playbook-author` · stepping-stone archive + prompt-diff review.

## Council role

- **Informing + independent.** Red-team never sits on the delivery path. Reds climb the ladder to Rung 3; Rung 6 is the only route to accept a red without fix.
- **Workspace + per-project scope.** Per-project artifacts in `<slug>/red-team/`. Portfolio artifacts + stepping-stone archive in `_vision/red-team/` + `_vision/playbooks/`.
- **Parallel to Eval + Audit.** CRT + CEVO + CAO all run on every close. None signs off on the others; each writes its own findings.

## Must

- Run a pre-release red-team on every shipped project before archival.
- Run a prompt-upgrade red-team on every mutation to `agents/*.md` or high-leverage `skills/*/SKILL.md` before the change lands.
- Map every finding to at least one OWASP ASI Top 10 category (`skills/red-team/references/owasp-asi-top-10.md`). Findings without an ASI mapping are invalid.
- File an ADR for every `high` or `critical` finding in the same CEO turn (per `skills/adr/references/decision-triggers.md > Red-team`).
- Author a stepping stone for every remediated `high`+ finding. Stones are immutable once archived.
- Route remediation through the owning council via `skills/taskflow` — red-team never edits delivery artifacts directly.

## Must not

- Dual-hat any red-team specialist with a delivery Chief or with Audit.
- File a finding without a reproduction. "It might be vulnerable" is not a finding.
- Fix findings. Red-team proves; the owning council repairs.
- Exfil real PII or real credentials in a reproduction. Synthesize.
- Edit an archived stepping stone. Supersede via a new stone that links back.
- Use destructive tool calls in reproductions. Dry-run or mock the destructive tail.
- Skip a prompt-diff review for an `agents/*.md` change. Skipping is a Wave 6 anti-pattern.

## Gate heuristic

| Finding severity present | Gate    |
|--------------------------|---------|
| critical                 | red     |
| high                     | red     |
| medium (≥ 1)             | yellow  |
| low / info only          | green   |
| no findings              | green   |
| red-team skipped         | (CEO cannot advance — procedural red) |

Yellow requires `followups[]` with an owning council per finding.

## Integration points

- **`skills/adr`** — Red-team triggers listed in `skills/adr/references/decision-triggers.md > Red-team (v0.3.0 Wave 6)`.
- **`skills/ladder`** — Red reds enter at Rung 3 (cross-council to owner, usually CISO). Rung 6 is the only accept-without-fix path.
- **`skills/eval`** — CEVO writes regression tests from stepping stones. Every `high`+ stone has a paired eval item.
- **`skills/audit`** — CAO cross-checks that every stepping stone has a linked ADR and that the remediation ADR exists for every finding marked `remediated: true`.
- **`skills/memory`** — `model-poisoning-scout` is read-only on `_memory/`. Corrections land via `[correction]` session-log lines through memory-auditor, not via scout rewrites.
- **`skills/worktree`** — Red-team worktrees are writable only under `<slug>/red-team/` and `<slug>/_worktrees/red-team-*/`.

## Outputs

- `<slug>/red-team/findings.md` — per-project.
- `<slug>/red-team/repros/rt-NNNN.md` — per-finding reproductions.
- `_vision/red-team/<date>-portfolio.md` — portfolio adversarial sweeps.
- `_vision/playbooks/ARCHIVE.md` — stepping-stone index.
- `_vision/playbooks/stones/stone-NNNN-<slug>.md` — individual stones.

## Independence invariants

- CRT cannot dual-hat with any delivery Chief or Audit.
- Specialists rotate out of any delivery pool they contributed to within the same quarter.
- A red-team finding on a project a specialist previously delivered to is blind-peer-reviewed by another specialist.
- Red-team worktrees are append-only on findings; never rewrite a prior finding entry.

## Escalation

- `critical`: same-turn `notify` event + ADR + immediate ladder Rung 3 dispatch to owner.
- `high`: same-turn ADR + next-dispatch Rung 3.
- `medium`: followup task + scheduled next-phase re-test.
- `low` / `info`: logged; no gate impact; may be bundled into a stone if recurring.
