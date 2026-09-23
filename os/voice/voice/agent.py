"""LiveKit entry point for the voice surface.

Run from os/voice with the environment loaded (copy .env.example to .env):

    python3 -m voice.agent console   # local microphone and speaker, no LiveKit server
    python3 -m voice.agent dev       # connect to LIVEKIT_URL with hot reload
    python3 -m voice.agent start     # production worker

Session skeleton carried from JARVIS-1.0/agent.py (AgentServer, rtc_session,
AgentSession with stt / llm / tts / vad, an Agent subclass holding the persona,
a greeting through generate_reply, agents.cli.run_app). The brain (recall,
classify, choose local or cloud, save) is wired in through Agent.llm_node, the
1.x extension point for the LLM step, instead of the LLM subclass JARVIS-2.0
used; it needs no private stream internals.

Everything from livekit is imported inside functions so the package and the
tests import without livekit installed. Signatures below were read from the
livekit-agents 1.8.2 wheel (voice/agent.py, voice/agent_session.py,
voice/turn.py, llm/chat_context.py, worker.py) and the livekit-plugins-openai
1.8.2 wheel (llm.py, stt.py, tts.py).
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any, AsyncIterator, Optional

from voice.brain.memory import InMemoryStore, Mem0PgVectorStore, MemoryStore, ollama_root
from voice.brain.router import Target, decide
from voice.config import VoiceConfig, load_config
from voice.tts import kokoro

logger = logging.getLogger("voice.agent")

PERSONA = (
    "You are the Chairman's personal voice assistant. Keep spoken replies "
    "short, clear and direct. Ask one question when something is ambiguous. "
    "Never claim to have done something you did not do."
)

MEMORY_PREAMBLE = "Known facts about the user from past conversations:"
MEMORY_POSTAMBLE = "Use them only when they are relevant to the current request."


# --------------------------------------------------------------------------- builders


def build_turn_handling(cfg: VoiceConfig) -> dict[str, Any]:
    """Interruption settings for AgentSession(turn_handling=...).

    Interrupt stops speech (the "Iron Man mechanic" from JARVIS-1.0/plan.md
    line 21). livekit-agents 1.8.2 implements barge-in inside AgentSession:
    when the VAD hears the user while the agent is talking, playback stops,
    the pending TTS audio is dropped and the transcript is truncated to what
    the user actually heard. The knobs live under turn_handling["interruption"]
    (InterruptionOptions in voice/turn.py of the 1.8.2 wheel). The plain dict
    form is what that TypedDict documents.

    mode "vad" is set explicitly. The alternative, "adaptive", constructs an
    AdaptiveInterruptionDetector that talks to LiveKit's hosted inference
    gateway; on a self-hosted server it is disabled in production mode and, in
    dev mode, fails and falls back to VAD anyway (agent_activity.py,
    _resolve_interruption_detection). Saying "vad" removes the warning and the
    network dependency. Both stt and vad must be present for barge-in to work.
    """
    return {
        "interruption": {
            "enabled": True,
            "mode": "vad",
            "min_duration": cfg.turns.interruption_min_duration,
            "min_words": cfg.turns.interruption_min_words,
        }
    }


def build_memory_store(cfg: VoiceConfig) -> MemoryStore:
    """Pick the memory backend. The mem0 store still needs connect() awaited."""
    if cfg.memory.backend == "mem0":
        return Mem0PgVectorStore.from_settings(
            cfg.memory, ollama_base_url=ollama_root(cfg.llm.local_url)
        )
    return InMemoryStore()


def build_stt(cfg: VoiceConfig) -> Any:
    if cfg.stt.provider == "deepgram":
        from livekit.plugins import deepgram

        return deepgram.STT(api_key=cfg.stt.api_key)
    from livekit.plugins import openai

    return openai.STT(api_key=cfg.stt.api_key)


def build_tts(cfg: VoiceConfig) -> Any:
    """Kokoro through the openai plugin: same endpoint, same body, less code.

    Kokoro-FastAPI is OpenAI-compatible. openai.TTS 1.8.2 takes model as a free
    string plus voice, base_url, api_key and response_format; its default
    format is mp3, so "pcm" is passed explicitly (24 kHz mono, as in
    voice/tts/kokoro.py). If this route misbehaves, a custom
    livekit.agents.tts.ChunkedStream over KokoroClient is the fallback.
    """
    from livekit.plugins import openai

    return openai.TTS(
        model=kokoro.MODEL,
        voice=cfg.kokoro.voice,
        base_url=cfg.kokoro.url,
        api_key=cfg.kokoro.api_key,
        response_format=kokoro.RESPONSE_FORMAT,
    )


def build_llms(cfg: VoiceConfig) -> tuple[Any, Optional[Any]]:
    """(local, cloud_or_None). Both are openai.LLM clients, as in JARVIS-2.0."""
    from livekit.plugins import openai

    local = openai.LLM(
        model=cfg.llm.local_model,
        base_url=cfg.llm.local_url,
        api_key=cfg.llm.local_api_key,
    )
    if not cfg.llm.cloud_available:
        return local, None
    cloud_kwargs: dict[str, Any] = {"model": cfg.llm.cloud_model, "api_key": cfg.llm.cloud_api_key}
    if cfg.llm.cloud_base_url:
        cloud_kwargs["base_url"] = cfg.llm.cloud_base_url
    return local, openai.LLM(**cloud_kwargs)


# --------------------------------------------------------------------------- helpers


def last_user_text(chat_ctx: Any) -> str:
    """Text of the most recent user message, or "" (ChatContext.messages() is a method)."""
    for message in reversed(chat_ctx.messages()):
        if getattr(message, "role", None) == "user":
            text = message.text_content
            if text:
                return text
    return ""


def format_memory_block(memories: list[str]) -> str:
    lines = "\n".join(f"- {m}" for m in memories)
    return f"{MEMORY_PREAMBLE}\n{lines}\n{MEMORY_POSTAMBLE}"


def with_memories(chat_ctx: Any, memories: list[str]) -> Any:
    """Copy of chat_ctx with a system message of memories placed after the instructions.

    ChatContext.add_message inserts by created_at when one is given, so the
    block lands right after a leading system message (the agent instructions)
    or at the front when there is none.
    """
    if not memories:
        return chat_ctx
    ctx = chat_ctx.copy()
    items = ctx.items
    created_at = 0.0
    if items and getattr(items[0], "role", None) == "system":
        created_at = items[0].created_at + 1e-6
    ctx.add_message(role="system", content=format_memory_block(memories), created_at=created_at)
    return ctx


def resolve_user_id(room: Any, fallback: str) -> str:
    """Identity of the first remote participant, else the configured fallback.

    Memory is keyed per speaker (JARVIS-2.0 hard-coded "default_user"). In
    console mode there is no remote participant, so the fallback applies.
    """
    try:
        for participant in room.remote_participants.values():
            identity = getattr(participant, "identity", "")
            if identity:
                return identity
    except Exception:  # noqa: BLE001 - never let identity lookup break a turn
        logger.debug("could not read remote participants", exc_info=True)
    return fallback


# --------------------------------------------------------------------------- agent


def make_assistant(
    cfg: VoiceConfig,
    *,
    store: MemoryStore,
    local_llm: Any,
    cloud_llm: Optional[Any],
    room: Any,
) -> Any:
    """Build the Agent subclass at runtime so livekit stays a lazy import."""
    from livekit.agents import Agent

    class Assistant(Agent):
        def __init__(self) -> None:
            super().__init__(instructions=PERSONA)
            self._pending: set[asyncio.Task[None]] = set()

        async def llm_node(self, chat_ctx: Any, tools: Any, model_settings: Any) -> AsyncIterator[Any]:
            user_id = resolve_user_id(room, cfg.memory.fallback_user_id)
            text = last_user_text(chat_ctx)

            # 1. Recall (async, so the audio loop is not blocked as it was in JARVIS-2.0).
            memories: list[str] = []
            if text:
                try:
                    memories = await store.recall(user_id, text, limit=cfg.memory.recall_limit)
                except Exception:  # noqa: BLE001 - memory is optional on a turn
                    logger.exception("memory recall failed; answering without memories")

            # 2. Classify and choose the model.
            decision = decide(
                text,
                has_tools=bool(tools),
                cloud_available=cloud_llm is not None,
                rules=cfg.router_rules,
            )
            target_llm = cloud_llm if (decision.target is Target.CLOUD and cloud_llm is not None) else local_llm
            logger.info(
                "turn user=%s route=%s target=%s memories=%d",
                user_id,
                decision.route.value,
                decision.target.value,
                len(memories),
            )

            # 3. Save the user's words off the hot path; keep the handle so it is not collected.
            if text:
                task = asyncio.create_task(self._save(user_id, text))
                self._pending.add(task)
                task.add_done_callback(self._pending.discard)

            # 4. Stream the reply from the chosen model (mirrors Agent.default.llm_node).
            ctx = with_memories(chat_ctx, memories)
            conn_options = self.session.conn_options.llm_conn_options
            async with target_llm.chat(
                chat_ctx=ctx,
                tools=tools,
                tool_choice=model_settings.tool_choice,
                conn_options=conn_options,
            ) as stream:
                async for chunk in stream:
                    yield chunk

        async def _save(self, user_id: str, text: str) -> None:
            try:
                await store.save(user_id, text)
            except Exception:  # noqa: BLE001
                logger.exception("memory save failed")

    return Assistant()


async def entrypoint(ctx: Any) -> None:
    """One job = one room. Registered with AgentServer.rtc_session in main()."""
    from livekit.agents import AgentSession
    from livekit.plugins import silero

    cfg = load_config()
    store = build_memory_store(cfg)
    if isinstance(store, Mem0PgVectorStore):
        await store.connect()  # hard failure on a bad config, never a silent fallback
    local_llm, cloud_llm = build_llms(cfg)

    session = AgentSession(
        stt=build_stt(cfg),
        llm=local_llm,  # the session default; llm_node swaps in the cloud client per turn
        tts=build_tts(cfg),
        vad=silero.VAD.load(),
        turn_handling=build_turn_handling(cfg),
    )

    assistant = make_assistant(
        cfg, store=store, local_llm=local_llm, cloud_llm=cloud_llm, room=ctx.room
    )
    # session.start connects the job to the room; no separate ctx.connect() is needed
    # on 1.8.2 (ipc/job_proc_lazy_main.py treats an active RoomIO as the connection).
    await session.start(room=ctx.room, agent=assistant)
    session.generate_reply(instructions=cfg.turns.greeting, allow_interruptions=True)


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    try:
        from dotenv import load_dotenv
    except ImportError:
        pass
    else:
        load_dotenv()  # reads ./.env if present; never committed

    cfg = load_config()  # fail early with a readable message before the worker starts

    from livekit import agents
    from livekit.agents import AgentServer

    server = AgentServer()
    # Dispatch: an empty agent_name means automatic dispatch (every new room gets
    # this agent). Setting LIVEKIT_AGENT_NAME switches LiveKit to explicit
    # dispatch, and then a dispatch rule, token or room configuration must name
    # the agent or it never joins. JARVIS-1.0 set agent_name="jarvis" without one.
    server.rtc_session(entrypoint, agent_name=cfg.livekit.agent_name)
    agents.cli.run_app(server)


if __name__ == "__main__":
    main()
