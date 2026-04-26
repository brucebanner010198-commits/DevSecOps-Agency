# COST-AWARENESS.md — The Agency's cost-discipline contract

This document is the single page the Agency points anyone at who asks "what is this thing going to cost me, and how do you keep it from running away?". It states — in plain language and in measurable terms — what the Agency promises about cloud spending on every project it ships, how each promise can be verified by reading files in the project folder, and what we owe you when we miss. It is subordinate to `CONSTITUTION.md` (Art I §1.1 supremacy, Art V §5 process guarantees) and to `VALUES.md` §12 (build-order priority — cost optimization is part of the **Operations** pillar, ahead of Timely Delivery and behind Security & Privacy / Design).

Ratified **2026-04-23** alongside plugin **v0.5.5**. Reviewed quarterly on the `rhythm` cadence; amendable only via `cost-amend` ADR with **CSRE + CAO + CFO-shaped review** routing (since no CFO chief exists, CSRE owns and CAO countersigns). Clauses affecting CONSTITUTION.md §8.5 non-waivables or §2.2 USER-ONLY actions route through Constitution Article X as USER-ONLY.

MUST / MUST NOT / SHALL / SHOULD / SHOULD NOT / MAY below follow RFC 2119 / RFC 8174.

Imported principles trace to the Google Cloud Well-Architected Framework Cost Optimization pillar (Apache-2.0, see [`LICENSES/APACHE-2.0-google-skills.txt`](LICENSES/APACHE-2.0-google-skills.txt)) and to FinOps Foundation principles (CC BY 4.0, cited inline). Synthesis is original.

---

## 1. The short version

The Agency is **not** a cost-blind code generator. It treats cloud spending as a first-class governance dimension. Four practical consequences:

1. **Every shipped project carries a cost estimate before it deploys.** Phase 6 (Deploy) cannot pass without a `<slug>/cost-estimate.md` signed off by CSRE. No surprises in your first invoice.
2. **Every cloud resource we provision is labeled with `env`, `team`, `app`, and `project-slug`.** You can answer "what is this $X line item from?" by running one filter in your billing console.
3. **Every project's monthly spend is reconciled against its estimate within 30 days of go-live.** Variance > 25% triggers a `cost-variance` ADR and a written cause-analysis. No silent drift.
4. **Any month-over-month spend increase > 50% on any project the Agency owns notifies the User same-day.** No five-figure surprise emails from your cloud provider.

Cost discipline with us is empirical, not aspirational. The same paper-trail posture that backs `TRUST.md` backs this document.

---

## 2. The twelve cost commitments

Each commitment has three fields: **Claim**, **How to verify**, **If we miss**. Claims are numbered for citation (cite as `COST §2.N`).

### §2.1 Cost attribution — 100% labeled resources

- **Claim.** Every cloud resource the Agency provisions on a user's account MUST carry these labels: `env={dev|staging|prod}`, `team=<owner-council>`, `app=<service-name>`, `project=<slug>`. Resources without all four labels MUST NOT pass the Phase 6 deploy gate.
- **How to verify.** In any project folder: `<slug>/infra/labels-policy.md` lists the four required keys. CSRE's deploy hook (`runtime-hooks/cost-gate/labels-check.sh`, added in v0.5.5) blocks any Terraform plan or `gcloud` invocation that creates a resource without the four labels. Cloud billing export (see §2.2) lets you confirm coverage by querying `WHERE label.project IS NULL`.
- **If we miss.** CSRE files `labels-violation` ADR; offending resources are relabeled within 7 days or torn down. Repeated violations escalate to a Keeper-Test review of the deploying agent.

### §2.2 Granular billing visibility — billing export enabled, queryable by SQL

- **Claim.** For every shipped project that incurs cloud cost, the Agency MUST enable cloud billing export to a queryable analytics store (BigQuery for GCP, S3+Athena for AWS, Cost Management Export for Azure). Setup MUST happen at Phase 1 (Intake), not at first invoice.
- **How to verify.** `<slug>/infra/billing-export.tf` (Terraform) or `<slug>/infra/billing-export.md` (manual setup record) exists. CSRE confirms first row in the export table within 24h of project go-live.
- **If we miss.** Project's monthly cost reconciliation (§2.11) is impossible without billing data — CSRE blocks the next phase transition until export is live.

