---
name: gates
description: >
  Internal skill. Single source of truth for gate vocabulary, per-council
  blocking rules, and gate aggregation at the project level. Invoked by the CEO
  after every Chief report to classify and aggregate gates, and by the
  command-center when rendering status. Do not invoke directly from the user
  surface.
metadata:
  version: "0.2.3"
---

# gates — what the colors mean and what they block

Every council hands the CEO a gate signal. This skill defines the exact meaning of each color, which councils can block a ship, and how the CEO computes an overall project gate from the set.

The rules here are authoritative. If a council's `AGENTS.md` contradicts this file, the council's file is narrower (describes **that** council's heuristic); this file describes the **aggregate** contract.

## Vocabulary

| Color    | Meaning                                                                 |
| -------- | ----------------------------------------------------------------------- |
| `green`  | All Must items satisfied. Proceed.                                      |
| `yellow` | One or more Must items satisfied with a documented follow-up ticket. Proceed, carry the follow-up. |
| `red`    | A Must item is unsatisfied or a Must not was violated. Block until fixed or waived. |
| `n/a`    | The council did not run for this phase (e.g. GC skipped for internal-only). Not counted in aggregation. |

No other values. If you catch yourself wanting "orange" or "light-red", pick one of the four and explain in the `note`.

## Who can block ship

`CONSTITUTION.md` §3.3 names four **blocking** councils. A `red` from any of them stops the ship regardless of any other signal:

- **CISO** (`security-lead`) — Critical or High without mitigation, raw secrets, wildcard allowlists, missing SBOM + SLSA.
- **CEVO** (`evaluation-lead`) — a regression of 5 percentage points or more against baseline, a skill eval below threshold, or variance σ/μ above 0.15.
- **CRT** (`red-team-lead`) — an ASI-class finding, a self-red-team independence breach, or an unpinned-hash adoption.
- **CAO** (`cao`) — an append-only violation, a missing ADR for a material decision, or non-goal drift without an ADR.

**GC** (legal council) is informing, as the Constitution lists it (§3.4). A GPL/AGPL dependency in a closed-source ship, or a missing `PRIVACY.md` when PII is in the data model, is a GC red. Like any informing red, at release it is waived only by the User (§8.6).

Every other council produces gates that **inform** the ship decision but do not unilaterally block it. Their reds still aggregate into the project gate (see below). At release (§8.6), the CEO cannot override an informing red: only the User can waive it, through `skills/waivers`.

Blocking-council overrides require the user in `inbox.json`. The CEO cannot waive a red from CISO, CEVO, CRT or CAO, or an informing red at release, alone; §3.3 clears it only by a fix and a re-run, or a user-signed waiver under `skills/waivers`.

## Gate emission contract

Every Chief report writes one gate entry to `chat.jsonl`:

```json
{
  "ts": "<iso>",
  "scope": "exec",
  "from": "<chief>",
  "to": "ceo",
  "type": "report",
  "phase": "<phase>",
  "gate": "green | yellow | red | n/a",
  "artifacts": ["..."],
  "note": "<one sentence>",
  "followups": [
    {"id": "fu-001", "severity": "medium", "summary": "add structured log redaction for email field", "owner": "devops-lead"}
  ]
}
```

- `gate` is mandatory on every `type:"report"` entry.
- `followups` is required when `gate == "yellow"`. One entry per documented follow-up. Empty array for `green` and `red`.
- `note` is required and ≤ 140 characters. It is what the command-center shows in the meeting row.

If a Chief reports without a `gate`, the CEO treats it as `red` and bounces it back.

## Aggregation

At each phase close, the CEO computes the phase gate by combining all Chief reports for that phase. At project close, the CEO computes the project gate the same way across all phases.

Rules, in order:

1. If **any blocking-council** report is `red` with no user-granted waiver → project is `red`.
2. Else if **any** report is `red` → project is `red`.
3. Else if **any** report is `yellow` → project is `yellow`.
4. Else → project is `green`.
5. `n/a` reports are skipped entirely.

The aggregate lives in `status.json > gates`:

```json
{
  "gates": {
    "overall": "yellow",
    "byCouncil": {
      "research":     "green",
      "product":      "green",
      "architecture": "green",
      "security":     "yellow",
      "execution":    "green",
      "quality":      "yellow",
      "devops":       "green",
      "docs":         "green",
      "legal":        "green"
    },
    "byPhase": {
      "discovery":      "green",
      "design":         "green",
      "build":          "green",
      "verify":         "yellow",
      "ship":           "green",
      "document-legal": "green"
    },
    "followups": [
      {"id": "fu-001", "from": "devops", "severity": "medium", "summary": "add structured log redaction for email field", "owner": "devops-lead", "state": "open"},
      {"id": "fu-002", "from": "quality", "severity": "low",   "summary": "one a11y contrast issue on empty state", "owner": "a11y-auditor",  "state": "open"}
    ],
    "waivers": []
  }
}
```

`followups` is the source of truth for the follow-up queue. `/devsecops-agency:retro` pulls from it.

## Waivers

A waiver is an explicit CEO-logged override of a `red` from a non-blocking council, recorded after the user accepts the risk in `inbox.json`.

```json
{"ts":"<iso>","scope":"exec","from":"ceo","to":"<chief>","type":"waiver","gate":"red","reason":"user accepted: tutorial red because feature is behind a flag","waivedBy":"user","inboxItem":"inbox-004"}
```

A waiver turns a `red` into effectively `yellow` for aggregation and forces a `followups` entry. Blocking-council reds cannot be waived by the CEO alone — they require a user waiver via `inbox.json`.

## Re-gate on fix-loop

When a Chief re-runs after a fix attempt, the new report supersedes the previous one. The superseded report remains in `chat.jsonl` (append-only) but the aggregator uses the latest report per (council, phase) pair.

## Invocation points (for the CEO)

- After every Chief report: validate gate color, require `followups` on yellow, re-run aggregation, update `status.json > gates`.
- At each phase close: emit a `exec-decision` entry with the phase's aggregate gate.
- At project close: emit the overall gate and include it in the user-facing summary.

## Progressive disclosure

- `references/gate-rules.md` — per-council Must/Must-not trigger matrix (blocking vs informing).
- `references/aggregation.md` — worked examples (yellow vs red propagation, waiver handling, n/a skipping).
