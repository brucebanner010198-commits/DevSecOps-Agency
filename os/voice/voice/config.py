"""Environment-driven settings for the voice surface.

Every provider setting comes from the environment. A secret (API key, the
LiveKit key pair, the Postgres password) has no default: a missing one raises
ConfigError naming every missing variable at once. Non-secret knobs (URLs on
localhost, model tags, thresholds) carry documented defaults.

Variable names follow JARVIS-2.0 where it had one (LIVEKIT_*, OPENAI_API_KEY,
DEEPGRAM_API_KEY, STT_PROVIDER, KOKORO_URL, KOKORO_VOICE, LOCAL_LLM_URL,
LOCAL_LLM_MODEL, POSTGRES_*). See .env.example for the full list.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Mapping, Optional

from voice.brain.router import HEAVY_KEYWORDS, TOOL_KEYWORDS, RouterRules
from voice.tts.kokoro import DEFAULT_VOICE as DEFAULT_KOKORO_VOICE

STT_PROVIDERS = ("openai", "deepgram")
MEMORY_BACKENDS = ("inmemory", "mem0")

# Non-secret defaults. Nothing here is a credential.
DEFAULT_LOCAL_LLM_URL = "http://localhost:11434/v1"  # Ollama's OpenAI-compatible endpoint
DEFAULT_LOCAL_LLM_API_KEY = "ollama"  # Ollama ignores the value; the client needs a non-empty one
DEFAULT_KOKORO_API_KEY = "not-needed"  # Kokoro-FastAPI has no authentication
DEFAULT_MEM0_COLLECTION = "voice_memories"
DEFAULT_MEM0_EMBED_MODEL = "nomic-embed-text"
DEFAULT_MEM0_EMBED_DIMS = 768
DEFAULT_MEMORY_RECALL_LIMIT = 5  # JARVIS-2.0 search limit
DEFAULT_INTERRUPTION_MIN_DURATION = 0.5  # livekit-agents 1.8.2 default (voice/turn.py)
DEFAULT_INTERRUPTION_MIN_WORDS = 0  # livekit-agents 1.8.2 default
DEFAULT_GREETING = "Greet the user in one short sentence and say you are ready."
DEFAULT_FALLBACK_USER_ID = "local-user"


class ConfigError(ValueError):
    """Required environment variables are missing or malformed."""


@dataclass(frozen=True)
class LiveKitSettings:
    url: str
    api_key: str
    api_secret: str
    agent_name: str  # "" means automatic dispatch; see agent.py


@dataclass(frozen=True)
class SttSettings:
    provider: str  # one of STT_PROVIDERS
    api_key: str


@dataclass(frozen=True)
class LlmSettings:
    local_url: str
    local_model: str
    local_api_key: str
    cloud_model: Optional[str]
    cloud_base_url: Optional[str]
    cloud_api_key: Optional[str]

    @property
    def cloud_available(self) -> bool:
        return bool(self.cloud_model and self.cloud_api_key)


@dataclass(frozen=True)
class KokoroSettings:
    url: str  # full base URL including port, e.g. http://localhost:8880/v1
    voice: str
    api_key: str


@dataclass(frozen=True)
class MemorySettings:
    backend: str  # one of MEMORY_BACKENDS
    recall_limit: int
    fallback_user_id: str
    postgres_host: Optional[str]
    postgres_port: Optional[int]
    postgres_user: Optional[str]
    postgres_password: Optional[str]
    postgres_db: Optional[str]
    collection: str
    embed_model: str
    embed_dims: int
    llm_model: str


@dataclass(frozen=True)
class TurnSettings:
    interruption_min_duration: float
    interruption_min_words: int
    greeting: str


@dataclass(frozen=True)
class VoiceConfig:
    livekit: LiveKitSettings
    stt: SttSettings
    llm: LlmSettings
    kokoro: KokoroSettings
    memory: MemorySettings
    turns: TurnSettings
    router_rules: RouterRules


def _split_csv(value: str, fallback: tuple[str, ...]) -> tuple[str, ...]:
    items = tuple(part.strip() for part in value.split(",") if part.strip())
    return items or fallback


def load_config(env: Optional[Mapping[str, str]] = None) -> VoiceConfig:
    """Read settings from `env` (default: os.environ) and validate them.

    Raises ConfigError with one message that lists every missing variable and
    every malformed value, so the operator fixes them in one pass.
    """
    source: Mapping[str, str] = os.environ if env is None else env
    missing: list[str] = []
    problems: list[str] = []

    def raw(name: str) -> str:
        value = source.get(name)
        return value.strip() if isinstance(value, str) else ""

    def required(name: str) -> str:
        value = raw(name)
        if not value:
            missing.append(name)
        return value

    def optional(name: str, default: str) -> str:
        value = raw(name)
        return value or default

    def choice(name: str, default: str, allowed: tuple[str, ...]) -> str:
        value = optional(name, default).lower()
        if value not in allowed:
            problems.append(f"{name}={value!r} is not one of {', '.join(allowed)}")
        return value

    def optional_int(name: str, default: int) -> int:
        value = raw(name)
        if not value:
            return default
        try:
            return int(value)
        except ValueError:
            problems.append(f"{name}={value!r} is not an integer")
            return default

    def optional_float(name: str, default: float) -> float:
        value = raw(name)
        if not value:
            return default
        try:
            return float(value)
        except ValueError:
            problems.append(f"{name}={value!r} is not a number")
            return default

    # LiveKit worker connection (JARVIS-1.0 .env.local names).
    livekit = LiveKitSettings(
        url=required("LIVEKIT_URL"),
        api_key=required("LIVEKIT_API_KEY"),
        api_secret=required("LIVEKIT_API_SECRET"),
        agent_name=optional("LIVEKIT_AGENT_NAME", ""),
    )

    # Speech to text. The chosen provider's key is required; the other is not.
    stt_provider = choice("STT_PROVIDER", "openai", STT_PROVIDERS)
    stt_key_name = "DEEPGRAM_API_KEY" if stt_provider == "deepgram" else "OPENAI_API_KEY"
    stt = SttSettings(provider=stt_provider, api_key=required(stt_key_name))

    # Models. Local is required; cloud is optional and needs OPENAI_API_KEY when set.
    cloud_model = optional("CLOUD_LLM_MODEL", "") or None
    cloud_api_key: Optional[str] = None
    if cloud_model:
        cloud_api_key = required("OPENAI_API_KEY")
    llm = LlmSettings(
        local_url=optional("LOCAL_LLM_URL", DEFAULT_LOCAL_LLM_URL),
        local_model=required("LOCAL_LLM_MODEL"),
        local_api_key=optional("LOCAL_LLM_API_KEY", DEFAULT_LOCAL_LLM_API_KEY),
        cloud_model=cloud_model,
        cloud_base_url=optional("CLOUD_LLM_BASE_URL", "") or None,
        cloud_api_key=cloud_api_key or None,
    )

    # Kokoro. The port is part of KOKORO_URL.
    kokoro = KokoroSettings(
        url=required("KOKORO_URL"),
        voice=optional("KOKORO_VOICE", DEFAULT_KOKORO_VOICE),
        api_key=optional("KOKORO_API_KEY", DEFAULT_KOKORO_API_KEY),
    )

    # Memory. Postgres settings are required only for the mem0 backend, and the
    # password never has a default (JARVIS-2.0 shipped one in code).
    backend = choice("MEMORY_BACKEND", "inmemory", MEMORY_BACKENDS)
    pg_host = pg_user = pg_password = pg_db = None
    pg_port: Optional[int] = None
    if backend == "mem0":
        pg_host = required("POSTGRES_HOST")
        pg_port = optional_int("POSTGRES_PORT", 5432)
        pg_user = required("POSTGRES_USER")
        pg_password = required("POSTGRES_PASSWORD")
        pg_db = required("POSTGRES_DB")
    memory = MemorySettings(
        backend=backend,
        recall_limit=optional_int("MEMORY_RECALL_LIMIT", DEFAULT_MEMORY_RECALL_LIMIT),
        fallback_user_id=optional("MEMORY_FALLBACK_USER_ID", DEFAULT_FALLBACK_USER_ID),
        postgres_host=pg_host,
        postgres_port=pg_port,
        postgres_user=pg_user,
        postgres_password=pg_password,
        postgres_db=pg_db,
        collection=optional("MEM0_COLLECTION", DEFAULT_MEM0_COLLECTION),
        embed_model=optional("MEM0_EMBED_MODEL", DEFAULT_MEM0_EMBED_MODEL),
        embed_dims=optional_int("MEM0_EMBED_DIMS", DEFAULT_MEM0_EMBED_DIMS),
        llm_model=optional("MEM0_LLM_MODEL", llm.local_model),
    )

    turns = TurnSettings(
        interruption_min_duration=optional_float(
            "INTERRUPTION_MIN_DURATION", DEFAULT_INTERRUPTION_MIN_DURATION
        ),
        interruption_min_words=optional_int("INTERRUPTION_MIN_WORDS", DEFAULT_INTERRUPTION_MIN_WORDS),
        greeting=optional("GREETING_INSTRUCTIONS", DEFAULT_GREETING),
    )

    rules = RouterRules(
        tool_keywords=_split_csv(optional("ROUTER_TOOL_KEYWORDS", ""), TOOL_KEYWORDS),
        heavy_keywords=_split_csv(optional("ROUTER_HEAVY_KEYWORDS", ""), HEAVY_KEYWORDS),
    )

    if missing or problems:
        parts = ["Voice surface configuration is incomplete."]
        if missing:
            parts.append("Missing required environment variables: " + ", ".join(missing) + ".")
        if problems:
            parts.append("Invalid values: " + "; ".join(problems) + ".")
        parts.append("Copy os/voice/.env.example to os/voice/.env and fill in the values.")
        raise ConfigError(" ".join(parts))

    return VoiceConfig(
        livekit=livekit,
        stt=stt,
        llm=llm,
        kokoro=kokoro,
        memory=memory,
        turns=turns,
        router_rules=rules,
    )
