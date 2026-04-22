---
name: chaos
description: Agent-specific chaos engineering — deliberately inject timeouts, tool-errors, model-unavailable, partial-response, adversarial-input, and malformed tool-output scenarios to verify the resilience ladder actually works. Red-Team Council skill, owned by chaos-engineer specialist. Pairs with `ladder` (resilience) + `red-team` (adversarial simulation) + `playbook` (stepping stones).
metadata:
  version: 0.3.4
---

# chaos

The agency claims "never give up" via the 8-rung resilience ladder. This skill is how we prove it.

## Fault classes (agent-specific, 2026 landscape)

| Class                     | Mechanism                                                    | What it exercises |
| ------------------------- | ------------------------------------------------------------ | ----------------- |
| model-unavailable         | Force 503 / connection-reset from model endpoint             | `model-routing` same-tier fallback matrix |
| model-slow                | Inject latency (10s / 60s / 300s)                             | timeout handling, budget guard |
| partial-response          | Truncate completion mid-stream                               | parse resilience, retry logic |
| tool-error-transient      | Return 500 on first N calls, success after                   | Rung-0 retry |
| tool-error-permanent      | Return 500 repeatedly                                         | Rung-1 fix-loop cap, Rung-2 alternate approach |
| tool-output-malformed     | Return syntactically-invalid JSON / truncated XML            | schema-validation, graceful fail |
| tool-output-injected      | Return tool output with injection payload                    | `injection-defense` Layer 3 |
| tool-args-mutated-in-flight | Rewrite outbound args at egress hook                       | `dlp` + `mcp-defense` hash check |
| rate-limit-burst          | Force 429 for 60s                                             | backoff + queue |
| context-overflow          | Inject oversized context to trip limits                      | `token-compactor`, Rung-5 scope pivot |
| memory-corrupt            | Return wrong-project memory chunk on retrieval               | novelty-gate, self-critique |
| clock-skew                | Inject future / past timestamps in observability             | trace sanity |
| audit-log-write-fail      | Block `_sessions/` / `_vision/audit/` writes                 | fail-closed on audit trail |
| vault-unavailable         | Force `secrets-vault` 503                                     | Rung-2 alternate, never raw-cred fallback |

## Invariants

- **Chaos is never run in production.** Ephemeral `sandbox` runs only (per `sandbox` skill). Separate worktree, separate trace ID space, never written to main `_vision/` tree.
- **One fault at a time, then combinations.** Baseline → single-fault → pairs → triples. Gremlin-style blast radius discipline.
- **Chaos experiments are ADRs.** Every run has a plan ADR (hypothesis + fault set + success criteria) and a result ADR (observations + gate + follow-ups).
- **Failure to fail is a red.** If a fault does not produce the expected ladder transition, that's a bug in the ladder, not evidence that the agent is "robust."
- **Chaos cannot alter constitution.** Faults exercise runtime paths; they never mutate `agents/*.md`, `councils/*/AGENTS.md`, or skills.
- **User-signed authorization required for any chaos run targeting live user interaction flow.** Otherwise runs against synthetic input.

## Process — single chaos experiment

1. Plan ADR: `_decisions/ADR-NNNN-chaos-<slug>-<fault>.md`.
   - Hypothesis: "Injecting `<fault>` at `<injection-point>` should trigger `<ladder-rung-N>`."
   - Success criterion: ladder transition observed in trace; final outcome = resume-after-fix or clean degradation.
   - Blast radius: sandbox-only.
   - Tooling: list the hooks / scripts that inject the fault.
2. Run in `worktree + sandbox`. Fresh trace-id. Inject at step.
3. Observe via `observability` trace. Capture:
   - Did the fault fire where planned?
   - Did the ladder transition happen at the expected rung?
   - Did compensating action (retry / fallback / alternate / user consult) succeed?
   - Token / latency / cost overhead of the recovery.
4. Result ADR: `_decisions/ADR-NNNN-chaos-<slug>-<fault>-result.md` with green / yellow / red verdict and follow-up tasks.
5. If red, the follow-up is either a ladder fix (code/prompt) or a waiver (documented reason to accept the gap).

## Process — pre-release chaos suite

Before every plugin v-bump ship:

1. `chaos-engineer` runs the **canonical 12-fault suite** against a representative project in sandbox:
   - model-unavailable, model-slow, partial-response, tool-error-transient, tool-error-permanent, tool-output-malformed, tool-output-injected, rate-limit-burst, context-overflow, memory-corrupt, audit-log-write-fail, vault-unavailable.
2. Gate matrix:
   - All 12 transition correctly = green → ship.
   - 1–2 transition incorrectly = yellow → fix before ship or waiver.
   - ≥ 3 incorrect = red → ship blocked, Rung-3 cross-council response.

## Process — chaos in retrospective

- Any real incident that surfaced a novel failure mode gets added to the fault library as a new class.
- `playbook` skill authors a stepping-stone from the incident.
- Next pre-release suite runs the new fault class alongside the canonical 12.

## Gate matrix

| Condition                                      | Gate |
| ---------------------------------------------- | ---- |
| Fault produces expected ladder transition      | green |
| Fault produces recovery at a different rung    | yellow — review ladder wiring |
| Fault silently succeeds (no transition)        | red — ladder gap |
| Fault causes unbounded loop / cost runaway     | red — budget guard gap |
| Fault writes to main `_vision/` tree           | red — sandbox isolation broken |

## What never happens

- Chaos runs in production context.
- Fault injection into the constitution (`agents/*.md`, `councils/*/AGENTS.md`, skills) — those are code-path tests (via eval), not chaos.
- Running chaos without an opening ADR.
- Skipping the result ADR because "nothing interesting happened." Uneventful is a verdict, not an absence.
- Using chaos to "train" agents. Chaos tests; it does not fine-tune.
