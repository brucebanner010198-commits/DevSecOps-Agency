---
name: fairness
description: >
  Audit an AI output, model, or decision process for bias and fairness
  across protected attributes.  Produces a group-level error-rate table,
  a disparate-impact score, documentation of trade-offs, and remediation
  guidance.  Invoke for any project producing outputs that could affect
  people unequally — hiring, lending, healthcare, housing, education,
  content moderation, or any scored/ranked output.  Trigger phrases
  include "fairness audit", "bias check", "disparate impact", "group
  fairness", "equalized odds", "demographic parity", "algorithmic
  discrimination", or any /devsecops-agency:fairness invocation.
metadata:
  version: "1.0.0"
---

# fairness — Bias + fairness audit

Authority: [`CONSTITUTION.md`](../../CONSTITUTION.md), [`VALUES.md`](../../VALUES.md), [`SECURITY.md`](../../SECURITY.md) §2 (ethics alignment)
Owner: CEthics · Reviewer: CAO
Called from: `skills/ship-it-kickoff`, `skills/eval`, `skills/audit`

## When to trigger

REQUIRED for:
- Any model or scoring system that ranks, filters, or selects people.
- Hiring, lending, healthcare, insurance, housing, education, immigration, criminal justice outputs.
- Content moderation that affects accounts.
- Generative output that could produce identity-linked stereotypes (image gen, narrative gen, voice gen).
- Any classifier whose false-positive or false-negative rate has different costs for different groups.

OPTIONAL for:
- General-purpose tools where use cases vary (document the unmitigated bias known to exist).

## Key concepts

### Protected attributes (context-dependent; not universal)

Common categories: race, ethnicity, gender / gender identity, age, disability, religion, national origin, sexual orientation, caste (DPDP / India relevant), pregnancy, veteran status, genetic information.

**Use cases define scope.** A health dataset may treat age as essential; a job applicant ranker may treat age as protected.

### Fairness notions (pick the right one — they cannot all be satisfied simultaneously)

- **Demographic parity** — outcome rate is equal across groups. Simple but can mask differing base rates.
- **Equalized odds** (Hardt et al., 2016) — TPR and FPR equal across groups. Strong but requires accurate ground truth.
- **Equal opportunity** — TPR equal across groups (weaker than equalized odds).
- **Predictive parity / calibration** — score means the same thing across groups (used in lending; cannot always coexist with equalized odds — Chouldechova 2017).
- **Individual fairness** — similar individuals get similar outcomes. Hard to define "similar" formally.
- **Counterfactual fairness** — output would be the same in a counterfactual world where the protected attribute differed. Requires a causal model.

**Choose the fairness criterion before running the audit.** Document the trade-off with other criteria that cannot also be satisfied. No criterion is universally right; choice is a values decision attributable to the CEthics review.

## Procedure

### Step 1 — Define the task precisely

- What is the input?
- What is the output (binary, probability, rank, generative)?
- What decision does the output drive?
- Who is the affected population?
- What is the cost of a false positive? A false negative?

### Step 2 — Select protected attributes

Based on the task domain + jurisdiction. Cite a source for each choice (law, policy, or CEthics justification).

### Step 3 — Choose the fairness criterion

Per §Key concepts above. Write one paragraph justifying the choice and naming what is traded off.

### Step 4 — Gather evaluation data

- Stratified across protected groups.
- Large enough per group that statistics are meaningful (≥ 30 samples per group is a floor; larger for rare outcomes).
- Ground-truth-labeled where outcome-based fairness is measured.

**If data is insufficient per group, the audit cannot confidently claim fairness. Say so plainly.**

### Step 5 — Compute group-level metrics

For each protected group:

| Metric | Formula |
|---|---|
| Positive rate (selection rate) | P(ŷ=1 \| group) |
| True positive rate (recall) | P(ŷ=1 \| y=1, group) |
| False positive rate | P(ŷ=1 \| y=0, group) |
| Precision (PPV) | P(y=1 \| ŷ=1, group) |
| Accuracy | P(ŷ=y \| group) |
| Calibration | E[y \| score=s, group] = s ? |

