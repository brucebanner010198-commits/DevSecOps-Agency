"""B2 — the dual-interface app model (the watchable desktop's trust core).

Each app exposes two interfaces: a human GUI (represented here by app state) and a
typed, structured **side-car agent API** that agents call instead of
screen-scraping. Every side-car call is routed through the B1 Trust Kernel, so it
is verifier-gated, capability-checked, and receipted.

Why this matters: there are no pixels to OCR and no buttons to trick the agent
into clicking. A prompt injection hidden inside a message body cannot make a
hijacked agent send mail or exfiltrate, because the agent simply lacks the
capability for `comms.send` / `net.egress` — the attack is refused structurally,
exactly as in the M3 least-privilege demo.

The native Wayland compositor (real windows, secure-attention sequence) is a later
native effort; this package is the runnable trust core that proves the primitive.
"""

__version__ = "0.1.0"
