---
name: mcp-authoring
description: Build high-quality MCP (Model Context Protocol) servers that expose the agency's tools to external agents, or integrate third-party APIs as MCP servers for internal use. Four-phase process — Plan → Implement → Review → Evaluate. Pairs with the mcp-defense skill (consumer side) to give the agency end-to-end MCP competence — producer and consumer. Use when agents need to ship an MCP server, wrap an API behind MCP, design tool schemas for agent use, or evaluate whether a draft MCP server is fit to release.
version: "0.3.5"
license: "Apache-2.0 (upstream: Anthropic skills repo) — see LICENSE.txt"
---

# MCP Authoring (Producer Side)

Pairs with **mcp-defense** (consumer side). Together they give the agency full MCP lifecycle coverage:

| | Skill | Specialist |
|--|--|--|
| Producer | **mcp-authoring** (this skill) | `mcp-author` |
| Consumer | `mcp-defense` | `mcp-defender` |

Use this skill when the agency is **building or shipping** an MCP server — either exposing internal capabilities to agents or wrapping a third-party API. For consuming a third-party MCP server safely, use `mcp-defense`.

## When to use

- `ship-it` needs to stand up a new MCP server to expose an internal capability to agents.
- `api-designer` / `integrations-engineer` is wrapping a third-party REST/GraphQL API as an MCP server.
- `mcp-registry-scout` discovered a candidate API and the agency wants to build the MCP wrapper in-house (rather than import a third-party one).
- QA wants to evaluate a draft MCP server before release.

## Process (4 phases)

### Phase 1 — Plan

**Coverage decision.** Prefer comprehensive API coverage over a small set of "workflow" tools unless measurement shows agents struggle with composition. Comprehensive tools let agents compose; workflow tools constrain to pre-imagined tasks.

**Tool naming.** Use consistent prefixes — `github_create_issue`, `github_list_repos` — not ambiguous verbs alone (`create`, `list`). Action-first. Stable across versions.

**Transport.** Streamable HTTP with stateless JSON for remote servers (simpler to scale than stateful sessions). stdio for local.

**SDK.** TypeScript SDK recommended for new servers (static typing, ecosystem, Zod schemas). Python SDK (FastMCP) if the underlying service is Python-native.

**Input/output schemas.** Every tool defines both. Use `outputSchema` + `structuredContent` in responses so downstream agents can parse without heuristics.

**Annotations — set all four.** `readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`. These drive the consumer's capability policy (see `mcp-defense`).

**Reference:**
- `reference/mcp_best_practices.md` — universal MCP guidelines
- `reference/node_mcp_server.md` — TypeScript patterns
- `reference/python_mcp_server.md` — Python / FastMCP patterns

### Phase 2 — Implement

**Shared utilities.** Single API client with auth baked in; one error-handling helper; one response formatter; pagination wrapper. DRY.

**Tool descriptions.** Concise. Parameter descriptions with examples in the field text. Error messages that tell the caller what to do next, not just what broke.

**Async I/O.** Everything that touches the network.

**Rate limiting & backoff.** Respect upstream limits. Surface `429` / `Retry-After` as structured hints, not crashes.

### Phase 3 — Review

Before shipping, check:

- No duplicated code across tools.
- Every tool has a schema-validated input and output.
- Error messages include next steps.
- Annotations are set.
- Secrets loaded from env, not hard-coded.
- **Agency-specific:** the server emits OTel GenAI tool-span events (see `skills/observability`) so `agent-telemetry-engineer` can trace tool use.
- **Agency-specific:** the server does NOT accept raw LLM output as a parameter for any destructive tool without an `<untrusted-data>` envelope check (see `skills/injection-defense`).

**Build check.** TypeScript: `npm run build`. Python: `python -m py_compile server.py`.

**Inspector check.** `npx @modelcontextprotocol/inspector` against the server. Every tool exercised at least once.

### Phase 4 — Evaluate

Ship no MCP server without a **10-question eval suite**.

Each question must be:

- **Independent** — not chained to other questions.
- **Read-only** — no destructive operations.
- **Complex** — requires multiple tool calls to answer.
- **Realistic** — mirrors a real user task.
- **Verifiable** — single correct answer, string-comparable.
- **Stable** — answer won't drift week-over-week.

**Output format** — see `scripts/example_evaluation.xml`. XML with `<qa_pair>` children.

**Runner:** `scripts/evaluation.py` — takes the XML eval + MCP server config, runs Claude against the server, reports pass/fail per question.

**Connection helpers:** `scripts/connections.py` — utilities for wiring to a local or remote MCP server during eval.

## Agency integration

- Ownership: **`mcp-author`** specialist agent (Execution council).
- Handoff from: `api-designer` (API surface spec) or `integrations-engineer` (third-party API to wrap).
- Handoff to: `mcp-defense` for consumer-side registration (the new server gets a pinned tool-hash entry), then `ship-it`.
- Eval results feed: `evaluation-lead` (CEVO), who decides release readiness.
- Always pairs with `skills/observability` (OTel GenAI spans on every tool) and `skills/injection-defense` (envelope pattern for any tool taking LLM-originated args).

## Reference files

- `reference/mcp_best_practices.md`
- `reference/node_mcp_server.md`
- `reference/python_mcp_server.md`
- `reference/evaluation.md`
- `scripts/evaluation.py`, `scripts/connections.py`, `scripts/example_evaluation.xml`, `scripts/requirements.txt`

## Lineage

Upstream: [anthropics/skills — mcp-builder](https://github.com/anthropics/skills/tree/main/skills/mcp-builder), Apache 2.0. Renamed to `mcp-authoring` to clarify producer-vs-consumer role against this plugin's `mcp-defense`. Reference files and scripts are the upstream originals, unmodified. This SKILL.md is agency-authored and wires the skill into the DevSecOps Agency's org chart. `LICENSE.txt` retained verbatim per Apache 2.0 §4(a).
