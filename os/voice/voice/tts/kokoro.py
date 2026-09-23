"""Client for a local Kokoro-FastAPI text-to-speech server.

Request contract carried from JARVIS-2.0/livekit_agent/custom_tts.py lines 78
to 89 and confirmed against the Kokoro-FastAPI README:

  POST {KOKORO_URL}/audio/speech
  Authorization: Bearer <api key>      (the server has no auth; any value works)
  Content-Type: application/json
  {"model": "kokoro", "input": <text>, "voice": "af_heart", "response_format": "pcm"}

The body streams raw PCM, 24 kHz, mono. The sample width is not stated by
either source; livekit's openai TTS plugin treats "pcm" as 16-bit signed
little-endian, which is what the agent relies on.

The server and port come from KOKORO_URL (for example http://localhost:8880/v1).
Kokoro-FastAPI listens on 8880 inside its container; JARVIS-2.0 mapped host
8888 to container 8000, which is wrong, so the port lives in the environment.

agent.py does not use this client on the hot path: livekit's openai.TTS plugin
speaks the same OpenAI-compatible endpoint with less code, so agent.py points
that plugin at KOKORO_URL. This module is the request contract the tests pin,
and the fallback if the plugin route ever fails.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, AsyncIterator, Callable, Optional

MODEL = "kokoro"
DEFAULT_VOICE = "af_heart"
RESPONSE_FORMAT = "pcm"
MIME_TYPE = "audio/pcm"
SAMPLE_RATE = 24_000
NUM_CHANNELS = 1
SPEECH_PATH = "/audio/speech"
DEFAULT_CHUNK_BYTES = 4096


class KokoroError(RuntimeError):
    """The Kokoro server refused or failed a request."""

    def __init__(self, message: str, *, status: Optional[int] = None) -> None:
        super().__init__(message)
        self.status = status


@dataclass(frozen=True)
class KokoroRequest:
    """Everything needed to issue one synthesis request."""

    url: str
    headers: dict[str, str] = field(default_factory=dict)
    json: dict[str, Any] = field(default_factory=dict)
    method: str = "POST"


def speech_url(base_url: str) -> str:
    base = base_url.strip()
    if not base:
        raise ValueError("KOKORO_URL is empty")
    return base.rstrip("/") + SPEECH_PATH


def build_speech_request(
    *,
    base_url: str,
    text: str,
    voice: str = DEFAULT_VOICE,
    api_key: str = "not-needed",
    model: str = MODEL,
    response_format: str = RESPONSE_FORMAT,
) -> KokoroRequest:
    """Build the request without sending it."""
    if not text or not text.strip():
        raise ValueError("text is empty")
    if not voice or not voice.strip():
        raise ValueError("voice is empty")
    return KokoroRequest(
        url=speech_url(base_url),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "input": text,
            "voice": voice,
            "response_format": response_format,
        },
    )


SessionFactory = Callable[[], Any]


class KokoroClient:
    """Small async client. Network access only inside stream_pcm / synthesize.

    `session_factory` returns an aiohttp.ClientSession-like object. Tests pass
    a fake; production leaves it None and aiohttp is imported lazily.
    """

    def __init__(
        self,
        *,
        base_url: str,
        voice: str = DEFAULT_VOICE,
        api_key: str = "not-needed",
        timeout_s: float = 30.0,
        chunk_bytes: int = DEFAULT_CHUNK_BYTES,
        session_factory: Optional[SessionFactory] = None,
    ) -> None:
        self.base_url = base_url
        self.voice = voice
        self.api_key = api_key
        self.timeout_s = timeout_s
        self.chunk_bytes = chunk_bytes
        self._session_factory = session_factory

    @property
    def url(self) -> str:
        return speech_url(self.base_url)

    def build_request(self, text: str) -> KokoroRequest:
        return build_speech_request(
            base_url=self.base_url, text=text, voice=self.voice, api_key=self.api_key
        )

    def _new_session(self) -> Any:
        if self._session_factory is not None:
            return self._session_factory()
        import aiohttp  # lazy: keeps the module importable without aiohttp

        return aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout_s))

    async def stream_pcm(self, text: str) -> AsyncIterator[bytes]:
        """Yield raw PCM chunks as the server streams them."""
        request = self.build_request(text)
        session = self._new_session()
        try:
            async with session.post(
                request.url, json=request.json, headers=request.headers
            ) as response:
                if response.status != 200:
                    body = (await response.text())[:200]
                    raise KokoroError(
                        f"Kokoro returned HTTP {response.status} for {request.url}: {body}",
                        status=response.status,
                    )
                async for chunk in response.content.iter_chunked(self.chunk_bytes):
                    if chunk:
                        yield chunk
        finally:
            close = getattr(session, "close", None)
            if close is not None:
                result = close()
                if hasattr(result, "__await__"):
                    await result

    async def synthesize(self, text: str) -> bytes:
        """Whole utterance as one PCM byte string."""
        parts: list[bytes] = []
        async for chunk in self.stream_pcm(text):
            parts.append(chunk)
        return b"".join(parts)
