---
name: capacity
description: This skill should be used when the COO (or `roster-manager` on COO's behalf) needs agency-wide capacity signals — who is overloaded, who is idle, which councils are bottlenecks, which KRs have insufficient coverage. Trigger phrases include "capacity check", "are we overloaded", "who is idle", "do we have bandwidth for another project", "bottleneck", "utilization", "bandwidth". Wired into roster checkpoint (every run) and into idea-pipeline pre-flight (does the agency have capacity to execute top-5 in parallel?).
metadata:
  version: 0.3.0-alpha.3
---

# capacity — utilization + bottleneck detection

Capacity is a read-only signal skill. It does not mutate the roster; it tells `roster-manager` + `hiring-lead` where the pressure is.

## When to trigger

- Roster checkpoint (every run) — supplies the `Utilization` column in `census.md`.
- Idea-pipeline pre-flight — does the agency have capacity to run multiple top-5 candidates in parallel? If not, CEO must sequence.
- User asks "can we take on another project" — CEO dispatches COO dispatches `roster-manager` which reads capacity.
- On any Chief reporting `gate: yellow` with reason "too many parallel dispatches" — reactive.

## Capacity bands

Measured per agent over the last 30 days:

| Band          | Dispatches in window | Signal                                      |
| ------------- | -------------------- | ------------------------------------------- |
| idle          | 0                    | Repurpose/fire candidate if 3+ quarters     |
| low           | 1–2                  | Healthy for niche/specialist roles          |
| healthy       | 3–7                  | Target band for most specialists            |
| hot           | 8–14                 | Watch — potential bottleneck                |
| overloaded    | > 14                 | Hire / clone / prompt-upgrade to split scope |

Per Chief over the last 30 days:

| Band          | Dispatches in window |
| ------------- | -------------------- |
| healthy       | 4–20                 |
| hot           | 21–40                |
| overloaded    | > 40                 |

The CEO is always labeled `n/a` — their dispatch rate is the aggregate of the agency.

## Council-level bottleneck detection

For each of the 11 councils, compute:

- **Fan-out**: avg dispatches per Chief report (high fan-out = council is on the critical path).
- **Fan-in**: avg reports feeding one CEO decision (high fan-in = Chief is bottlenecked).
- **Parallel-dispatch utilization**: (parallel dispatches this window) / (total dispatches). Low parallel utilization in a council where `worktree/references/parallel-matrix.md` allows parallel = missed throughput.

Flag any council with:

- Parallel utilization < 30 % when matrix allows ≥ 50 %.
- Fan-in > 6 on a single Chief (decision-fatigue risk).
- 0 dispatches for 2 consecutive project cycles (idle council — CSO may be running the portfolio without this council's input; roster candidate for fire or merge).

## Coverage check

For every active KR in `_vision/VISION.md > ## OKRs`, verify:

- ≥ 1 agent has traced a green `okr_alignment` to this KR in the last 30 days.
- Coverage fails if: KR orphan for > 30 days AND no delivery scope currently in progress that targets it.

Uncovered KRs → `roster-manager` surfaces them in `census.md > ## Coverage gaps`. CSO + CEO decide whether to hire, repurpose, or retire the KR.

## Process

1. `roster-manager` (per `roster/SKILL.md`) enumerates all agents from `agents/*.md`.
2. Dispatch count per agent from `_sessions/**/*.jsonl` grepped for `"from": "<name>"` type=dispatch and type=report, window = 30 days.
3. Council roll-up from `agents/AGENTS.md > Council color mapping` + parallel-matrix data.
4. Emit capacity block as part of `census.md`:

```markdown
## Capacity (window: last 30 days)

### Per-agent bands
- overloaded (>14): <list>
- hot (8-14): <list>
- healthy (3-7): <n> agents
- low (1-2): <n> agents
- idle (0): <list>

### Per-council bands
- overloaded: <list>
- hot: <list>
- healthy: <list>
- idle: <list>

### Bottleneck flags
- <council> — parallel utilization <x>% (matrix allows <y>%) — reason
- <agent> — fan-in <n> — reason

### Coverage gaps (uncovered active KRs)
- KR-<id>: no green alignment in 30d — closest agents: <list>
```

## Invariants

- Windows are 30 days for `capacity`-as-part-of-roster; 90 days for quarter roll-up capacity summaries.
- Capacity never fires a recommendation. Capacity produces signal; `hiring-lead` produces recommendations.
- Prompt-cache determinism: all capacity lists sorted alphabetically for names, descending for numeric bands (overloaded first to surface risk).
- Coverage check is agency-level. Per-project coverage is Product Council's problem.

## What this skill is not

- Not a performance review. Performance is quality; capacity is quantity. `performance-reviewer` handles quality.
- Not budget tracking. Token-cost / dollar-cost budget lives in the Wave 5 `budget` skill.
- Not routing. Which agent should handle the next dispatch is the Chief's call; capacity informs, doesn't decide.
