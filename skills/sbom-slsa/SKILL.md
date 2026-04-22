---
name: sbom-slsa
description: Produce Software Bill of Materials (CycloneDX) + SLSA provenance attestations for every shipped artifact. Runs at close-phase on any project that emits code; on any release candidate before publish. Pairs with ip-lineage (lineage = origin, sbom-slsa = composition + provenance). Owned by sbom-slsa specialist on the Security Council.
metadata:
  version: 0.3.0
---

# sbom-slsa

No artifact ships without an SBOM and a SLSA statement.

## When to use

- Project close-phase, for any project that emits code or compiled artifacts.
- Release-candidate stage, immediately before publish.
- Any dep-tree change > 5 deps added / removed (delta SBOM).

## Process

1. **Enumerate deps** — read package.json / pyproject.toml / Cargo.toml / go.sum / Gemfile.lock / etc.
2. **Generate SBOM**:
   - Primary: CycloneDX JSON.
   - Secondary (if consumer requires): SPDX.
   - Every dep: name, version, hash, license, direct/transitive.
   - Output: `<slug>/dist/sbom.cdx.json`.
3. **Generate SLSA provenance**:
   - Build environment identified (GitHub Actions, local, other).
   - SLSA level determined by what the build actually achieves (1 / 2 / 3 / 4).
   - Signed via sigstore keyless (OIDC) when in CI, or configured KMS key otherwise.
   - Output: `<slug>/dist/provenance.intoto.jsonl`.
4. **Verify**:
   - `slsa-verifier verify-artifact` on the attached artifact.
   - `cyclonedx-cli validate` on the SBOM.
5. **Attach** — both files go into the release assets.
6. **Log** — `_vision/security/<date>-provenance-<slug>.md`.

## SLSA levels (how to determine, not claim)

- **Level 1** — build is documented; provenance generated.
- **Level 2** — build is version-controlled + provenance is signed.
- **Level 3** — build is hermetic + provenance is tamper-evident (sigstore / in-toto).
- **Level 4** — build is reproducible; two builds produce byte-identical artifacts.

Report what's achievable. Don't claim level 3 on a local laptop build.

## ADR triggers

- Every dep with unknown license (red; block ship until resolved via ip-lineage).
- Every hash mismatch between manifest and lockfile (supply-chain finding).
- Every SLSA downgrade (project previously level 3, now level 2).
- Every unsigned SBOM shipped (incident-mode only; opening + closing ADR).

## Invariants

- Every published artifact has both SBOM + SLSA.
- Signatures always. Unsigned outputs are informational, not attestations.
- Keyless > long-lived keys.
- Transitive deps counted, always.
- SLSA level reported, not assumed.

## What never happens

- Ship without SBOM.
- Claim SLSA level the build doesn't achieve.
- Long-lived signing key in the repo.
- Omit deps because they're "transitively transitive".
- Pass a hash-mismatch dep as green.
