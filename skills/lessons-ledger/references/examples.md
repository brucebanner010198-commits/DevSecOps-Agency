# lessons-ledger/references/examples.md

Three worked examples: one shipped, one blocked, one parked-rung-7. Illustrative only — not committed to the actual `LESSONS.md`.

## Example 1 — shipped (clean run)

```markdown
### invoice-splitter — 2026-04-21

| Field | Value |
| --- | --- |
| outcome | shipped |
| council-lead ship | CISO=green, GC=green |
| okr-alignment final | green |
| rungs traversed | 0 |
| fix-loops (sum) | 2 |
| waivers | 0 — none |
| stones authored | none |
| lessons | OAuth at Phase 2 (not Phase 4) saved the CISO gate. `_meetings/invoice-splitter-retro-2026-04-21.md:§Lessons:1`<br>Vercel deploy cut Ship phase by 40% vs prior Fly.io baseline. `_meetings/invoice-splitter-retro-2026-04-21.md:§Lessons:2` |
| reusable decisions | ADR-0042 — Vercel over Fly.io for < 10k MAU side-projects. `_decisions/ADR-0042-vercel.md` |
| what we'd change | Baseline perf run at Phase 3 entry, not Phase 4. `_meetings/invoice-splitter-retro-2026-04-21.md:§What we'd change:1` |
| next-run trigger | - |
```

## Example 2 — blocked (never reached Ship)

```markdown
### dorms-chat-app — 2026-03-18

| Field | Value |
| --- | --- |
| outcome | blocked |
| council-lead ship | CISO=red, GC=- |
| okr-alignment final | yellow |
| rungs traversed | 1-5 |
| fix-loops (sum) | 6 |
| waivers | 0 — none |
| stones authored | 1 — _vision/playbooks/stones/ASI01-session-fixation-2026-03.md |
| lessons | Session-fixation found at Phase 4 — CISO ladder-walked to Rung 5 without resolution. `_meetings/dorms-chat-app-retro-2026-03-18.md:§Loops & rungs`<br>User declined waiver at Rung 4 — correct call per VALUES §2. `_decisions/ADR-0031-user-decline-waiver.md` |
| reusable decisions | ADR-0033 — session-fixation kill-switch must be in auth library selection rubric. `_decisions/ADR-0033-auth-rubric.md` |
| what we'd change | Run STRIDE S1 (spoofing) check at Phase 2 architecture review, not at Phase 4. `_meetings/dorms-chat-app-retro-2026-03-18.md:§What we'd change:1` |
| next-run trigger | - |
```

## Example 3 — parked-rung-7 (preserved for future revival)

```markdown
### video-conferencing-mvp — 2026-02-28

| Field | Value |
| --- | --- |
| outcome | parked-rung-7 |
| council-lead ship | CISO=yellow, GC=- |
| okr-alignment final | red |
| rungs traversed | 1-7 |
| fix-loops (sum) | 4 |
| waivers | 0 — none |
| stones authored | none |
| lessons | Market scope too broad — CSO did not surface the Zoom competitive dominance at idea-pipeline stage. `_meetings/video-conferencing-mvp-retro-2026-02-28.md:§Gated:2` |
| reusable decisions | ADR-0028 — require competitive-analyst to score OSSR (odds-of-surviving-the-incumbent) before any idea reaches top-5. `_decisions/ADR-0028-ossr-scoring.md` |
| what we'd change | Add OSSR to idea-pipeline pre-flight. `_meetings/video-conferencing-mvp-retro-2026-02-28.md:§What we'd change:1` |
| next-run trigger | If a new modality (WebRTC improvement, edge-video codec) changes the competitive shape, CSO reopens under new slug. |
```

## Example 4 — correction row

For a previously shipped project where a post-deploy incident revealed a hidden issue:

```markdown
### invoice-splitter — 2026-05-12

| Field | Value |
| --- | --- |
| outcome | shipped-corrected |
| council-lead ship | CISO=yellow, GC=green |
| okr-alignment final | yellow |
| rungs traversed | 0 |
| fix-loops (sum) | 0 |
| waivers | 0 — none |
| stones authored | 1 — _vision/playbooks/stones/ASI04-prompt-injection-invoice-2026-05.md |
| lessons | [correction] Post-deploy red-team found a prompt-injection vector in PDF parsing — did not surface in pre-release red-team. Corrects LESSONS.md > invoice-splitter-2026-04-21. `_vision/audit/incident-INC-0017.md` |
| reusable decisions | ADR-0054 — add PDF-parser injection probe to CRT pre-release suite. `_decisions/ADR-0054-pdf-probe.md` |
| what we'd change | Add adversarial PDF samples to CRT probe catalogue before any project with PDF parsing ships. `_meetings/incident-INC-0017-retro-2026-05-12.md:§What we'd change:1` |
| next-run trigger | - |
```

Note: the correction row does not edit the original. Both rows remain; readers see both and the lineage is explicit.

## Non-examples (what not to write)

**Too vague:**

```
| lessons | We learned a lot about auth. |
```

Fails — no cited behaviour.

**Too long:**

```
| lessons | Authentication is a complicated concern that touches many parts of the system including the login flow, session management, token rotation, and ... (300 more chars) |
```

Fails — exceeds 120 chars per cell. Detail belongs in the retro minutes and `_memory/patterns/<slug>.md`.

**Editing a prior row:**

```
- Open LESSONS.md
- Find invoice-splitter row
- Change "green" to "yellow" because a post-deploy issue emerged
- Save
```

Fails — violates append-only. Correct move: write a correction row with a new `closedAt`.
