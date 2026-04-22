---
name: system-card
description: >
  Regenerate SYSTEM-CARD.md at every minor version bump (v0.X.0) or after
  any material capability or limit change.  The skill collects actual
  measured capabilities from the current repo state (councils, skills,
  hooks, founding docs), verifies claims against evidence, and produces
  the updated card.  Trigger phrases include "regenerate system card",
  "update SYSTEM-CARD", "refresh system card", or any
  /devsecops-agency:system-card invocation.
metadata:
  version: "1.0.0"
---

# system-card — Regenerate SYSTEM-CARD.md

Authority: [`CONSTITUTION.md`](../../CONSTITUTION.md) Article III (Transparency) + [`SYSTEM-CARD.md`](../../SYSTEM-CARD.md)
Owner: CEVO · Reviewer: CAO · Called by: `skills/rhythm` (on minor version bump)

## Purpose

Ensure the published [`SYSTEM-CARD.md`](../../SYSTEM-CARD.md) reflects what is actually true about the Agency, not what was true at the last release. A claim in the card that is no longer true is a Critical governance finding.

## When to run

- **Required:** Every minor version bump (v0.X.0).
- **Required within 48h:** any time a capability claim or limit claim is discovered false.
- **On demand:** before any external audit or third-party review.

## Inputs

1. Current repo state.
2. [`CONSTITUTION.md`](../../CONSTITUTION.md) — source of truth for governance claims.
3. [`AGENTS.md`](../../AGENTS.md) root — source of truth for council/agent counts.
4. `skills/` directory — source of truth for skill count.
5. `runtime-hooks/` directory — source of truth for hooks.
6. Latest [`TRUST.md`](../../TRUST.md) scorecard.
7. Latest Keeper Test findings.
8. Latest [`THREAT-MODEL.md`](../../THREAT-MODEL.md) — for residual risk.
9. Latest [`SWOT.md`](../../SWOT.md) — for opportunity/threat roadmap dates.

## Procedure

### Step 1 — Measure actual counts

```bash
# Councils
ls councils/ | wc -l

# Agents per council (walk councils/*/AGENTS.md or chief/specialist/worker subdirs)
# Skills
ls skills/ | wc -l

# Hooks
ls runtime-hooks/ | wc -l

# Founding documents at repo root
ls *.md
```

Write each count as a hard number. These numbers go into [`SYSTEM-CARD.md`](../../SYSTEM-CARD.md) §1.

### Step 2 — Verify capability claims in §3

For each claim in [`SYSTEM-CARD.md`](../../SYSTEM-CARD.md) §3 (Capabilities), locate the evidence:

- Claim in §3.1 (Governance) → cite [`CONSTITUTION.md`](../../CONSTITUTION.md) section.
- Claim in §3.2 (Security) → cite `runtime-hooks/...` + [`SECURITY.md`](../../SECURITY.md) section.
- Claim in §3.3 (Quality, Reliability, Audit) → cite council file path + SLAs.
- Claim in §3.4 (Ethics) → cite [`VALUES.md`](../../VALUES.md) + [`CONSTITUTION.md`](../../CONSTITUTION.md) §8.5.
- Claim in §3.5 (Knowledge) → cite [`LESSONS.md`](../../LESSONS.md) + `skills/career-ladder`.

**Any claim without evidence is re-written as "planned for vX.Y.Z" or removed.** No aspirational claims in the card.

### Step 3 — Verify limits in §4

Three sub-sections. Verify each list remains accurate:

- **Will not** — confirm refusal pattern is enforced (check Constitution §8.5 + relevant hooks).
- **Cannot** — confirm capability bound is real (scale, single-user, etc.).
- **Has not been tested against** — confirm each item remains genuinely untested; remove items now covered by drills.

### Step 4 — Update evaluation methodology metrics

§5 references the latest [`TRUST.md`](../../TRUST.md) targets. Confirm the target values match what [`TRUST.md`](../../TRUST.md) §3 currently specifies. If they diverge, reconcile — [`TRUST.md`](../../TRUST.md) is authoritative and [`SYSTEM-CARD.md`](../../SYSTEM-CARD.md) quotes it.

### Step 5 — Refresh known failure modes

§6 items are rolling. Add any new failure mode discovered since last release (source: LESSONS rows, RCAs, Keeper Test findings). Remove an item only if a corresponding control fully closes it (rare — usually move to "mitigated, monitored").

### Step 6 — Dependencies + environmental

§9 lists what we depend on externally; §10 lists environmental posture. Update only if truly changed (model pin change, sustainability council added, etc.).

### Step 7 — Disclosures — honesty pass

§12 is the hardest section. Ask:

- Is anything here overstated?
- Is any new limitation un-disclosed?
- Is the probation window (year-one) still active? Today?

**If you are tempted to soften a disclosure, don't.** The disclosures section is what a third party reads to calibrate trust.

### Step 8 — Produce the updated card

Write the new [`SYSTEM-CARD.md`](../../SYSTEM-CARD.md) with:

- Version bumped (1.0 → 1.1, etc.).
- `Plugin version at card publish` updated.
- `Ratified` date updated to today.

### Step 9 — Diff review

Produce a markdown diff summary: what changed, what didn't, and why. This summary accompanies the commit message. CEVO + CAO sign off before merge.

### Step 10 — Publish

Commit to `main` alongside the version bump. Update [`README.md`](../../README.md) footer link to the card.

## Anti-patterns

- **Copy-paste last quarter.** The point is to re-measure.
- **Hide limits discovered since last release.** Worst trust failure.
- **"Aspirational capabilities."** A card is a description of what IS, not what WILL BE. Planned items live in [`SWOT.md`](../../SWOT.md) §5 roadmap.
- **Omitting untested territory.** If it hasn't been tested, §4 must say so.

## Outputs

- Updated [`SYSTEM-CARD.md`](../../SYSTEM-CARD.md) (version incremented).
- Diff summary in the commit message.
- LESSONS row if something material changed.

## References

- Mitchell et al., *Model Cards for Model Reporting* (FAT* 2019).
- Anthropic Claude 3 model card family (as pattern).
- OpenAI GPT-4 system card (as pattern).
- Gebru et al., *Datasheets for Datasets* (CACM 2021).
- NIST AI RMF 1.0 — documentation function.
