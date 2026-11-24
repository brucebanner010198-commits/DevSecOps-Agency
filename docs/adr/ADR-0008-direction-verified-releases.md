---
adr: 0008
title: Direction - the agency's product is verified releases (working assumption)
status: proposed
date: 2026-11-22
deciders: user (pending)
kind: direction
related: design review 1 (E1, E2), the 2026-06-17 direction decision, alignment plan Part 7A
---

# ADR-0008: Direction - verified releases

## Status

**Proposed.** Build work assumes this ADR from 2026-11-22, when the Chairman said "build it as per what I have already planned and shared". The Chairman has not accepted it. Until they do, only work that holds under every direction option is built on it: the baseline run, Phase 1a and Phase 2a. Phases 3 to 5, the Constitution amendments (E3 and E4) and the thin slice to a live URL still wait for the Chairman.

## Context

On 2026-06-17 the agency recorded "trust layer first": build the chaired company only after the trust layer earns revenue. That decision had a kill check on 2026-09-30, and no result was recorded. Since then the Chairman has asked for an agency that turns an idea into a product published in the real world. Design review 1 (E1) found that the two conflict: Phases 3 to 5 sit behind the June decision.

Options considered:

- **(a) Agency first.** The agency builds the Chairman's products, and the trust spine is its enforcement layer.
- **(b) Keep June.** The release gate is sold as a plugin, and the agency is its demo.
- **(c) Hybrid, verified releases.** The agency builds and publishes the Chairman's products. Nothing ships without an independent verdict and the Chairman's signature. The release gate and its verifiable record are the part others can use.

## Decision (proposed)

**(c).** It keeps the goal the Chairman stated and the path to a live URL. It also keeps the only differentiators both reviews found defensible: an independent verdict and a release record anyone can check. It does not compete with low-cost app builders on speed.

**Kill check:** by **2027-01-31**, one of the Chairman's products is live at a public URL with a verified release record. If not, the direction is reviewed.

If accepted, this ADR supersedes the 2026-06-17 decision.

## Consequences

- Phase 1 is narrowed and re-ordered (E2): first a baseline run, then Phase 1a (the enforced contract), then Phase 2a (deterministic hooks). The full Role Card v2 is not dropped, only moved later.
- Nothing in `CONSTITUTION.md`, `MISSION.md`, `VISION.md` or `GOVERNANCE.md` changes because of this ADR. Amendments need their own ADR and the Chairman's approval (G3).
- Accepting it closes G4, the roadmap's open "trust layer first?" question.
