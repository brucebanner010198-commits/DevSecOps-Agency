# arxiv — provenance

This skill is an agency import, ported verbatim from:

- **Source:** `NousResearch/hermes-agent`, path `skills/research/arxiv/`
- **License:** MIT (retained; the agency plugin is MIT, compatible)
- **Audit date:** v0.3.3 port. Grep pattern `eval\(|exec\(open|curl.*\|.*bash|wget.*\|.*sh|os\.system\(|shell=True` returned **zero matches**.
- **Scope change vs. upstream:** none. Files copied as-is.

## How the agency uses it

- **Research Council** specialists (`market-researcher`, `literature-reviewer`, `trend-scout`) invoke `arxiv` when a project needs academic-paper grounding.
- Thin wrapper over the free arXiv REST API. No API key. No outbound credentials. No rate-limit risk at agency scale (arXiv allows ~1 req/3s polite).
- Output feeds `_vision/research/` with citations. Never replaces `web-search` as the default research reach — arxiv is the preprint/academic lane.

## IP-lineage

Every lineage statement that cites an arXiv-sourced paper records:

- Source: `NousResearch/hermes-agent @ <commit>` MIT for the wrapper; arXiv for the paper corpus.
- Port date: v0.3.3
- Attribution of the paper itself follows the paper's license terms (usually CC-BY or arXiv's non-exclusive license; check per-paper).

See `skills/ip-lineage/SKILL.md` for the invariant.

## Exclusions on this port

None in this subtree.
