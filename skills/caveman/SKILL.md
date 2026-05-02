---
name: caveman
description: Ultra-compressed agent communication mode. Cuts agent outbound token cost ~60-75% by dropping articles, filler words, pleasantries, and hedging while keeping all technical substance exact. Opt-in per call in v0.6.1 — never default. Designed for Agency-internal traffic where readability for future audits is acceptable in a compressed register: session logs, agent-to-agent dispatch, council meeting receipts. NEVER for User-facing surfaces (this chat, USER-ONLY decision briefs, trust scorecard) — natural language is the contract there. The v0.6.2 cycle plans an experiment defaulting caveman for ONE specific agent's session-log output to measure cost savings, audit clarity impact, and any cross-model-panel bias-flag false positives before deciding broader default-on rules.
metadata:
  version: "1.0.0"
  ratified: "2026-04-26"
  shipped_with_plugin: "0.6.1"
---

# caveman

## When to invoke

Opt-in per call. The convening Specialist (or the agent itself, when the agent realizes a low-readability-need surface is coming) sets `mode: caveman` for the response. Three valid surfaces for v0.6.1:

| Surface | Why caveman fits |
|---|---|
| **Session logs** (`_sessions/<agent>/<date>.jsonl`) | Append-only internal; future agents read for past-decision context, not narrative; compressed register is acceptable. |
| **Agent-to-agent dispatch** (CEO → Chief → Specialist routing) | Internal only; not directly read by Sovereign; CAO governance audit can decompress when needed. |
| **Council meeting receipts** (`_meetings/*.md`) | Receipts; readable but the council audience is other agents most of the time. **Caveman acceptable but verify with convening Council before defaulting** — these are referenced in trust scorecards. |

Three surfaces where caveman is **NEVER** valid:

| Surface | Why prose is the contract |
|---|---|
| **This chat** (User-facing) | Natural language is what the Sovereign expects. |
| **USER-ONLY decision briefs** | The Sovereign needs the full reasoning, in full sentences, to make the call. |
| **Trust scorecard** + other public artifacts | These are the Agency's public posture; compressed register reads as evasion. |

## How to talk in caveman

Drop:

- Articles (`a` / `an` / `the`)
- Filler (`just` / `really` / `basically` / `actually` / `simply`)
- Pleasantries (`Sure!` / `Of course` / `Happy to help`)
- Hedging (`I think` / `It seems like` / `It might be the case that`)
- Conjunctions when the relationship is clear from order
- Most pronouns when the subject is obvious from prior turn

Keep exact:

- Technical terms (no synonym substitution that loses precision)
- Code blocks (unchanged)
- Error messages (quoted exact, never paraphrased)
- File paths
- Numeric values

Use:

- Fragments OK
- Short synonyms (`big` not `extensive`, `fix` not `implement a solution for`)
- Common abbreviations (`DB` / `auth` / `config` / `req` / `res` / `fn` / `impl` / `ADR`)
- Arrows for causality (`X -> Y`)
- One word when one word is enough

Pattern: `[thing] [action] [reason]. [next step].`

### Examples

**Question:** "Why is this React component re-rendering?"

> Inline obj prop -> new ref -> re-render. `useMemo`.

**Question:** "Explain database connection pooling."

> Pool = reuse DB conn. Skip handshake -> fast under load.

**Council dispatch:** *"CEO needs CISO verdict on Phase 5 security gate for invoice-app."*

> CISO. Phase 5 gate. invoice-app. Verdict needed. Files at `<slug>/security/`. Reply by EOD.

## Persistence within a turn

Once caveman mode is set for a response, **stay in caveman for the entire response**. No partial reverts mid-paragraph. No "let me explain in normal mode just for this part" drift.

## Auto-clarity exception

Drop caveman temporarily for these specific spans within an otherwise-caveman response, then resume:

1. **Security warnings.** Anything with risk of irreversible harm. Full prose, full sentences.
2. **Irreversible action confirmations.** "This will permanently delete X" — full prose.
3. **Multi-step sequences where fragment order risks misread.** If a numbered list of steps could be parsed wrong as fragments, expand the affected steps.
4. **Sovereign asks for clarification or repeats the question.** Treat as a signal that caveman wasn't readable enough this turn — answer the clarification in full prose, then resume caveman if the next turn calls for it.
5. **Quoting an external system's output (errors, API responses).** Quote verbatim — caveman only applies to the agent's own prose.

Example:

> Bug in auth middleware. Token expiry check use `<` not `<=`. Fix in `src/auth/middleware.ts:47`.
>
> **Warning:** This requires restarting the auth service. Active sessions will be terminated. Confirm before deploy.
>
> Caveman resume. Test with `npm run test:auth`. Deploy via `make deploy:auth`.

