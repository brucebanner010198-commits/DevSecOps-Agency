"""Long-term memory: a thin save / recall interface with two implementations.

Design carried from JARVIS-2.0/brain/memory_manager.py and orchestrator.py:
before each reply, look up memories for the speaker with the last user
utterance as the query; after the reply is chosen, save that utterance. Only
the user's words are stored, never the assistant's reply.

What changed from the prototype:

  * The interface is async, so a slow backend cannot stall the audio loop.
    The prototype called mem0's synchronous search and add on the event loop.
  * Memory is keyed by the LiveKit participant identity, not a hard-coded
    "default_user".
  * The mem0 adapter never falls back to another store. The prototype
    silently switched to a temp-path Qdrant store when Postgres was down.
  * The prototype's default Postgres password literal is gone. The password
    comes from the environment only (see config.py).

InMemoryStore is the working implementation used by tests and by
MEMORY_BACKEND=inmemory. Mem0PgVectorStore is a stub for MEMORY_BACKEND=mem0:
the config dict and call shapes were read from the mem0ai 2.1.0 wheel but
were not executed against a live Postgres in this scaffold.
"""

from __future__ import annotations

import math
import re
import time
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Callable, Mapping, Protocol

if TYPE_CHECKING:  # avoid a runtime import cycle with config.py
    from voice.config import MemorySettings


class MemoryBackendError(RuntimeError):
    """A memory backend is missing, unconfigured, or unreachable."""


class MemoryStore(Protocol):
    """What the agent needs from a memory backend."""

    async def recall(self, user_id: str, query: str, *, limit: int = 5) -> list[str]:
        """Return up to `limit` remembered facts for `user_id` relevant to `query`."""

    async def save(
        self, user_id: str, text: str, *, metadata: Mapping[str, str] | None = None
    ) -> None:
        """Store one user utterance for `user_id`."""

    async def close(self) -> None:
        """Release connections."""


# --------------------------------------------------------------------------- in memory

_WORD_RE = re.compile(r"[a-z0-9]+")


def _tokens(text: str) -> set[str]:
    """Lower-case alphanumeric tokens of three or more characters ("dog's" gives "dog")."""
    return {w for w in _WORD_RE.findall(text.lower()) if len(w) >= 3}


@dataclass(frozen=True)
class MemoryRecord:
    text: str
    created_at: float
    metadata: dict[str, str] = field(default_factory=dict)


class InMemoryStore:
    """Per-user list of utterances with token-overlap recall.

    Good enough for console testing and for the unit tests. Not persistent.
    """

    def __init__(
        self, *, max_items_per_user: int = 1000, clock: Callable[[], float] = time.time
    ) -> None:
        if max_items_per_user < 1:
            raise ValueError("max_items_per_user must be at least 1")
        self._max = max_items_per_user
        self._clock = clock
        self._records: dict[str, list[MemoryRecord]] = {}

    async def save(
        self, user_id: str, text: str, *, metadata: Mapping[str, str] | None = None
    ) -> None:
        if not user_id:
            raise ValueError("user_id is required")
        if not text or not text.strip():
            raise ValueError("text is empty")
        bucket = self._records.setdefault(user_id, [])
        bucket.append(
            MemoryRecord(text=text.strip(), created_at=self._clock(), metadata=dict(metadata or {}))
        )
        if len(bucket) > self._max:
            del bucket[: len(bucket) - self._max]

    async def recall(self, user_id: str, query: str, *, limit: int = 5) -> list[str]:
        bucket = self._records.get(user_id, [])
        if not bucket or limit < 1:
            return []
        newest_first = sorted(bucket, key=lambda r: r.created_at, reverse=True)
        query_tokens = _tokens(query)
        if not query_tokens:
            return [r.text for r in newest_first[:limit]]
        scored: list[tuple[float, float, str]] = []
        for record in newest_first:
            overlap = len(query_tokens & _tokens(record.text))
            if overlap:
                score = overlap / math.sqrt(len(query_tokens))
                scored.append((score, record.created_at, record.text))
        scored.sort(key=lambda s: (s[0], s[1]), reverse=True)
        return [text for _, _, text in scored[:limit]]

    def count(self, user_id: str) -> int:
        return len(self._records.get(user_id, []))

    async def close(self) -> None:
        return None


# --------------------------------------------------------------------------- mem0 stub


