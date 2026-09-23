---
adr: 0006
title: Personal AI surface, mined from the JARVIS prototypes
status: proposed
date: 2026-09-23
deciders: user
kind: product-surface
shipped-with-plugin: 0.7.0 (no version bump; nothing under skills/ or plugin.json changed contract)
related: VISION.md, MISSION.md, ADR-0004 (OS foundation), ADR-0005 (Chairman and Board model), os/voice/README.md, skills/ariv-mentor/SKILL.md
---

# ADR-0006: Personal AI surface, mined from the JARVIS prototypes

## Context

`VISION.md` (line 19, and line 44 under "The two surfaces") describes Personal
AI Mode as a JARVIS that is always present, summonable, and fronting the
recursive AI company the Chairman owns. `MISSION.md` line 14 ("Give the
Chairman a company, not a chatbot") restates it and adds the constraints:
identity-bearing data stays local, every egress passes a trust broker, an
independent verifier can veto, and reserved actions need the golden-share
signature. Until this record, nothing in the repo implemented the spoken
surface. `os/` had the trust spine, the desktop side-car and the
de-identification broker, and `os/broker` shipped a stub voice ASR behind an
interface, but there was no voice loop and no brain that routes a spoken
request.

Two prototypes existed outside the repo, in sibling folders:

- `JARVIS-1.0` (`agent.py`, `plan.md`, `docker-compose.yml`, `livekit.yaml`,
  `requirements.txt`): a LiveKit voice loop on the current 1.x API with cloud
  STT, a cloud LLM and cloud TTS, plus a compose file for a LiveKit server.
- `JARVIS-2.0` (`brain/orchestrator.py`, `brain/memory_manager.py`,
  `livekit_agent/agent.py`, `livekit_agent/custom_tts.py`,
  `docker-compose.yml`): a LangGraph brain that recalls mem0 memories from
  pgvector, classifies the request by keywords, sends chat to Ollama and heavy
  requests to a cloud model, and a custom Kokoro TTS client. Its LiveKit code
  mixes the 0.x and 1.x APIs and cannot import on any current release.

A read-only extract of both prototypes was produced before this record (the
findings are summarised in `os/voice/README.md`). Every claim about the 1.x
API used in the port was then checked against the livekit-agents 1.8.2 and
livekit-plugins-openai 1.8.2 wheels, and the mem0 config keys against the
mem0ai 2.1.0 wheel, before code was written.

Two more things arrived with the same directive: the ARIV Mentor OS (seven
markdown files defining a personal coaching mentor with five modes), and a
thesis draft, `AI-arch.md`, on an understanding-gated architecture for
reasoning and memory.

`kind: product-surface` is new. ADR-0005 used `constitution-amend`; ADR-0004
has no kind. This record does not touch the Constitution or the org model, so
a new kind was chosen rather than reusing one that does not fit.

## Decision

1. **Personal AI Mode is delivered inside this repo.** It lives at `os/voice/`
   as the fourth `os/` package, following the same layout as `trust-spine`,
   `desktop` and `broker` (flat folder, snake_case package, `conftest.py`,
   `tests/`, README). The two surfaces in `VISION.md` share one core, and the
   trust machinery that makes the personal surface trustworthy already lives
   here; a separate repo would have to import it. The prototypes were mined,
   not moved: `JARVIS-1.0` and `JARVIS-2.0` stay where they are until the
   owner archives them. Nothing in them was deleted or changed.

2. **Taken from JARVIS-1.0:** the session skeleton on livekit-agents 1.x
   (`AgentServer`, `rtc_session`, `AgentSession(stt, llm, tts, vad)`, an
   `Agent` subclass holding the persona, a greeting through
   `generate_reply`, `agents.cli.run_app`); the "interrupt stops speech"
   requirement from `plan.md`, now set explicitly through
   `turn_handling["interruption"]` in VAD mode; the worker env var names;
   the shape of a self-hosted LiveKit server in compose, corrected so the
   published UDP port (7882) is the one the server uses.

3. **Taken from JARVIS-2.0:** the routing rule (tool keywords when tools are
   offered, else heavy keywords, else chat; chat goes local, the rest go
   cloud), ported to `voice/brain/router.py` with the same keyword lists; the
   memory design (recall by the last user utterance before the reply, save
   that utterance after the model is chosen, mem0 on pgvector), ported to
   `voice/brain/memory.py` as an async interface with a working in-memory
   store and a mem0 adapter stub; the Kokoro request contract (`POST
   /v1/audio/speech`, model `kokoro`, voice `af_heart`, `response_format`
   `pcm`, 24 kHz mono), ported to `voice/tts/kokoro.py`; the pgvector and
   Kokoro compose services once corrected; the remaining env var names.

4. **Rejected:** the 0.x LiveKit API in JARVIS-2.0 (`VoiceAssistant`,
   `ChatContext.append`); every hard-coded credential (the LiveKit key pair in
   `livekit.yaml`, the Postgres password in the compose file and in
   `memory_manager.py`, the n8n basic-auth pair), all replaced by environment
   variables with no default; the retired `claude-3-5-sonnet-20240620` id and
   the dated `gpt-4o` and `llama3` defaults, replaced by env-driven model
   names; `pip install` at import time and the `sys.path` hack; LangGraph as a
   dependency (the graph was four sequential nodes and one branch; plain
   async Python does the same job); the keyword classifier's substring
   matching, replaced by whole-word matching; synchronous memory calls on the
   event loop; the hard-coded `default_user`; the silent fallback to a
   temp-path Qdrant store; the unused n8n service; the Kokoro image name that
   returns 404 and its wrong container port.

5. **Two deliberate rule changes are recorded here** so they are not mistaken
   for porting errors: whole-word keyword matching (the prototype routed
   "recall" to tools and "reasonable" to heavy reasoning), and heavy requests
   go to the cloud model only when one is configured, otherwise local (the
   prototype always chose the cloud client and would fail without a key).

6. **Redis is present in the compose file because the directive asked for
   it.** A single LiveKit node runs without it. It is wired through the
   `redis` block in `livekit.yaml` so it is not a dead service, and the
   README says how to remove both.

7. **Dependencies are pinned to exact versions** in `os/voice/requirements.txt`
   (livekit-agents 1.8.2 and its three plugins, aiohttp 3.12.14, python-dotenv
   1.1.1, pytest 9.0.1), with the one unverified pin (mem0ai 2.1.0) commented
   out and marked. This departs from the range pins in `os/trust-spine`; the
   directive asked for exact pins, and the global rule that dependencies be
   pinned agrees.

8. **ARIV became a skill.** `skills/ariv-mentor/SKILL.md` describes the five
   modes (TEACH, TRAIN, COACH, EXAMINE, SPAR), the session ritual and the hard
   limits, and the seven source files were copied unchanged into
   `skills/ariv-mentor/references/`, keeping their original names. A row was
   added to `skills/AGENTS.md`. It is the coaching face of the personal
   surface: the same person the voice loop serves, in a different mode.

9. **`AI-arch.md` sits in local-only research.** It was copied to
   `research/AI-arch-understanding-gated-predictive-intelligence.md` and
   indexed in `research/README.md`. `research/` is gitignored (root
   `.gitignore` line 6) and the file was not force-added, so it exists only on
   the owner's machine. It is background for the brain design, not a shipped
   artifact.

## Consequences

**Positive:**

- The surface `VISION.md` has described since v0.6.x now has runnable code
  in the repo, with 57 tests that need neither a network nor livekit
  installed, and a documented list of what is still a stub.
- Every credential the prototypes carried is gone. The loader raises one
  error naming every missing variable; the compose file refuses to start
  without them.
- The port targets one pinned release whose signatures were read from the
  wheel, so the "cannot import on any current release" failure of JARVIS-2.0
  cannot recur silently.
- The brain hooks in through `Agent.llm_node`, the documented 1.x extension
  point, instead of a custom `LLM` subclass that forwards private stream
  internals.

**Negative:**

- `skills/ariv-mentor/references/PROFILE_SWOT.md` and `EVOLUTION_LOG.md`
  carry personal facts about the owner (employer type, visa constraint,
  weekly hours) and mutable state. The root `.gitignore` calls this repo
  public. They were committed because the directive said to copy all seven
  files unchanged; the owner should decide before any push whether to
  gitignore those two, move them to a data path, or accept them as tracked.
  Nothing has been pushed.
- `agent.py`, the openai-plugin route to Kokoro and the mem0 adapter have not
  been executed against live services in this scaffold. Console mode is the
  first thing to run.
- STT is still cloud only, so the local-first claim holds for chat and
  memory but not for transcription.
- The voice loop does not yet emit receipts or route reserved actions through
  the trust spine, so it is not yet a governed surface in the sense of
  `MISSION.md` items 5 and 6.

**Neutral:**

- `plugin.json` and `CHANGELOG.md` were not touched: no existing skill
  changed contract, and the directive did not ask for a release. A later
  release can bundle this with other changes.
- `os/README.md` still quotes stale test counts for the older packages (77
  and 105); only a row for `voice/` and the run loop were added.

## Alternatives considered

- **Keep the voice surface in its own repo** (finish JARVIS-2.0 in place).
  Rejected: the trust machinery it must call lives here, `VISION.md` treats
  the two surfaces as one product with one core, and the 2.0 code could not
  run without the same rewrite anyway.
- **Port the JARVIS-2.0 `LLM` subclass and LangGraph graph as written.**
  Rejected: it depends on names `livekit.agents.llm` no longer exports,
  forwards chunks through a private channel, and adds a dependency for a
  four-node straight line. `Agent.llm_node` is the supported hook.
- **Write a custom `tts.ChunkedStream` for Kokoro** as the prototype did.
  Deferred: livekit's `openai.TTS` accepts model, voice, base_url, api_key and
  response_format, so it speaks Kokoro's endpoint with no new class. The
  request contract and a small client are kept in `voice/tts/kokoro.py` as
  the fallback and as the thing the tests pin.
- **Use `agent_name="jarvis"` on `rtc_session`** as JARVIS-1.0 did.
  Rejected as a default: a named agent switches LiveKit to explicit dispatch
  and never joins a room without a dispatch rule. The name is env-driven and
  empty by default.
- **Drop Redis.** Not done, because the directive listed it; recorded as
  optional instead.
- **Rename the ARIV reference files to lowercase kebab-case** to match the
  repo's `references/` convention. Not done: the directive said unchanged,
  and `diff -r` against the source proves it.

## Verification

- `cd os/voice && python3 -m pytest -q`: 57 passed.
- `for p in trust-spine desktop broker; do (cd os/$p && python3 -m pytest -q); done`:
  81, 12 and 12 passed.
- `python3 -c "import voice.agent"` from `os/voice` succeeds with no livekit
  module loaded, so the package and tests import without it.
- `docker compose -f docker-compose.voice.yml config` succeeds with the five
  credential variables set and fails naming each missing one when they are
  unset.
- `diff -r` between `ARIV-mentor-os/` and `skills/ariv-mentor/references/`
  reports no differences.
- A grep of the new tree for the three credential literals seen in the
  JARVIS-2.0 sources returns nothing; a grep for em dashes, en dashes and
  ellipsis characters in the new prose returns nothing.
- `git check-ignore -v` resolves the research copy to `.gitignore:6`.

## Provenance

- The owner's directive for this session (2026-09-23), relayed through a
  workflow run: build the personal-AI surface in this repo from the two
  JARVIS prototypes, add ARIV as a skill, keep `AI-arch.md` in local
  research, file this ADR as proposed.
- `VISION.md` lines 19 and 44 and `MISSION.md` lines 14 and 83 for what the
  surface must be.
- `JARVIS-1.0/agent.py`, `plan.md` line 21, `docker-compose.yml`,
  `livekit.yaml` (keys block not copied), `requirements.txt`.
- `JARVIS-2.0/brain/orchestrator.py` lines 104 to 147 (routing rule),
  `brain/memory_manager.py` (mem0 config, password default not copied),
  `livekit_agent/custom_tts.py` lines 78 to 89 (Kokoro contract),
  `docker-compose.yml` (credential values not copied).
- livekit-agents 1.8.2 wheel: `voice/agent_session.py`, `voice/agent.py`,
  `voice/turn.py`, `voice/agent_activity.py`, `llm/chat_context.py`,
  `worker.py`, `job.py`; livekit-plugins-openai 1.8.2 wheel: `llm.py`,
  `stt.py`, `tts.py`; mem0ai 2.1.0 wheel: `memory/main.py`,
  `configs/vector_stores/pgvector.py`, `configs/llms/ollama.py`,
  `configs/embeddings/base.py`.
- `livekit/livekit` `config-sample.yaml` (udp_port, redis) and
  `livekit-server --help` (`--keys`, env `LIVEKIT_KEYS`); the ghcr.io
  manifest for `remsky/kokoro-fastapi-cpu:latest` (HTTP 200).
- `docs/adr/README.md` for the format and the append-only numbering;
  ADR-0005 for the section layout followed here.
