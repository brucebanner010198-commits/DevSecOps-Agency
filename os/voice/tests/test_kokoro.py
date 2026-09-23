"""Kokoro request contract and client, with a fake HTTP session. No network."""

import asyncio

import pytest

from voice.tts.kokoro import (
    DEFAULT_VOICE,
    MIME_TYPE,
    MODEL,
    NUM_CHANNELS,
    RESPONSE_FORMAT,
    SAMPLE_RATE,
    KokoroClient,
    KokoroError,
    build_speech_request,
    speech_url,
)


def run(coro):
    return asyncio.run(coro)


def test_audio_contract_constants():
    assert SAMPLE_RATE == 24000
    assert NUM_CHANNELS == 1
    assert MODEL == "kokoro"
    assert DEFAULT_VOICE == "af_heart"
    assert RESPONSE_FORMAT == "pcm"
    assert MIME_TYPE == "audio/pcm"


def test_speech_url_joins_base_and_path():
    assert speech_url("http://localhost:8880/v1") == "http://localhost:8880/v1/audio/speech"
    assert speech_url("http://localhost:8880/v1/") == "http://localhost:8880/v1/audio/speech"
    with pytest.raises(ValueError):
        speech_url("  ")


def test_build_speech_request_matches_prototype_contract():
    req = build_speech_request(base_url="http://kokoro:8880/v1", text="Hello there", api_key="abc")
    assert req.method == "POST"
    assert req.url == "http://kokoro:8880/v1/audio/speech"
    assert req.headers == {"Authorization": "Bearer abc", "Content-Type": "application/json"}
    assert req.json == {
        "model": "kokoro",
        "input": "Hello there",
        "voice": "af_heart",
        "response_format": "pcm",
    }


def test_build_speech_request_rejects_empty_text_or_voice():
    with pytest.raises(ValueError):
        build_speech_request(base_url="http://x/v1", text="  ")
    with pytest.raises(ValueError):
        build_speech_request(base_url="http://x/v1", text="hi", voice="")


def test_client_port_comes_from_base_url():
    client = KokoroClient(base_url="http://127.0.0.1:9999/v1", voice="af_bella")
    assert client.url == "http://127.0.0.1:9999/v1/audio/speech"
    req = client.build_request("hi")
    assert req.json["voice"] == "af_bella"
    assert req.url.startswith("http://127.0.0.1:9999/")


class _FakeContent:
    def __init__(self, chunks):
        self._chunks = chunks

    async def iter_chunked(self, n):
        for chunk in self._chunks:
            yield chunk


class _FakeResponse:
    def __init__(self, status, chunks=(), text=""):
        self.status = status
        self.content = _FakeContent(list(chunks))
        self._text = text

    async def text(self):
        return self._text

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        return False


class _FakeSession:
    """Records the request and replays a canned response. Never touches the network."""

    def __init__(self, response):
        self.response = response
        self.calls = []
        self.closed = False

    def post(self, url, *, json, headers):
        self.calls.append({"url": url, "json": json, "headers": headers})
        return self.response

    async def close(self):
        self.closed = True


def test_stream_pcm_yields_chunks_and_sends_the_contract():
    session = _FakeSession(_FakeResponse(200, chunks=[b"\x00\x01", b"", b"\x02\x03"]))
    client = KokoroClient(base_url="http://localhost:8880/v1", session_factory=lambda: session)

    async def collect():
        return [c async for c in client.stream_pcm("say this")]

    assert run(collect()) == [b"\x00\x01", b"\x02\x03"]  # empty chunk skipped
    assert session.closed is True
    assert session.calls == [
        {
            "url": "http://localhost:8880/v1/audio/speech",
            "json": {"model": "kokoro", "input": "say this", "voice": "af_heart", "response_format": "pcm"},
            "headers": {"Authorization": "Bearer not-needed", "Content-Type": "application/json"},
        }
    ]


def test_synthesize_concatenates():
    session = _FakeSession(_FakeResponse(200, chunks=[b"ab", b"cd"]))
    client = KokoroClient(base_url="http://localhost:8880/v1", session_factory=lambda: session)
    assert run(client.synthesize("x")) == b"abcd"


def test_non_200_raises_kokoro_error_with_status():
    session = _FakeSession(_FakeResponse(503, text="model loading"))
    client = KokoroClient(base_url="http://localhost:8880/v1", session_factory=lambda: session)
    with pytest.raises(KokoroError) as exc:
        run(client.synthesize("x"))
    assert exc.value.status == 503
    assert "503" in str(exc.value)
    assert session.closed is True


def test_no_network_without_a_session_factory_until_called():
    # Constructing the client must not import aiohttp or open anything.
    client = KokoroClient(base_url="http://localhost:8880/v1")
    assert client.build_request("hello").json["input"] == "hello"