def ollama_root(openai_compatible_url: str) -> str:
    """Turn Ollama's OpenAI-compatible URL (ending in /v1) into its native API root.

    mem0's Ollama provider wants the native root (http://host:11434), while the
    livekit openai plugin wants the /v1 endpoint. One env var feeds both.
    """
    url = openai_compatible_url.strip().rstrip("/")
    if url.endswith("/v1"):
        url = url[: -len("/v1")]
    return url


def build_mem0_config(memory: "MemorySettings", *, ollama_base_url: str) -> dict[str, Any]:
    """The mem0 config dict for pgvector storage with Ollama for both LLM and embeddings.

    Keys verified against the mem0ai 2.1.0 wheel:
      vector_store pgvector: user, password, host, port (int), dbname,
        collection_name, embedding_model_dims (mem0/configs/vector_stores/pgvector.py)
      llm ollama: model, ollama_base_url (mem0/configs/llms/ollama.py)
      embedder ollama: model, embedding_dims, ollama_base_url
        (mem0/configs/embeddings/base.py)

    Pointing llm and embedder at Ollama is what keeps memory local. mem0's
    defaults are OpenAI for both, which would need OPENAI_API_KEY even on the
    "local" path (JARVIS-2.0 had this problem).
    """
    if memory.backend != "mem0":
        raise MemoryBackendError("build_mem0_config called but MEMORY_BACKEND is not mem0")
    return {
        "vector_store": {
            "provider": "pgvector",
            "config": {
                "user": memory.postgres_user,
                "password": memory.postgres_password,
                "host": memory.postgres_host,
                "port": int(memory.postgres_port),
                "dbname": memory.postgres_db,
                "collection_name": memory.collection,
                "embedding_model_dims": int(memory.embed_dims),
            },
        },
        "llm": {
            "provider": "ollama",
            "config": {"model": memory.llm_model, "ollama_base_url": ollama_base_url},
        },
        "embedder": {
            "provider": "ollama",
            "config": {
                "model": memory.embed_model,
                "embedding_dims": int(memory.embed_dims),
                "ollama_base_url": ollama_base_url,
            },
        },
    }


class Mem0PgVectorStore:
    """Adapter stub: mem0 AsyncMemory over pgvector.

    Status: not exercised. `connect()` builds the client with
    `AsyncMemory.from_config`, which validates the config and opens the
    Postgres connection; any failure propagates. Call shapes (2.1.0 wheel):

      await memory.add(text, user_id=..., metadata=...)
      await memory.search(query, top_k=..., filters={"user_id": ...})
        -> {"results": [{"memory": "...", ...}, ...]}

    Note that 2.x rejects a top-level user_id on search; it must go in
    filters. The JARVIS-2.0 call `search(query, user_id=..., limit=5)` is the
    old 0.1.x shape and raises on 2.1.0.
    """

    def __init__(self, config: dict[str, Any]) -> None:
        self._config = config
        self._memory: Any = None

    @classmethod
    def from_settings(cls, memory: "MemorySettings", *, ollama_base_url: str) -> "Mem0PgVectorStore":
        return cls(build_mem0_config(memory, ollama_base_url=ollama_base_url))

    async def connect(self) -> None:
        try:
            from mem0 import AsyncMemory  # type: ignore[import-not-found]
        except ImportError as exc:
            raise MemoryBackendError(
                "MEMORY_BACKEND=mem0 but the mem0ai package is not installed. "
                "Uncomment mem0ai in os/voice/requirements.txt and install it, "
                "or set MEMORY_BACKEND=inmemory."
            ) from exc
        self._memory = AsyncMemory.from_config(self._config)

    def _require(self) -> Any:
        if self._memory is None:
            raise MemoryBackendError("Mem0PgVectorStore.connect() was not awaited")
        return self._memory

    async def recall(self, user_id: str, query: str, *, limit: int = 5) -> list[str]:
        memory = self._require()
        result = await memory.search(query, top_k=limit, filters={"user_id": user_id})
        rows = result.get("results", []) if isinstance(result, dict) else []
        return [str(r["memory"]) for r in rows if isinstance(r, dict) and r.get("memory")]

    async def save(
        self, user_id: str, text: str, *, metadata: Mapping[str, str] | None = None
    ) -> None:
        memory = self._require()
        await memory.add(text, user_id=user_id, metadata=dict(metadata or {}))

    async def close(self) -> None:
        self._memory = None
