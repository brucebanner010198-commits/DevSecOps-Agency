# Board phases — full spec

The CEO runs 7 phases. Each phase has **inputs**, **Chiefs invoked**, **artifacts produced**, and an **exit criterion**. Do not advance past a phase whose exit criterion has failed.

---

## Phase 1 — Discovery

**Inputs**
- `brief.md > ## Idea` and `## Intake`

**Chiefs (parallel)**
- `cro` — runs Research Council
- `pm-lead` (CPO) — runs Product Council (strategy + roadmap)

**Artifacts**
- `research-brief.md`, `research/market.md`, `research/tech-landscape.md`, `research/prior-art.md`, `research/user-needs.md`
- `product/strategy.md`, `product/roadmap.md`, `brief.md > ## Functional spec`

**Exit criterion**
- CRO gate: not red
- Product v1 scope is concrete (features enumerated with acceptance criteria)

---

## Phase 2 — Design

**Inputs**
- `brief.md`, `research-brief.md`, `product/strategy.md`, `product/roadmap.md`

**Chiefs (sequential)**
1. `engineering-lead` (CTO hat) — runs Architecture Council (system / api / data / infra)
2. `security-lead` (CISO) — runs threat-modeler + compliance-officer against the architecture

**Artifacts**
- `architecture.md`, `architecture/data-model.md`, `architecture/infra.md`, `docs/api/*` stubs
- `threat-model.md`, `security/compliance.md`

**Exit criterion**
- CISO gate: no Critical/High unmitigated risk
- CTO gate: API surface + data model + infra choice pinned

---

## Phase 3 — Build

**Inputs**
- All phase-2 artifacts

**Chiefs**
- `engineering-lead` (VP-Eng second hat) — dispatches backend-dev, frontend-dev, db-engineer, integrations-engineer in parallel where safe

**Artifacts**
- `src/` — working code

**Exit criterion**
- Project builds locally
- All planned endpoints exist
- No business logic imports a vendor SDK directly (integrations shim is in place)

---

## Phase 4 — Verify

**Inputs**
- `src/`, `test-matrix.md`, `threat-model.md`

**Chiefs (parallel)**
- `qa-lead` (CQO) — test-designer, test-runner, performance-tester, a11y-auditor
- `security-lead` (CISO second pass) — code-auditor + pen-tester on the built code

**Artifacts**
- `tests/`, `qa-report.md`, `qa/perf-report.md`, `qa/a11y-report.md`
- `security/code-audit.md`, `security/pentest-report.md`

**Exit criterion**
- P0 tests all green
- CISO gate: no Critical/High open
- CQO gate: green or documented yellow with rationale

---

## Phase 5 — Ship

**Inputs**
- `src/`, `architecture/infra.md`

**Chiefs**
- `devops-lead` (VP-Ops) — ci-engineer, deployment-engineer, observability-engineer

**Artifacts**
- `.github/workflows/ci.yml` (or platform-equivalent), `deploy/*`, `deploy/observability.md`

**Exit criterion**
- CI is green on the commit
- Rollback plan exists and is documented
- Health endpoints return 200 locally

---

## Phase 6 — Document + Legal

**Inputs**
- All prior artifacts

**Chiefs (parallel)**
- `docs-lead` (CKO) — api-documenter, readme-writer, tutorial-writer
- `gc` — license-checker, privacy-counsel

**Artifacts**
- `README.md`, `docs/api/*`, `docs/tutorial/getting-started.md`
- `legal/licenses.md`, `legal/privacy.md`, `PRIVACY.md` (if needed)

**Exit criterion**
- CKO gate: README commands verified against repo
- GC gate: not red

---

## Phase 7 — Close

**Inputs**
- Everything

**Owner**
- CEO only

**Artifacts**
- Final `status.json` with `phase: "delivered"`
- Final summary message to the user

**Exit criterion**
- User has a link to the repo and a summary
