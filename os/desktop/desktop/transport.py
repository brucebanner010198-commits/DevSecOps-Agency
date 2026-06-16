"""Local-only JSON-RPC transport for the side-car (Unix domain socket).

Agents talk to apps over a local socket — never a network port — so the agent
API has no remote attack surface. Each request is one JSON line:

    {"actor": "...", "app": "...", "method": "...", "params": {...},
     "golden_share": "<hex, optional>"}

The server hands every request to the SideCar, which routes it through the Trust
Kernel. This is a thin, dependency-free transport for the demo and tests.
"""

from __future__ import annotations

import hmac
import json
import os
import socket
import threading
from typing import Any, Dict, Optional

from .sidecar import SideCar


def _frame(obj: Dict[str, Any]) -> bytes:
    return (json.dumps(obj) + "\n").encode("utf-8")


def _read_line(conn: socket.socket) -> bytes:
    data = b""
    while not data.endswith(b"\n"):
        chunk = conn.recv(4096)
        if not chunk:
            break
        data += chunk
    return data


class SideCarServer:
    def __init__(
        self,
        sidecar: SideCar,
        socket_path: str,
        tokens: Optional[Dict[str, str]] = None,
    ) -> None:
        self.sidecar = sidecar
        self.socket_path = socket_path
        # actor → connection token. When set, every request must carry the token
        # bound to the actor it claims, so a local process cannot impersonate
        # another (more-privileged) actor by simply asserting its name. The
        # `actor` string drives every capability/attribution decision, so it
        # MUST be authenticated at the untrusted socket boundary.
        self._tokens = tokens
        self._srv: Optional[socket.socket] = None
        self._thread: Optional[threading.Thread] = None
        self._stop = False

    def start(self) -> "SideCarServer":
        if os.path.exists(self.socket_path):
            os.unlink(self.socket_path)
        self._srv = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self._srv.bind(self.socket_path)
        # Owner-only: only same-uid processes may even connect (defence in depth
        # beneath the per-actor token check).
        try:
            os.chmod(self.socket_path, 0o600)
        except OSError:  # pragma: no cover - non-POSIX
            pass
        self._srv.listen(8)
        self._srv.settimeout(0.5)
        self._thread = threading.Thread(target=self._serve, daemon=True)
        self._thread.start()
        return self

    def _authenticate(self, req: Dict[str, Any]) -> bool:
        if self._tokens is None:
            return True  # no auth configured (trusted single-agent / test mode)
        actor = req.get("actor", "")
        expected = self._tokens.get(actor)
        got = req.get("token")
        if expected is None or not isinstance(got, str):
            return False
        return hmac.compare_digest(expected, got)

    def _serve(self) -> None:
        while not self._stop:
            try:
                conn, _ = self._srv.accept()  # type: ignore[union-attr]
            except socket.timeout:
                continue
            except OSError:
                break
            with conn:
                raw = _read_line(conn)
                if not raw:
                    continue
                conn.sendall(_frame(self._handle(raw)))

    def _handle(self, raw: bytes) -> Dict[str, Any]:
        try:
            req = json.loads(raw.decode("utf-8"))
            if not self._authenticate(req):
                return {
                    "ok": False,
                    "decision": "unauthorized",
                    "reason": "actor authentication failed (missing/invalid connection token)",
                }
            gs = bytes.fromhex(req["golden_share"]) if req.get("golden_share") else None
            r = self.sidecar.call(
                req["actor"],
                req["app"],
                req["method"],
                req.get("params"),
                golden_share=gs,
                nonce=req.get("nonce"),
            )
            return {
                "ok": r.ok,
                "decision": r.decision,
                "reason": r.reason,
                "result": r.result,
                "receipt_id": r.receipt_id,
            }
        except Exception as e:  # noqa: BLE001 - transport returns errors, never crashes
            return {"ok": False, "decision": "error", "reason": f"{type(e).__name__}: {e}"}

    def stop(self) -> None:
        self._stop = True
        if self._thread:
            self._thread.join(timeout=2)
        if self._srv:
            self._srv.close()
        if os.path.exists(self.socket_path):
            try:
                os.unlink(self.socket_path)
            except OSError:
                pass


def call_sidecar(
    socket_path: str,
    actor: str,
    app: str,
    method: str,
    params: Optional[Dict[str, Any]] = None,
    *,
    golden_share: Optional[bytes] = None,
    nonce: Optional[str] = None,
    token: Optional[str] = None,
) -> Dict[str, Any]:
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.connect(socket_path)
    with client:
        payload: Dict[str, Any] = {
            "actor": actor,
            "app": app,
            "method": method,
            "params": params or {},
        }
        if golden_share is not None:
            payload["golden_share"] = golden_share.hex()
        if nonce is not None:
            payload["nonce"] = nonce
        if token is not None:
            payload["token"] = token
        client.sendall(_frame(payload))
        raw = _read_line(client)
    return json.loads(raw.decode("utf-8"))
