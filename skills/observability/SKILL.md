---
name: observability
description: OTel GenAI semantic conventions — cross-agent distributed tracing with gen_ai.* attributes, tool/LLM/retrieval spans, tail-based sampling, sensitive-data-in-events-not-attributes. SRE Council skill, owned by observability-engineer specialist. Pairs with `session-log` (per-agent JSONL) — observability is the cross-agent view; session-log is the per-agent reel.
metadata:
  version: 0.3.4
---

# observability

The agency already has per-agent session logs. It did not have a cross-agent trace. This skill adds one, using the OTel GenAI semantic conventions that stabilized in early 2026.

## Scope

- Every CEO dispatch opens a root span. Every Chief dispatch opens a child span. Every specialist opens a grandchild span. Every LLM call, tool call, and retrieval step opens a leaf span.
- Spans live in `_vision/traces/<yyyy-mm>/<trace-id>.jsonl` (append-only). One JSONL per trace. Cross-referenced from `_vision/status.json` via `traceId`.
- Attributes follow OTel GenAI: `gen_ai.system`, `gen_ai.request.model`, `gen_ai.operation.name`, `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`, `gen_ai.tool.name`, `gen_ai.tool.server`.
- Prompts + completions stored as **span events**, not attributes. Attributes are indexed + size-limited + PII-risky. Events can be dropped / redacted at a collector layer.

## Invariants

- **Attribute hygiene.** No prompt text, no completion text, no tool arguments go into span attributes. Ever. Only into events.
- **Sensitive events pass through `dlp`.** Events referencing prompts / completions are scanned for secrets before write.
- **Tail-based sampling.** Error traces: 100 %. Success traces: 10 %. Adjustable per-project via `status.json.sampling`.
- **Traces are append-only.** Closing a span writes a `span.end` event; corrections go via new event, never mutation.
- **Trace IDs propagate.** A Chief dispatching a specialist passes `traceId` + `parentSpanId` in the dispatch envelope. Specialists emit with the right parent.

## Span schema

```json
{
  "traceId": "<32 hex chars>",
  "spanId": "<16 hex chars>",
  "parentSpanId": "<16 hex chars | null>",
  "name": "ceo.dispatch | chief.convene | specialist.run | llm.call | tool.call | retrieval",
  "startTimeUnixNano": 1744200000000000000,
  "endTimeUnixNano": 1744200012500000000,
  "status": "ok | error | unset",
  "attributes": {
    "agent.name": "…",
    "agent.council": "…",
    "agent.model": "sonnet|opus|haiku|…",
    "gen_ai.system": "anthropic|openai|…",
    "gen_ai.request.model": "claude-sonnet-4-6",
    "gen_ai.operation.name": "chat.completion",
    "gen_ai.usage.input_tokens": 1234,
    "gen_ai.usage.output_tokens": 567,
    "gen_ai.usage.cached_tokens": 900,
    "gen_ai.tool.name": "Read",
    "gen_ai.tool.server": "local|mcp:…",
    "mcp.hash.matched": true,
    "dlp.flags": 0,
    "injection_defense.flags": 0
  },
  "events": [
    {"name": "prompt", "timeUnixNano": 1744200000100000000, "attributes": {"redacted": true, "ref": "_vision/traces/events/<span-id>-prompt.txt"}},
    {"name": "completion", "timeUnixNano": 1744200012400000000, "attributes": {"redacted": false, "ref": "_vision/traces/events/<span-id>-completion.txt"}}
  ]
}
```

## Process — emit a span

1. At dispatch time, generate `spanId`. If this is a root, generate `traceId`.
2. Open span: append `{"event":"span.start", …}` line.
3. On every tool/LLM call inside the span, emit a child span with the same process.
4. On close, append `{"event":"span.end", …}` with `endTimeUnixNano`, `status`, token usage, flags.
5. If sampling decision is drop, still write span.start + span.end but omit events (prompts / completions) — keeps structural topology without content cost.

## Process — consume traces

- `_vision/traces/` is readable by CEO + CEVO + CSRE + CAO.
- `observability-engineer` builds dashboards by replaying JSONL into any OTel-compatible backend (Jaeger, Tempo, Honeycomb, Datadog). Not our problem what they use.
- Regression detection (`eval`) reads traces to compute p50/p95 per council per project.
- `finops` reads traces to attribute cost per dimension.

## Sensitive-data boundary

- `dlp` is the gate for events that contain prompts/completions. If `dlp.flags > 0`, the event's `ref` is written to a quarantine path, not the normal events dir. Trace topology is preserved; content is sealed.
- `injection_defense.flags > 0` marks a span where the skill detected instruction-shaped content in a tool output. Useful for post-hoc red-team analysis.

## What never happens

- Prompt text in `attributes`.
- Mutating a written span.
- Skipping span emission because "the call was trivial." Every tool call opens a span.
- Sampling decisions that drop error traces. Errors are always kept.
- Traces leaking to external backends without a redaction pass (= `dlp` + `ip-lineage` check).