### §2.3 Budgets and alerts — every project has both

- **Claim.** Every shipped project MUST have a defined monthly budget (in USD or local currency) and at least three alert thresholds (typically 50%, 90%, 100% of budget). Budget MUST be set before the first cloud resource is provisioned, not retroactively.
- **How to verify.** `<slug>/cost-estimate.md` declares the budget and threshold list. The corresponding cloud-native budget object exists in the user's project (`gcloud billing budgets list`, `aws budgets describe-budgets`, etc.) and is linked from the file.
- **If we miss.** No budget = blocked Phase 6 deploy. CSRE has hard veto here.

### §2.4 Pre-deploy cost estimate — written, owned, signed

- **Claim.** Every project MUST produce `<slug>/cost-estimate.md` before Phase 6 (Deploy). The estimate MUST include monthly cost projection broken down by component (compute, storage, network egress, managed-service fees), the assumed traffic/usage levels, and a sensitivity analysis ("if traffic is 10× the assumed level, monthly cost goes from $X to $Y"). CSRE signs off.
- **How to verify.** File exists; CSRE's signature row appears at the bottom; the cost-impact estimate is referenced in the Phase 6 ADR.
- **If we miss.** Phase 6 cannot pass. There is no waiver path — this is non-waivable for any project that touches cloud resources.

### §2.5 Post-deploy reconciliation — actual vs estimate, within 30 days

- **Claim.** Within 30 calendar days of project go-live, the Agency MUST publish `<slug>/cost-reconciliation.md` comparing actual cloud spend (from billing export §2.2) against the pre-deploy estimate (§2.4). Variance > 25% in either direction MUST trigger a written `cost-variance-<over|under>` ADR explaining the cause.
- **How to verify.** `<slug>/cost-reconciliation.md` exists 30d after the Phase 7 ADR. Variance ADR (if any) is linked from it. CAO monthly audit spot-checks variance ADRs for actual cause-analysis content (not "TBD").
- **If we miss.** Project enters drift status. Monthly heartbeat surfaces it. After two consecutive missed reconciliations, project routes to Rung 3 of the never-give-up ladder.

### §2.6 Idle-resource sweep — monthly, with deletion teeth

- **Claim.** CSRE MUST run a monthly idle-resource sweep on every shipped project: orphan persistent disks, idle VMs (CPU < 5% for ≥ 14 days), unattached IP addresses, idle Kubernetes clusters, unused load balancers. Findings are either deleted (if ownership is clear and no one objects in 7 days) or assigned an owner with a justification ADR.
- **How to verify.** `_vision/rhythm/monthly-<YYYY-MM>.md` includes a `cost-sweep` section listing what was found, what was deleted, what was kept (with ADR ref).
- **If we miss.** A skipped month triggers compliance-drift in §2.9 (rhythm cadence).

### §2.7 Rightsizing cadence — quarterly, against recommender

- **Claim.** Every quarter, CSRE MUST review cloud-native rightsizing recommendations (GCP Active Assist Recommender, AWS Compute Optimizer, Azure Advisor) for every shipped project and either apply them or file a justification ADR (`rightsizing-decline-<resource>-<date>.md`) explaining why the current size is correct.
- **How to verify.** Quarterly retrospective (`_meetings/retrospective-YYYY-QN.md`) includes a rightsizing-actions row per project.
- **If we miss.** Same as §2.6 — surfaces in monthly audit, escalates to drift after two missed quarters.

### §2.8 Storage tiering — lifecycle policies on every persistent bucket

