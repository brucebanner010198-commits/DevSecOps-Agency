"""B3 — the de-identification trust broker (the "identity stays home" proof).

The broker is the only path from the device to a cloud model. Before anything
leaves, it:

  1. masks real entities (names, emails, cards, phones, paths) → synthetic
     surrogates, keeping the reversible map *local only*;
  2. normalizes writing style to blunt stylometric fingerprinting;
  3. (voice→text happens locally first — the cloud never receives audio);
  4. routes the egress through the B1 Trust Kernel — default-deny host allowlist,
     a signed receipt on every send, and a golden-share gate for sensitive egress;
  5. re-identifies the cloud reply locally, so the user sees real names the cloud
     never did.

Identity-bearing inference runs on a *local* model; only de-identified text is
ever eligible to leave. The real local-LLM backend (llama.cpp / Ollama) plugs in
behind `LocalModel`; v0 ships a stub so the trust flow is runnable without a
model download.
"""

__version__ = "0.1.0"
