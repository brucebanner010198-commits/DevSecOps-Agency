"""Memory interface: in-memory store behaviour and the mem0 adapter stub contract."""

import asyncio
import sys

import pytest

from voice.brain.memory import (
    InMemoryStore,
    Mem0PgVectorStore,
    MemoryBackendError,
    build_mem0_config,
    ollama_root,
)
from voice.config import MemorySettings


def run(coro):
    return asyncio.run(coro)


def _clock(start=1000.0):
    t = [start]

    def tick():
        t[0] += 1.0
        return t[0]

    return tick


def test_save_then_recall_ranks_by_overlap():
    store = InMemoryStore(clock=_clock())
    run(store.save("u1", "My dog is called Rex"))
    run(store.save("u1", "I live in Boston"))
    hits = run(store.recall("u1", "what is my dog's name"))
    assert hits == ["My dog is called Rex"]


def test_users_are_isolated():
    store = InMemoryStore(clock=_clock())
    run(store.save("alice", "alice likes tea"))
    run(store.save("bob", "bob likes coffee"))
    # No stemming: "like" does not match "likes", so the query names the nouns.
    assert run(store.recall("bob", "tea or coffee?")) == ["bob likes coffee"]
    assert run(store.recall("alice", "tea or coffee?")) == ["alice likes tea"]
    assert run(store.recall("nobody", "tea or coffee?")) == []


def test_empty_query_returns_newest_first():
    store = InMemoryStore(clock=_clock())
    for word in ("one", "two", "three"):
        run(store.save("u", f"note {word}"))
    assert run(store.recall("u", "", limit=2)) == ["note three", "note two"]


def test_limit_is_respected_and_ties_prefer_newest():
    store = InMemoryStore(clock=_clock())
    run(store.save("u", "coffee in the morning"))
    run(store.save("u", "coffee after lunch"))
    run(store.save("u", "coffee at night"))
    hits = run(store.recall("u", "coffee", limit=2))
    assert hits == ["coffee at night", "coffee after lunch"]


def test_max_items_per_user_drops_oldest():
    store = InMemoryStore(max_items_per_user=2, clock=_clock())
    run(store.save("u", "first"))
    run(store.save("u", "second"))
    run(store.save("u", "third"))
    assert store.count("u") == 2
    assert run(store.recall("u", "")) == ["third", "second"]


def test_save_rejects_empty_text_and_missing_user():
    store = InMemoryStore()
    with pytest.raises(ValueError):
        run(store.save("u", "   "))
    with pytest.raises(ValueError):
        run(store.save("", "hello"))


def test_metadata_is_copied_not_shared():
    store = InMemoryStore(clock=_clock())
    meta = {"source": "voice"}
    run(store.save("u", "remember this", metadata=meta))
    meta["source"] = "changed"
    assert store._records["u"][0].metadata == {"source": "voice"}


def test_ollama_root_strips_v1():
    assert ollama_root("http://localhost:11434/v1") == "http://localhost:11434"
    assert ollama_root("http://localhost:11434/v1/") == "http://localhost:11434"
    assert ollama_root("http://ollama:11434") == "http://ollama:11434"


def _mem0_settings(**overrides):
    base = dict(
        backend="mem0",
        recall_limit=5,
        fallback_user_id="local-user",
        postgres_host="db",
        postgres_port=5432,
        postgres_user="voice",
        postgres_password="placeholder-for-test-only",
        postgres_db="voice",
        collection="voice_memories",
        embed_model="nomic-embed-text",
        embed_dims=768,
        llm_model="llama3.2",
    )
    base.update(overrides)
    return MemorySettings(**base)


def test_build_mem0_config_targets_pgvector_and_ollama():
    cfg = build_mem0_config(_mem0_settings(), ollama_base_url="http://localhost:11434")
    assert cfg["vector_store"]["provider"] == "pgvector"
    vs = cfg["vector_store"]["config"]
    assert vs == {
        "user": "voice",
        "password": "placeholder-for-test-only",
        "host": "db",
        "port": 5432,
        "dbname": "voice",
        "collection_name": "voice_memories",
        "embedding_model_dims": 768,
    }
    assert isinstance(vs["port"], int)
    assert cfg["llm"] == {
        "provider": "ollama",
        "config": {"model": "llama3.2", "ollama_base_url": "http://localhost:11434"},
    }
    assert cfg["embedder"]["provider"] == "ollama"
    assert cfg["embedder"]["config"]["embedding_dims"] == 768
    assert cfg["embedder"]["config"]["model"] == "nomic-embed-text"


def test_build_mem0_config_refuses_other_backends():
    with pytest.raises(MemoryBackendError):
        build_mem0_config(_mem0_settings(backend="inmemory"), ollama_base_url="http://x")


def test_mem0_store_connect_fails_clearly_without_mem0(monkeypatch):
    # A None entry in sys.modules makes `import mem0` raise ImportError.
    monkeypatch.setitem(sys.modules, "mem0", None)
    store = Mem0PgVectorStore.from_settings(_mem0_settings(), ollama_base_url="http://localhost:11434")
    with pytest.raises(MemoryBackendError, match="mem0ai"):
        run(store.connect())


def test_mem0_store_refuses_use_before_connect():
    store = Mem0PgVectorStore({"vector_store": {"provider": "pgvector", "config": {}}})
    with pytest.raises(MemoryBackendError, match="connect"):
        run(store.recall("u", "q"))
    with pytest.raises(MemoryBackendError, match="connect"):
        run(store.save("u", "text"))


class _FakeAsyncMemory:
    """Stands in for mem0.AsyncMemory to pin the 2.1.0 call shapes the stub relies on."""

    def __init__(self):
        self.calls = []

    async def search(self, query, *, top_k, filters):
        self.calls.append(("search", query, top_k, filters))
        return {"results": [{"memory": "likes tea"}, {"memory": ""}, {"other": 1}]}

    async def add(self, text, *, user_id, metadata):
        self.calls.append(("add", text, user_id, metadata))
        return {"results": []}


def test_mem0_store_uses_filters_for_user_id_and_reads_results_key():
    store = Mem0PgVectorStore({})
    fake = _FakeAsyncMemory()
    store._memory = fake
    assert run(store.recall("u1", "tea?", limit=3)) == ["likes tea"]
    run(store.save("u1", "I like tea", metadata={"k": "v"}))
    assert fake.calls == [
        ("search", "tea?", 3, {"user_id": "u1"}),
        ("add", "I like tea", "u1", {"k": "v"}),
    ]