## Cost economics (why we ship this)

Per the LLM-as-Judge survey + practical observation across the LLM-tooling community: ~60-75% reduction in outbound tokens on internal-traffic surfaces. For the Agency specifically:

- Session-log entries average ~400 tokens of agent prose per turn currently. Caveman → ~120-160 tokens.
- A typical month of Agency operation produces ~10,000 session-log turns across all active projects + Agency-internal heartbeats. Compressed: ~6,000-8,000 turns of token savings = roughly $30-60/month at current Anthropic pricing.
- Council meeting receipts are larger (~2,000 tokens each); fewer of them per month (~50). Compressed: similar absolute savings, smaller relative impact.

This is real money. But it's not enough money to justify default-on without measuring impact on audit clarity (CAO spot-checks of compressed session logs) and on cross-model-panel bias-flag accuracy (compressed responses might trigger self-enhancement-similarity check oddly). v0.6.2 will run the measured experiment.

## Anti-patterns

- **Caveman on User-facing surfaces.** Never.
- **Drifting between caveman and prose mid-response.** Pick one for the turn. Auto-clarity exceptions are short labeled spans, not free-form drift.
- **Synonym substitution that loses technical precision.** "Auth" for "authentication" is fine. "Login" for "authentication" is wrong — different concept.
- **Quoting errors or API responses inside caveman compression.** Quote verbatim.
- **Caveman for new-vocabulary explanations.** If introducing a term that's not yet in `CONTEXT.md`, full prose for the introduction; caveman after the term is established.
- **Caveman during incident response.** Pressure + compressed prose = misread. Use full prose during incidents.
- **Defaulting caveman on without User approval.** v0.6.1 is opt-in only. v0.6.2 measures one experimental default-on case; broader default-on requires User sign-off.

## Quality check

Before sending a caveman response, the agent verifies:

- [ ] The surface is on the valid-surfaces list above (session log / agent-dispatch / [verified-OK] council receipt).
- [ ] No technical term has been substituted for a less-precise synonym.
- [ ] Code blocks, error messages, file paths, and numeric values are exact.
- [ ] Auto-clarity exceptions are full prose, not compressed.
- [ ] If this is the first caveman-mode response in a session, the next turn previews the mode-switch so future readers (CAO audit) can see when the register changed.

## v0.6.2 planned experiment

One specific surface — daily heartbeat session-log entries from the rhythm-reporter agent — runs default-caveman for one calendar quarter. Measured outcomes:

- Token-cost delta per heartbeat (expected: ~65% reduction)
- CAO spot-check pass rate on caveman heartbeats vs prose baseline (expected: parity ± 5pp)
- Cross-model-panel bias-flag false-positive rate when one of the panel responses is caveman-mode (expected: parity)
- Sovereign comprehension when reading a caveman heartbeat directly (subjective; collected via inbox.json feedback)

If all four metrics land within tolerance, v0.6.3 expands default-on to broader categories per the experimental data. If not, caveman stays opt-in indefinitely.

## Interaction with other skills

| Skill | How `caveman` composes |
|---|---|
| `cross-model-panel` | A panelist responding in caveman is NOT supported in v0.6.1 — bias-mitigation procedures depend on response shape; caveman could trigger false positives on self-enhancement check. v0.6.2 experiment will assess this. |
| `incident-response` | NEVER caveman during incidents. Pressure + compression = misread. |
| `grill-with-docs` | Grilling responses to the Sovereign are full prose. The Specialist's internal note-taking during a grilling session can be caveman. |
| `audit` (CAO) | CAO spot-checks compressed session logs by occasionally asking the originating agent to expand a specific entry to prose for verification. Audit clarity is a load-bearing metric for the v0.6.2 experiment. |
| `rhythm` (heartbeat skill) | The v0.6.2 experiment runs caveman on daily heartbeats from the rhythm-reporter agent. Outcome data feeds the v0.6.3 default-on decision. |

## Provenance

- The technique is decades-old. Telegraph-era technical communication, military signals, IRC/SMS shorthand all use compressed registers when the context (audience, channel, conversation history) makes the missing words recoverable.
- The named "caveman mode" pattern for LLM-tooling is observable across the agent-development community. The `mattpocock/skills` repository (MIT, 2026) is the curator that surfaced the explicit slash-command framing to the Agency in the v0.6.1 cycle.
- The Agency-specific synthesis in this skill — valid-surface enumeration, the v0.6.2 experimental protocol, the cross-model-panel non-support note, the auto-clarity exception list calibrated to the Agency's incident posture — is original.
