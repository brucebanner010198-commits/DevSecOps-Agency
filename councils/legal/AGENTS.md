# councils/legal — boundaries

## Output contract

- Lead: `gc` (General Counsel). Specialists: license-checker, privacy-counsel.
- Artifacts: `<slug>/legal/licenses.md` (SBOM + compat verdict), `<slug>/legal/privacy.md` (PRIVACY posture), `PRIVACY.md` dropped at repo root if missing.
- Gate: green/yellow/red. Red blocks public release, full stop.

## Must

- License-checker produces a **full SBOM** of runtime dependencies plus transitive ones that introduce new obligations.
- Verdict per dependency: MIT/BSD/Apache = ✅; MPL/LGPL = ⚠️ (document dynamic-linking caveat); GPL/AGPL = ❌ for closed-source, flag explicitly.
- Privacy-counsel maps: what PII is collected, lawful basis, retention, user rights, sub-processors.
- Cross-check against `architecture/data-model.md` PII classification. Disagreement is a red flag.
- If `_memory/MEMORY.md > Recurring risks` has a relevant entry, cite it.

## Must not

- Give legal advice. State posture, cite obligations, recommend consulting a real lawyer for high-stakes shipping.
- Approve a dependency without checking its license text. Name of the package ≠ verdict.
- Ship public without a `PRIVACY.md`. If one doesn't exist, write one based on the data model.
- Let the user ship to a restricted jurisdiction (PCI, HIPAA) without the compliance-officer's compliance.md signoff.

## Gate heuristic

- `green`: SBOM clean, PRIVACY.md exists, posture documented, no GPL/AGPL unless user explicitly chose open-source.
- `yellow`: one MPL/LGPL dependency with documented caveat.
- `red`: GPL/AGPL in a closed-source ship, or missing PRIVACY.md with PII in data model, or PII-classification mismatch with data model.
