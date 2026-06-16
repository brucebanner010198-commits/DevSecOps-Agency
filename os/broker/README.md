# B3 — De-identification trust broker

The "identity stays home" proof. The broker is the **only** egress path to a cloud
model, and before anything leaves it:

1. **masks** real entities (names, emails, cards, phones, paths) → synthetic
   surrogates, keeping the reversible map **local-only**;
2. **normalizes** writing style to blunt stylometric re-identification;
3. relies on **local voice→text** (the cloud never receives audio);
4. routes egress through the **B1 Trust Kernel** — default-deny host allowlist, a
   signed receipt on every send, and a **golden-share** gate for sensitive egress;
5. **re-identifies** the cloud reply locally, so the user sees real names the cloud
   never saw.

Identity-bearing inference runs on a **local model**; only de-identified text is
eligible to leave.

## What's here

```
broker/
  surrogates.py    # entity → surrogate masking, local-only reversible map
  stylometry.py    # style normalization (pluggable local LDP paraphraser)
  voice.py         # local voice→text (stub; whisper.cpp backend plugs in)
  local_model.py   # LocalModel interface + stub (llama.cpp/Ollama plug in)
  broker.py        # TrustBroker — masks, routes egress through the kernel, re-identifies
tests/             # 11 tests (masking, no-leak, default-deny, on-disk audit, golden-share)
demos/b3_broker_demo.py
```

## Run it

```bash
cd os/broker
python3 -m pytest -q                  # 11 passing
python3 demos/b3_broker_demo.py       # real-vs-sent, default-deny, audit, golden-share
```

## What the demo proves

- The **sent** text contains **no** real entities; the **real** text and the
  surrogate map never leave the device.
- The on-disk **receipt log holds no real identity** (only the masked text is hashed in).
- Egress to a non-allowlisted host is **default-denied**; the cloud call never runs.
- A **sensitive** send is held until the Owner's **golden-share** signs the exact
  masked payload they reviewed.

## Scope note

The real on-device LLM serving (llama.cpp / Ollama) and a production LDP paraphrase
model plug in behind `LocalModel` / `normalize_style(paraphraser=…)`. v0 ships
deterministic stubs so the **trust flow** — mask → default-deny → receipt →
re-identify — is fully runnable and tested without a model download.
