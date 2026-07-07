"""Local voice → text.

The cloud learns the *shape* of a task, never the user's voice. Transcription
happens locally; the cloud never receives audio. v0 is a stub — a real
whisper.cpp / on-device ASR backend plugs in behind `transcribe`.
"""

from __future__ import annotations

from typing import Optional


def transcribe(audio: bytes, *, transcript: Optional[str] = None) -> str:
    """Return text for the given audio. In v0, pass `transcript=` to simulate a
    local ASR result; the audio bytes are never returned or forwarded."""
    if transcript is not None:
        return transcript
    return f"[local-asr-stub: {len(audio)} bytes transcribed on-device]"