- **Claim.** Every persistent object-storage bucket the Agency creates MUST have a lifecycle policy moving objects to colder/cheaper tiers based on access age (typical: 30d → Nearline/Infrequent-Access, 90d → Coldline/Glacier-Instant, 365d → Archive/Glacier-Deep). Buckets containing logs/audit-trails MUST set retention-with-hold rather than hard deletion.
- **How to verify.** `<slug>/infra/storage-lifecycle.tf` or equivalent. Spot-check via `gcloud storage buckets describe gs://<bucket> --format='value(lifecycle)'`.
- **If we miss.** CSRE files `lifecycle-missing` ADR; bucket is brought into compliance within 7 days.

### §2.9 Managed services preferred — bias to serverless / managed

- **Claim.** When the Architecture council picks a runtime, **managed and serverless options** (Cloud Run, GKE Autopilot, Cloud Run functions, Lambda, Fargate, Spanner, BigQuery, Aurora Serverless v2) MUST be the default. Choosing self-managed (Compute Engine, EC2, K8s on raw VMs, self-hosted DBs) requires an ADR (`runtime-choice-self-managed-<slug>.md`) explaining the technical reason and the operational cost it accepts in exchange for the saved infrastructure cost.
- **How to verify.** Project's architecture ADR records the choice and (if self-managed) the rationale. CSRE reviews these ADRs at the quarterly cost retrospective.
- **If we miss.** Architecture decision is reopened; if no defensible rationale exists, the project migrates to a managed alternative on the next maintenance window.

### §2.10 Commitment strategy — long-running workloads use CUDs/RIs

- **Claim.** Any compute workload that has been running for ≥ 6 months at predictable utilization MUST be reviewed quarterly for committed-use discount coverage (GCP CUDs, AWS Reserved Instances / Savings Plans, Azure Reservations). Coverage decisions are recorded in the quarterly retrospective.
- **How to verify.** Quarterly retrospective `cost-commitments` section lists each long-running workload, its current commitment coverage, and the next decision date.
- **If we miss.** Money is left on the table; CAO flags it in the next monthly audit. Not a hard ship-block but a measurable miss.

### §2.11 No silent overruns — same-day User notification on > 50% MoM jumps

- **Claim.** Any month-over-month cloud spend increase greater than **50%** on any project the Agency owns MUST notify the User the same business day, via `inbox.json` priority `cost-spike`, with a preliminary cause-analysis attached.
- **How to verify.** `runtime-hooks/cost-gate/spike-detector.sh` (added in v0.5.5) runs daily on the billing export and writes to `inbox.json` when triggered. CAO cross-checks `inbox.json` cost-spike entries against the billing export at the monthly audit.
- **If we miss.** Silent overrun = ASI-class finding (analogous to §2.10 of TRUST.md "loudly, not silently") → CRT review → User notified the next session.

### §2.12.5 Cross-vendor model spend (added v0.6.0)

- **Claim.** Any project that invokes `skills/cross-model-panel` in `cross-vendor` mode (per [`skills/cross-model-panel/references/cross-vendor-panel.md`](skills/cross-model-panel/references/cross-vendor-panel.md)) MUST line-item OpenRouter spend separately from direct-Anthropic spend in `<slug>/cost-estimate.md`. The two cost categories MUST be tracked as distinct rows in the billing data feeding the spike-detector — a 50% jump in OpenRouter spend in a project that previously had zero OpenRouter spend is a §2.11 spike independent of total spend.
- **How to verify.** `<slug>/cost-estimate.md` has explicit `direct_anthropic_usd` and `openrouter_usd` rows in its line-item breakdown when cross-vendor is in use. The `manual-billing.csv` (or BigQuery export equivalent) carries `vendor` as a column. CAO spot-checks at quarterly cost scorecard.
- **If we miss.** Cross-vendor spend lumped under "AI" without vendor split = compliance-drift; CSRE files `cost-vendor-attribution-missing` ADR. Repeated misses route through Rung 3 of the never-give-up ladder.
- **Setup gate.** Before any project enables `cross-vendor` mode, the User MUST provision `OPENROUTER_API_KEY` in vault refs (per Constitution §8.5 non-waivable raw-secret class) AND set a per-project budget cap in OpenRouter's dashboard (recommend $50/month default; raise on need). Setup checklist is in [`cross-vendor-panel.md`](skills/cross-model-panel/references/cross-vendor-panel.md).

