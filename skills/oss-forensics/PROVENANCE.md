# oss-forensics — provenance

This skill is an agency import, ported verbatim from:

- **Source:** `NousResearch/hermes-agent`, path `optional-skills/security/oss-forensics/`
- **License:** MIT (retained; the agency plugin is MIT, compatible)
- **Inspired-by (upstream-acknowledged):** RAPTOR's OSS Forensics system (1800+ line reference implementation)
- **Audit date:** v0.3.3 port. Grep pattern `eval\(|exec\(open|curl.*\|.*bash|wget.*\|.*sh|os\.system\(|shell=True` returned **zero matches** across `SKILL.md`, `scripts/`, `references/`, and `templates/`.
- **Scope change vs. upstream:** none. Files copied as-is.

## How the agency uses it

- **Security Council** specialists invoke `oss-forensics` alongside `secrets-vault` and `sbom-slsa` when a dep drops a red on SBOM reconciliation or a `secrets-scanner` hook fires.
- **Red-Team Council** specialist `supply-chain-attacker` invokes it in pre-release sweeps to enumerate the attacker's view of the dep graph.
- Never on delivery path. Invoked reactively on incidents and pre-release as a hygiene pass.

## IP-lineage

Every lineage statement that cites a pattern from this skill records:

- Source: `NousResearch/hermes-agent @ <commit>` MIT
- Inspired-by: RAPTOR OSS Forensics
- Port date: v0.3.3

See `skills/ip-lineage/SKILL.md` for the invariant.

## Exclusions on this port

None in this subtree. The godmode / sherlock / 1password exclusions live at the repo-survey level and were applied before copy-in.
