"""Voice surface v0: the spoken front door of Personal AI Mode.

A LiveKit voice loop (Silero VAD, STT, one routing brain, Kokoro TTS) in front
of a local-first brain that recalls memories, classifies the request, answers
from a local Ollama model or a cloud model, and saves the turn back to memory.

Scaffolded from two prototypes (JARVIS-1.0 for the session skeleton,
JARVIS-2.0 for the brain rule, memory design and Kokoro contract). See
README.md for what was taken, what was rejected, and what is still a stub.

Modules:
  config.py        env-driven settings; secrets have no defaults
  brain/router.py  request classification and local-vs-cloud choice
  brain/memory.py  save / recall interface, in-memory store, mem0 stub
  tts/kokoro.py    request contract and client for a local Kokoro server
  agent.py         LiveKit entry point (the only module that imports livekit)
"""

__version__ = "0.1.0"
