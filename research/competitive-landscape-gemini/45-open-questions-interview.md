# Open Questions — the one-at-a-time interview (AFTER the reports)

**Purpose:** the Sovereign asked to be **interviewed one question at a time** to define every term before we design — but only *after* reading this research pack. This doc is the backbone for that conversation. The CEO asks **Q1, waits, then Q2** — never a wall of questions.

**Rule of the interview:** each answer becomes a defined term in a future `GLOSSARY.md` / vision doc. No design work starts until the blocking questions (Q1–Q5) are answered.

---

## Block 1 — What "the OS" is (blocking)

**Q1. Which build form is "the OS"?** A (experience-layer app on the user's current OS), B (bootable custom Linux distro), C (cloud-streamed custom Linux, à la Warmwind), or A→B/C as a staged path? *(See doc 40 §4. Recommendation: A as on-ramp, B/C as destination, on a reused Linux kernel.)*

**Q2. How deep does the company recurse, and what is a "one-task leaf"?** The repo currently caps depth at 3 (CEO→Chief→Specialist→Worker), deeper requires an ADR (`AGENTS.md:48,105`). Your vision says "recurse until the lowest employee does exactly one task." Do we lift the cap to *dynamic* recursion, and how do we define "one task" so leaves don't fragment infinitely? *(Note: The source repository's own depth-cap wording is ambiguous -- is it counted from CEO or from Chief? The design interview must resolve this.)*

## Block 2 — Who it's for (blocking)

**Q3. Primary pitch target and audience.** "A personal AI OS everyone wants" — but who is the *beachhead*? (e.g., solo founders / power users / privacy-conscious professionals first, then everyone?) This sets the whole UX and trust story.

## Block 3 — The trust wedge made concrete (blocking)

**Q4. Concrete trust + security model.** What does "trustable" mean operationally to you — per-agent least-privilege? a dedicated **Chief Trust Officer** (doc 46)? a visible verifier on every output? receipts the user can replay/reverse? all of the above, and in what priority?

**Q5. Which PQC layers, and on what timeline?** Identity, transport (TLS), data-at-rest, inter-agent comms — all four, or a subset first? Hybrid (classical+PQC) at launch? (See doc 41; NIST standards are final, no rival ships this.)

## Block 4 — Composition & sovereignty (shapes design, non-blocking)

**Q6. The first executive roster the user "hires" as Chairman.** Start from the repo's 16 Chiefs + the four candidate adds (Chief Trust Officer, CAIO, Chief Privacy Officer, Chief Experience Officer — doc 46 §3)? Or a leaner founding board?

**Q7. Local / cloud / hybrid + data sovereignty.** Must it run offline? Where does user data live? (Warmwind is cloud-only; that's a gap we can take — doc 10.) Does "sovereign" mean self-hosted, or just user-owned keys?

## Block 5 — Naming & identity (shapes brand, non-blocking)

**Q8. Names.** The OS, the company, the AI employees, the board/CEO, the verifier, and "the building" (the workspace metaphor). The category name matters as much as the product name (doc 44).

## Block 6 — Scope guards (so we don't overbuild)

**Q9. Explicit non-goals.** What are we deliberately *not* doing in v1? (e.g., not a real device OS / Category 1; not enterprise multi-tenant; not a model lab.) Accepting a non-goal is a USER-ONLY action (`GOVERNANCE.md`).

**Q10. Success definition for v1.** What does the first shippable version do, for whom, that proves the thesis ("a trustable AI company you chair")?

---

## How the answers flow into design

```
Q1 → doc 40 build-form decision → architecture spike
Q2 → recursion model → amend AGENTS.md depth cap (USER-ONLY, via ADR)
Q3 → audience → positioning canvas (doc 44) finalized
Q4+Q5 → trust spec → new Chief Trust Officer council + PQC ADR
Q6+Q7 → founding board + deployment model
Q8 → GLOSSARY.md + brand
Q9+Q10 → vision doc + v1 scope lock
```

Nothing here is decided yet — these are the questions, in order, for the conversation that follows the pack.
