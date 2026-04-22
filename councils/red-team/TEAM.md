# `red-team` council — TEAM

> Living team card. Updated whenever the roster changes. Paired with [`AGENTS.md`](./AGENTS.md) which declares the council's contract.

## Remit

Adversarial prompting, tool abuse, PII exfil, memory poisoning, supply-chain, social engineering, chaos injection.

## Convened when

Every project's second-pass; pre-release chaos-gate; post-incident retros.

## Lead

- **`red-team-lead`** — sonnet — Chief Red-Team Officer (CRT) — the Chief who runs an adversarial council that tries to break everything the agency has built before an outside party does.

## Specialists

| Agent | Tier | Purpose |
| --- | --- | --- |
| `adversarial-prompter` | `haiku` | Red-Team Council needs prompt-injection, jailbreak, and indirect-injection tests run against a project's LLM-facing surfaces (chatbots, RAG endpoints, agent tool prompts, system... |
| `tool-abuse-tester` | `haiku` | Red-Team Council needs tool-abuse, permission-bypass, and tool-chaining tests run against a project's agent surface or MCP integrations. |
| `data-exfil-tester` | `haiku` | Red-Team Council needs data-exfiltration tests run against a project — PII leaks, credential egress, secret disclosure, training-data regurgitation, and sensitive-context leakag... |
| `model-poisoning-scout` | `haiku` | Red-Team Council needs memory-poisoning, context-window-poisoning, and long-horizon manipulation signals checked across a project or the workspace. |
| `supply-chain-attacker` | `haiku` | Red-Team Council needs dependency / supply-chain attack simulations run against a project — package-pinning review, typosquatting, lockfile drift, transitive-dependency CVE scan... |
| `social-engineering-tester` | `haiku` | Red-Team Council needs social-engineering, impersonation, and human-in-the-loop overload tests run against a project. |
| `playbook-author` | `haiku` | Red-Team Council needs to turn a remediated finding into a durable stepping stone, review a prompt diff against the archived stones, or propose a self-modifying playbook update ... |
| `chaos-engineer` | `sonnet` | Red-Team council needs deliberate fault injection to verify the resilience ladder — model-unavailable, tool-error-transient/permanent, tool-output-malformed/injected, rate-limit... |

## Worker tier

Specialists may, when a task decomposes cleanly along a dimension (per-file, per-table, per-endpoint, per-dependency), spawn **workers** — a third tier below specialist. Workers inherit the parent specialist's tool set and model tier unless overridden. Default depth cap is three levels (Chief → Specialist → Worker); deeper fanout requires an ADR from the lead.

Worker declaration lives in the parent specialist's frontmatter:

```yaml
workers:
  - name: <slug>
    split: <dimension>    # e.g. per-file, per-endpoint, per-dep
    max_parallel: 8       # per-council cap, overrides optional
```

Fanout + aggregation is handled by `skills/fanout/` (see root README).

This council declares no worker patterns in v0.3.7. Extend here when one emerges.

## Council norms

The council's must / must-not contract is authoritative in [`AGENTS.md`](./AGENTS.md). This file only records who currently staffs the council.
