---
name: ip-lineage
description: Track IP provenance for every generated artifact — prompts, models, training-data similarity, external deps, user contributions. Produces a lineage statement on close-phase. Flags incompatible licenses, concerning training-data similarity, and unattributed user contributions. Pairs with sbom-slsa (sbom = composition, lineage = origin). Owned by ip-lineage specialist on the Legal Council.
metadata:
  version: 0.3.0
---

# ip-lineage

Every shipped artifact has a traceable origin. Lineage is the trace.

## When to use

- Project close-phase, for any project that emits artifacts.
- Creative outputs (images, logos, copy, music) get extra similarity scrutiny.
- License conflict resolution when sbom-slsa flags a dep.
- Any user dispute ("I contributed X") — lineage is the record.

## Process

1. **Build lineage tree** for each artifact:
   - **Prompt source** — user / agent / template.
   - **Model** — vendor + family + version + run time.
   - **External inputs** — libraries, APIs, fetched docs, user uploads.
   - **Derived-from** — any quoted / adapted source, attributed.
2. **Reconcile dep licenses**:
   - Pull each dep's license.
   - Cross-check against project's declared license.
   - Flag incompatibilities as red.
   - Runtime support — `runtime-hooks/dependency-license-checker/check-licenses.sh` scans dep diffs (npm, pip, go mod, gem, cargo) and emits JSONL findings. Lineage consumes these findings as pre-filtered input.
3. **Run similarity check** (creative outputs):
   - Perceptual hash (images) / n-gram overlap (text) / melodic-fingerprint (music).
   - ≥ 85% similarity to known corpus → red.
   - 70–85% → yellow, attribution required.
4. **Attribute user contributions** — any user-provided idea / spec / asset named + credited.
5. **Write statement** — `_vision/legal/<date>-ip-lineage-<slug>.md`.
6. **Attach** to release assets.

## ADR triggers

- Every license incompatibility.
- Every ≥ 85% similarity hit.
- Every unknown-license dep (blocks ship until resolved).
- Every user-contribution dispute.

## Invariants

- Every artifact has a lineage statement.
- License incompatibilities = reds, not yellows.
- Similarity thresholds are fixed — raising them is an ADR.
- User contributions always credited.
- Imported skill packs and agents record source provenance in their own `README.md` (or agent-file frontmatter comment) and are surfaced in every lineage statement that cites a pattern from them. Current imports: `skills/sdlc-patterns/` ← `NousResearch/hermes-agent` MIT; `runtime-hooks/` ← `github/awesome-copilot` MIT; `skills/oss-forensics/` ← hermes-agent MIT (inspired by RAPTOR's OSS Forensics system); `skills/arxiv/` ← hermes-agent MIT; `agents/audit/agent-governance-reviewer.md` ← awesome-copilot MIT (frontmatter reformatted to agency convention).

## What never happens

- Ship without similarity check on creative output.
- Unknown license dep accepted silently.
- Attribution stripped for brevity.
- Lineage mixed with novelty verdicts (CRT / CEVO own novelty).
- Skipping lineage for internal projects. Internal still has a license.
