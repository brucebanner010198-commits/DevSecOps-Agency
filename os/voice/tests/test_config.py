"""Config loader: env-driven, no secret defaults, one clear error for everything missing."""

import os
import re

import pytest

from voice import config as cfgmod
from voice.config import ConfigError, load_config

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_EXAMPLE = os.path.join(HERE, ".env.example")

# Placeholder values for tests only; none of these is a real credential.
MINIMAL = {
    "LIVEKIT_URL": "ws://localhost:7880",
    "LIVEKIT_API_KEY": "test-key",
    "LIVEKIT_API_SECRET": "test-secret",
    "OPENAI_API_KEY": "test-openai",
    "LOCAL_LLM_MODEL": "llama3.2",
    "KOKORO_URL": "http://localhost:8880/v1",
}


def test_minimal_env_loads_with_documented_defaults():
    cfg = load_config(MINIMAL)
    assert cfg.livekit.url == "ws://localhost:7880"
    assert cfg.livekit.agent_name == ""  # automatic dispatch
    assert cfg.stt.provider == "openai"
    assert cfg.stt.api_key == "test-openai"
    assert cfg.llm.local_url == cfgmod.DEFAULT_LOCAL_LLM_URL
    assert cfg.llm.local_model == "llama3.2"
    assert cfg.llm.cloud_available is False
    assert cfg.llm.cloud_api_key is None
    assert cfg.kokoro.url == "http://localhost:8880/v1"
    assert cfg.kokoro.voice == "af_heart"
    assert cfg.memory.backend == "inmemory"
    assert cfg.memory.postgres_password is None
    assert cfg.turns.interruption_min_duration == 0.5
    assert cfg.turns.interruption_min_words == 0
    assert cfg.router_rules.tool_keywords == cfgmod.TOOL_KEYWORDS


def test_missing_everything_lists_every_required_name_in_one_error():
    with pytest.raises(ConfigError) as exc:
        load_config({})
    message = str(exc.value)
    for name in ("LIVEKIT_URL", "LIVEKIT_API_KEY", "LIVEKIT_API_SECRET", "OPENAI_API_KEY",
                 "LOCAL_LLM_MODEL", "KOKORO_URL"):
        assert name in message
    assert ".env.example" in message


def test_empty_string_counts_as_missing():
    env = dict(MINIMAL, LIVEKIT_API_SECRET="   ")
    with pytest.raises(ConfigError, match="LIVEKIT_API_SECRET"):
        load_config(env)


def test_deepgram_provider_needs_its_own_key_not_openai():
    env = dict(MINIMAL, STT_PROVIDER="deepgram")
    env.pop("OPENAI_API_KEY")
    with pytest.raises(ConfigError, match="DEEPGRAM_API_KEY"):
        load_config(env)
    env["DEEPGRAM_API_KEY"] = "test-dg"
    cfg = load_config(env)
    assert cfg.stt.provider == "deepgram" and cfg.stt.api_key == "test-dg"


def test_unknown_stt_provider_is_reported():
    with pytest.raises(ConfigError, match="STT_PROVIDER"):
        load_config(dict(MINIMAL, STT_PROVIDER="whisper"))


def test_cloud_model_requires_openai_key():
    env = dict(MINIMAL, STT_PROVIDER="deepgram", DEEPGRAM_API_KEY="dg", CLOUD_LLM_MODEL="gpt-4.1")
    env.pop("OPENAI_API_KEY")
    with pytest.raises(ConfigError, match="OPENAI_API_KEY"):
        load_config(env)
    env["OPENAI_API_KEY"] = "cloud-key"
    cfg = load_config(env)
    assert cfg.llm.cloud_available is True
    assert cfg.llm.cloud_model == "gpt-4.1"
    assert cfg.llm.cloud_base_url is None


def test_mem0_backend_requires_postgres_settings_with_no_password_default():
    env = dict(MINIMAL, MEMORY_BACKEND="mem0")
    with pytest.raises(ConfigError) as exc:
        load_config(env)
    for name in ("POSTGRES_HOST", "POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_DB"):
        assert name in str(exc.value)
    env.update(POSTGRES_HOST="db", POSTGRES_USER="voice", POSTGRES_PASSWORD="pw-test", POSTGRES_DB="voice")
    cfg = load_config(env)
    assert cfg.memory.backend == "mem0"
    assert cfg.memory.postgres_port == 5432  # non-secret default
    assert cfg.memory.postgres_password == "pw-test"
    assert cfg.memory.llm_model == "llama3.2"  # falls back to the local model tag


def test_malformed_numbers_are_reported_not_swallowed():
    with pytest.raises(ConfigError, match="INTERRUPTION_MIN_DURATION"):
        load_config(dict(MINIMAL, INTERRUPTION_MIN_DURATION="soon"))
    with pytest.raises(ConfigError, match="MEMORY_RECALL_LIMIT"):
        load_config(dict(MINIMAL, MEMORY_RECALL_LIMIT="five"))


def test_router_keywords_come_from_env():
    cfg = load_config(dict(MINIMAL, ROUTER_TOOL_KEYWORDS="fetch, grab", ROUTER_HEAVY_KEYWORDS="prove"))
    assert cfg.router_rules.tool_keywords == ("fetch", "grab")
    assert cfg.router_rules.heavy_keywords == ("prove",)


def test_no_secret_has_a_default_in_the_module():
    # Every module-level DEFAULT_* is a non-secret knob. Names that look like credentials
    # must not exist, except the two documented placeholders for servers with no auth.
    allowed_placeholders = {"DEFAULT_LOCAL_LLM_API_KEY", "DEFAULT_KOKORO_API_KEY"}
    for name in dir(cfgmod):
        if not name.startswith("DEFAULT_"):
            continue
        if re.search(r"SECRET|PASSWORD|TOKEN", name):
            pytest.fail(f"{name} looks like a credential default")
        if "KEY" in name:
            assert name in allowed_placeholders, name


def test_env_example_lists_every_variable_with_empty_values():
    with open(ENV_EXAMPLE, encoding="utf-8") as fh:
        lines = [ln.rstrip("\n") for ln in fh]
    assignments = [ln for ln in lines if ln and not ln.startswith("#")]
    assert assignments, ".env.example has no variables"
    for line in assignments:
        name, sep, value = line.partition("=")
        assert sep == "=", line
        assert re.fullmatch(r"[A-Z][A-Z0-9_]*", name), line
        assert value == "", f"{name} must be empty in .env.example"
    listed = {ln.partition("=")[0] for ln in assignments}
    # Every name the loader reads must be documented in the example file.
    with open(os.path.join(HERE, "voice", "config.py"), encoding="utf-8") as fh:
        read_by_loader = set(re.findall(r'(?:required|optional|choice|optional_int|optional_float)\("([A-Z0-9_]+)"', fh.read()))
    assert read_by_loader, "no env reads found in config.py"
    assert read_by_loader <= listed, sorted(read_by_loader - listed)