### §2.12 No cost optimization at the expense of higher pillars

- **Claim.** Cost optimization MUST NOT override Security & Privacy or Design (per `VALUES.md` §12 build-order). The Agency MUST NOT skip a pen-test, downgrade a managed-DB to an unmanaged-DB on a security-critical workload, remove redundancy from a production tier, or weaken accessibility — to reduce cost. Cost cuts MUST come from waste reduction, rightsizing, commitment strategy, or scope cuts approved by the CEO + User.
- **How to verify.** Every cost-driven architectural change MUST cite `VALUES.md §12` in its ADR and explain which lower-priority concern (Operations or Timely Delivery) is yielding. ADRs that cite cost as the reason for downgrading Security or Design MUST be rejected by CISO/CRT.
- **If we miss.** This is the cost analogue of §2.4 USER-ONLY actions — cost-driven security downgrade is non-waivable except via Article X (USER-ONLY Constitution amendment). Any such decision is auto-routed to CISO + CRT + User.

---

## 3. The cost scorecard

A quarterly **cost scorecard** is published alongside the trust scorecard (`TRUST.md` §3) every Jan/Apr/Jul/Oct 22. The first cost scorecard publishes **2026-07-22**.

The scorecard reports, per project active that quarter:

- Estimate vs actual spend (with variance)
- Idle-resource sweep findings + actions (§2.6)
- Rightsizing actions taken or declined (§2.7)
- Commitment coverage status (§2.10)
- Any cost-spike alerts triggered (§2.11)
- Any cost-driven architecture changes that touched a higher pillar (§2.12)

The cost scorecard is published to `_meetings/cost-scorecard-YYYY-QN.md` and linked from `TRUST.md` §3 alongside the trust scorecard.

---

## 4. What this document is not

- **Not a billing system.** The Agency does not pay your cloud bill. You hold the billing account; we operate within it.
- **Not a magic optimizer.** A 50% cost reduction is rarely available without architectural change. Most savings come from removing waste (§2.6), choosing right-sized resources (§2.7), and using managed services (§2.9).
- **Not a substitute for FinOps maturity.** A user with a serious cloud-cost program will run their own FinOps cadence. This document defines what the Agency commits to as a participant in that program.

---

## 5. Push back

If a commitment in §2 is ambiguous, missing, mis-targeted, or routinely missed, you can:

1. File an issue against the repo with label `cost-commitment-feedback`.
2. Open `inbox.json` priority `cost-amend-request` in any project folder.
3. Mention `@CSRE` or `@CAO` in any meeting prompt.

CSRE owns this document. CAO audits its application. The User can amend it at any time via `cost-amend` ADR.

---

## 6. Sources & influences

- **Google Cloud Well-Architected Framework — Cost Optimization pillar.** Source of the four core principles (alignment with business value, culture of cost awareness, optimize resource usage, optimize continuously) and the validation-checklist structure. Apache-2.0; see `LICENSES/APACHE-2.0-google-skills.txt`. Original at <https://docs.cloud.google.com/architecture/framework/cost-optimization>.
- **FinOps Foundation Framework.** Source of the FinOps cycle (inform → optimize → operate) and the principle of cross-team accountability for cloud spend. CC BY 4.0. <https://www.finops.org/framework/>.
- **AWS Well-Architected Framework — Cost Optimization pillar** and **Microsoft Azure Well-Architected Framework — Cost Optimization pillar.** Cross-checked for shared principles; nothing copied verbatim.
- **`TRUST.md` (this repo, v0.5.0).** Structural template — Claim / How-to-verify / If-we-miss tripartite, RFC 2119 grammar, USER-amendable, quarterly scorecard, "what this document is not" closer.

End of `COST-AWARENESS.md` v1.0 — ratified 2026-04-23 with plugin v0.5.5.
