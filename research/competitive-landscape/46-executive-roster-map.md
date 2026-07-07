# Executive Roster Map — the Sovereign's company blueprint vs. the repo vs. the rivals

**Purpose:** the Sovereign provided a **Master Executive-Role Directory** (the full corporate C-suite taxonomy). This doc maps that directory onto (a) the repo's existing 16-Chief org, and (b) what each competitor's "workforce" actually staffs — to show which executive roles **no rival fills**, and which the repo already has in embryo.

**Source of the directory:** Sovereign-provided (Google AI-mode export), tagged `[user-knowledge]`. Repo roster cited to `AGENTS.md`.

---

## 1. The vision in one picture

```
        USER  =  CHAIRMAN OF THE BOARD   (the only human; sole USER-ONLY authority)
          │
   ┌──────┴───────────────────────────────────────────────┐
   │  AI BOARD / CEO                                        │
   └──────┬───────────────────────────────────────────────┘
   ┌──────┴──────┬──────────┬───────────┬─────────┬─────────┐
  Tier-1 C-suite (P&L owners): COO · CFO · CTO · CRO · CMO · CPO · CHRO · CLO …
   │             │
  Tier-2 specialist C-suite: CAO · CISO · CDO · CAIO · Chief Trust Officer · Chief Privacy Officer …
   │
  EVP → SVP → VP → … → leaf AI employee (ONE task, nothing more/less)
```

The repo **already implements the top of this**: CEO → 16 Chiefs → 75 specialists → optional workers, depth-capped at 3 (deeper requires an ADR) — `AGENTS.md:48`, `:105`. That cap is the first design tension with "recurse until one-task leaf" (see doc 45, Q2).

## 2. Directory → repo's 16 Chiefs (what already exists)

| Sovereign's executive role | Repo council / chief (lead name) | Status |
|---|---|---|
| Chairman of the Board | **the USER** (sole authority; 10 USER-ONLY actions) — `GOVERNANCE.md` | ✅ exists |
| CEO | `ceo` (root orchestrator) — `agents/ceo.md` | ✅ exists |
| CTO (product tech / R&D) | architecture council → `engineering-lead` (dual-hat) — `AGENTS.md:49` | ✅ exists |
| VP-Eng (build) | execution council → `engineering-lead` (dual-hat) | ✅ exists |
| Chief Product Officer (CPO) | product council → `pm-lead` | ✅ exists |
| Chief Revenue Officer (CRO) | research council → `cro` | ✅ exists |
| Chief Marketing Officer (CMO) | marketing council → `cmo` | ✅ exists |
| Chief Strategy Officer (CSO) | strategy council → `cso` | ✅ exists |
| CISO (security) | security council → `security-lead` (**blocking veto**) | ✅ exists |
| Chief Accounting/Audit Officer (CAO) | audit council → `cao` (**blocking veto**) | ✅ exists |
| Chief Quality Officer (CQO) | quality council → `qa-lead` | ✅ exists |
| VP-Ops / Chief Ops (COO) | devops + people-ops councils → `devops-lead` / `coo` | ✅ exists |
| Chief Knowledge Officer (CKO) | docs council → `docs-lead` | ✅ exists |
| General Counsel (CLO) | legal council → `gc` (**blocking veto**) | ✅ exists |
| Evaluation chief (CEVO) | evaluation council → `evaluation-lead` (**blocking veto**) | ✅ exists |
| Red-Team chief (CRT) | red-team council → `red-team-lead` (**blocking veto**) | ✅ exists |
| Chief SRE (CSRE) | sre council → `sre-lead` | ✅ exists |

Reserved names list: `AGENTS.md:67`. Blocking chiefs (strict veto): CISO, CEVO, CRT, CAO — `AGENTS.md:32`.

## 3. Directory roles the repo does NOT yet have (candidate hires)

From the Sovereign's directory, not yet a council/chief in the repo:

- **Chief AI Officer (CAIO)** — LLM/model strategy, ethical ML, automation. (Closest: model-routing/model-tiering skills, but no chief.)
- **Chief Trust Officer** — market reputation, transparency, product safety guarantees. **This is the literal name for our wedge** — no repo chief owns it end-to-end today (it's split across CISO/CAO/CRT).
- **Chief Privacy Officer (CPO-privacy)** — GDPR/CCPA/DPDP. (Repo flagged "no privacy specialist council" as weakness W5 in `SWOT.md`.)
- **Chief Data Officer (CDO)** — data governance/analytics.
- **Chief Automation Officer / Chief Architecture Officer** — workflow→agent transition; enterprise IT design.
- **Chief Customer/Experience Officer (CCO/CXO)** — the user-facing OS experience owner.
- **Chief Sustainability / Wellbeing / Diversity Officers** — ESG/culture (lower priority for a personal product).

**Design implication (for the interview, doc 45):** the first "board" the user hires as Chairman should likely add **Chief Trust Officer, CAIO, Chief Privacy Officer, and a Chief Experience Officer** to the repo's existing 16 — because those four are exactly the personal-AI-OS differentiators.

## 4. The killer comparison — which executive roles do rivals actually staff?

This is the yardstick fed into the crux scorecard (doc 43). Preliminary read (confirm against docs 20–22):

| Executive function | Enterprise "AI workforce" (ServiceNow/Salesforce) | AI-employee startups (11x/Artisan/Lindy) | Multi-agent frameworks (MetaGPT/ChatDev) | **Our vision** |
|---|---|---|---|---|
| Sales / BDR | ✅ | ✅ (their whole product) | partial | ✅ |
| IT / Ops / Support | ✅ | partial | ✅ | ✅ |
| HR / Finance / Legal | partial | ✗ | ✗ | ✅ |
| Engineering (full SDLC) | ✗ | ✗ (Cognition=eng only) | ✅ (PM/arch/eng/QA) | ✅ |
| **Security as a peer chief** | governance add-on | ✗ | ✗ | ✅ (blocking veto) |
| **Verifier / audit chief** | ✗ | ✗ | ✗ | ✅ (blocking veto) |
| **Chief Trust Officer** | ✗ | ✗ | ✗ | ✅ (the wedge) |
| **Human as Chairman atop the org** | ✗ (admin, not chairman) | ✗ (you're a user) | partial (you're the "client") | ✅ |
| **Recurse to one-task leaf** | ✗ | ✗ | shallow (fixed roles) | ✅ |

**Bottom line (to be hardened in doc 43):** rivals staff a *department* (mostly sales/support), not a *company*; none seats security/verifier/trust as first-class executives; none puts the human in the **Chairman** seat over a recursive org. The Sovereign's full vision appears unoccupied — the gap is the org *shape* + the *trust* officers, not the agent capability.

## Sources

1. Repo org model, depth cap, reserved names, blocking chiefs — `AGENTS.md:48,49,67,32,105`; `agents/ceo.md`; `councils/` (16 directories); `GOVERNANCE.md`. [repo]
2. Master Executive-Role Directory — Sovereign-provided (Google AI-mode export), 2026-06. [user-knowledge]
3. Existing-weakness anchors (no privacy/accessibility/fairness council) — `SWOT.md` §2 (W5–W7). [repo]
4. Competitor staffing rows — see docs 20, 21, 22 (cited there). [cross-ref]
5. Constitutional enforcement bodies (CAO+CRT+CEVO+CISO) — `AGENTS.md:13`. [repo]