Present as a table, group × metric.

### Step 6 — Compute fairness scores

Based on the chosen criterion in Step 3:

- **Disparate impact ratio** = positive rate of smaller group / positive rate of larger group. **US EEOC "four-fifths" rule of thumb:** ratio < 0.8 is a red flag (not a legal conclusion; jurisdiction-specific).
- **Equalized-odds gap** = max |TPR_g - TPR_h| + max |FPR_g - FPR_h| across groups. Report raw.
- **Calibration gap** = max |E[y \| score, g] - score| across groups and score bins.

### Step 7 — Intersectional analysis

Do not stop at single attributes. Women of color may face different effects than women or people of color separately. Stratify by intersections where group sizes permit.

### Step 8 — Qualitative review

Quantitative metrics miss representational harms. Examples:

- Generative model produces stereotyped imagery (e.g., "CEO" → all male, light-skinned).
- Output language is more formal for one group than another.
- Error modes cluster around culturally specific names or locations.

Review a stratified sample manually.

### Step 9 — Identify mitigations

Options (each has trade-offs):

- **Pre-processing:** rebalance training data, reweight samples.
- **In-processing:** fairness-constrained optimization during training.
- **Post-processing:** adjust decision thresholds per group (legally fraught in some jurisdictions; document).
- **Remove or reduce reliance on proxy features** (ZIP code as proxy for race, etc.).
- **Change the decision** — sometimes the fair answer is to not deploy the system.

Document the mitigation path selected, what it costs, and what residual bias remains.

### Step 10 — Document residual risk + sunset date

Even post-mitigation bias may remain. State it clearly:

- "After mitigation, the disparate impact ratio is 0.87; we accept this because [reason] and will re-audit in 6 months."
- Or: "After mitigation, the calibration gap remains 0.08 for group X. Users are informed via [mechanism]."

### Step 11 — Sign-off

CEthics sign-off on the fairness appendix before the artifact ships if any affected decision is legally or ethically consequential. USER approval additionally required if disparate-impact ratio is < 0.8 post-mitigation and deploy is still proposed.

## Anti-patterns

- **"Fairness through unawareness."** Dropping the protected attribute rarely works — proxy features carry the signal. Measure; don't hope.
- **Single-metric audits.** One fairness score without the trade-off conversation misleads the stakeholder.
- **Ignoring base-rate differences.** "Equal outcomes" may not be the right target if base rates legitimately differ.
- **Treating fairness as a one-time certification.** Models drift; audit recurs.
- **Benchmark-suite worship.** Generic fairness benchmarks miss domain-specific harms.
- **Not consulting affected communities.** Quantitative + affected-community review is stronger than either alone.

## Outputs

- Fairness Appendix attached to project ADR.
- Group-level metrics table.
- Fairness-score summary with chosen criterion + traded-off criterion.
- Mitigation decision with rationale.
- Residual-risk statement with re-audit date.
- LESSONS row if a pattern was unusual.

## References (original synthesis)

- Barocas, Hardt & Narayanan, *Fairness and Machine Learning* (fairmlbook.org).
- Hardt, Price & Srebro, *Equality of Opportunity in Supervised Learning* (NeurIPS 2016).
- Chouldechova, *Fair prediction with disparate impact* (Big Data, 2017).
- Kusner et al., *Counterfactual Fairness* (NeurIPS 2017).
- EEOC Uniform Guidelines on Employee Selection Procedures (1978) — four-fifths rule.
- NIST SP 1270, *Towards a Standard for Identifying and Managing Bias in AI* (2022).
- Gebru et al., *Datasheets for Datasets* (CACM 2021).
- Mitchell et al., *Model Cards for Model Reporting* (FAT* 2019).
