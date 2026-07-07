# B2 — Watchable desktop (dual-interface app model)

The trust core of the observable AI desktop. Apps expose a **typed side-car agent
API** (JSON-RPC over a local Unix socket) *beside* their human interface, and
every agent call is routed through the **B1 Trust Kernel** — verifier-gated,
capability-checked, receipted.

> Why it stands out: there are **no pixels to OCR and no buttons to trick the
> agent into clicking**. The agent calls typed methods; an injection hidden in a
> message body cannot make a hijacked agent send or exfiltrate, because it lacks
> the capability (`comms.send` → `network_egress`). This kills the screen-scraping
> prompt-injection class structurally, not by detection.

## What's here

```
desktop/
  apps.py        # FilesApp, SheetApp, CommsApp — typed methods, each mapped to a trust action
  sidecar.py     # the dispatcher: routes every call through the Trust Kernel; human can seize control
  transport.py   # local-only JSON-RPC over a Unix domain socket (no network port)
tests/           # 8 tests (dispatch, injection-blocked, golden-share send, human-seize, socket round-trip)
demos/b2_dual_interface_demo.py
```

## Run it

```bash
cd os/desktop
python3 -m pytest -q                       # 8 passing
python3 demos/b2_dual_interface_demo.py    # the full scene
```

## What the demo proves

- The agent acts through a **structured API**, every call a signed receipt.
- A prompt injection in an inbox message **cannot** make the assistant exfiltrate
  — it holds no `network_egress` (M3 lethal-trifecta separation, reused here).
- The human can **seize control** at any instant; agent calls pause.
- A legitimate outbound send is **reserved** — it runs only with the Owner's
  **golden-share** signature over that exact message.

## Scope note

This is the runnable trust core. The native graphical compositor — real windows,
a secure-attention sequence for the golden-share prompt, live on-screen takeover —
is a later native effort (Wayland). The security-relevant primitive (typed
side-car + trust routing) is what's built and tested here.
