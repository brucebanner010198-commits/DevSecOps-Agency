# Voice surface v0

The spoken front door of Personal AI Mode from [`VISION.md`](../../VISION.md)
(the summonable overlay that fronts the company the Chairman owns). This is a
scaffold: a LiveKit voice loop (Silero VAD, STT, one routing brain, Kokoro
TTS) in front of a local-first brain that recalls memories, classifies the
request, answers from a local Ollama model or a cloud model, and saves the
user's words back to memory.

It was built by mining two earlier prototypes, `JARVIS-1.0` and `JARVIS-2.0`
(sibling folders, to be archived), and keeping only what still holds on
livekit-agents 1.x. The decision record is
[`docs/adr/ADR-0006-personal-ai-surface.md`](../../docs/adr/ADR-0006-personal-ai-surface.md).

## Layout

```
voice/
  config.py          env-driven settings; secrets have no defaults
  brain/router.py    classify the request, choose local or cloud
  brain/memory.py    save / recall interface, InMemoryStore, mem0 stub
  tts/kokoro.py      Kokoro request contract and client
  agent.py           LiveKit entry point; the only module that imports livekit
tests/               57 tests, no network, no livekit needed
docker-compose.voice.yml, livekit.yaml, .env.example
```

## Run it

```bash
cd os/voice
python3 -m pytest -q                                   # unit tests, no services needed

pip install -r requirements.txt                        # livekit-agents 1.8.2 and plugins
cp .env.example .env                                   # fill in every value
docker compose -f docker-compose.voice.yml up -d       # livekit, redis, pgvector, kokoro
ollama pull <LOCAL_LLM_MODEL>                          # Ollama runs on the host, port 11434
python3 -m voice.agent console                         # talk through the local mic
python3 -m voice.agent dev                             # join rooms on LIVEKIT_URL
```

Run the agent as a module from this directory; running `voice/agent.py`
directly breaks the package imports.

## What came from where

From **JARVIS-1.0** (`agent.py`, `plan.md`):

- The session skeleton on the current 1.x API: `AgentServer`, `rtc_session`,
  `AgentSession(stt, llm, tts, vad)`, an `Agent` subclass holding the persona,
  a greeting through `generate_reply`, `agents.cli.run_app`.
- The "interrupt stops speech" requirement (plan.md, "Iron Man mechanic").
  On 1.8.2 that is `turn_handling["interruption"]`; `agent.py` sets it
  explicitly to VAD mode and documents why.
- The env var names for the worker (`LIVEKIT_URL`, `LIVEKIT_API_KEY`,
  `LIVEKIT_API_SECRET`) and the compose shape for a LiveKit server.

From **JARVIS-2.0** (`brain/orchestrator.py`, `brain/memory_manager.py`,
`livekit_agent/custom_tts.py`, `docker-compose.yml`):

- The routing rule: tool keywords when tools exist, else heavy keywords, else
  chat; chat goes local, the rest go cloud. Ported to `brain/router.py` with
  the same keyword lists.
- The memory design: recall by the last user utterance before the reply, save
  that utterance after the model is chosen, five hits per turn, mem0 on
  pgvector. Ported to `brain/memory.py` as an async interface.
- The Kokoro request contract: `POST {KOKORO_URL}/audio/speech` with
  `{"model": "kokoro", "input", "voice": "af_heart", "response_format": "pcm"}`,
  24 kHz mono. Ported to `tts/kokoro.py`.
- The pgvector and Kokoro compose services and the remaining env var names.

## What was rejected, and why

- JARVIS-2.0's LiveKit code targets the 0.x API (`VoiceAssistant`,
  `ChatContext.append`) and cannot import on any current release. The 1.0
  skeleton was used instead.
- Hard-coded credentials: the LiveKit key pair in `livekit.yaml`, the Postgres
  password in the compose file and in `memory_manager.py`, the n8n basic-auth
  pair. Every one is now an environment variable with no default.
- Retired or dated model ids (`claude-3-5-sonnet-20240620`, `gpt-4o`, the
  `llama3` tag). Model names are env-driven.
- `pip install` at import time and `sys.path` hacks.
- The keyword classifier's substring matching ("recall" routed to tools,
  "reasonable" to heavy). The port matches whole words.
- Blocking memory calls on the event loop, the hard-coded `default_user`, and
  the silent fallback to a temp-path Qdrant store when Postgres was down.
- The unused n8n service. Redis is kept because the task asked for it; a single
  LiveKit node does not need it.

## What is a stub

- `brain/memory.py` `Mem0PgVectorStore`: the config dict and the call shapes
  were read from the mem0ai 2.1.0 wheel but never run against a live Postgres.
  `InMemoryStore` is the working backend and the default.
- `tts/kokoro.py` `KokoroClient`: exercised only with a fake HTTP session.
  `agent.py` reaches Kokoro through livekit's `openai.TTS` plugin pointed at
  `KOKORO_URL`, which speaks the same endpoint; that path has not been run
  against a live Kokoro here.
- `agent.py` as a whole: written against the 1.8.2 wheel's signatures, not
  executed against a LiveKit server in this scaffold. Console mode is the
  first thing to try.
- STT is cloud only (OpenAI or Deepgram), as in both prototypes. A local STT
  is the obvious next step for the local-first claim.
- No trust-spine integration yet: the loop does not emit receipts or route
  reserved actions through the golden share. That is the point of putting it
  in this repo, and it is the next milestone.

## Environment variables

See [`.env.example`](.env.example) for the full list with comments.
Required always: `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`,
`LOCAL_LLM_MODEL`, `KOKORO_URL`, plus the API key of the chosen
`STT_PROVIDER`. Required with `CLOUD_LLM_MODEL`: `OPENAI_API_KEY`. Required
with `MEMORY_BACKEND=mem0`: `POSTGRES_HOST`, `POSTGRES_USER`,
`POSTGRES_PASSWORD`, `POSTGRES_DB`. A missing variable raises one error that
names all of them.
