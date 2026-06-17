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
import struct
import sys
import threading
from typing import Any, Dict, Optional

from .sidecar import SideCar

# Resource bounds for the untrusted socket boundary. An unbounded read and a
# blocking single-flight accept loop let one local client exhaust memory or stall
# every other agent indefinitely (CWE-770 / CWE-400, slowloris). We cap the frame
# size, deadline every recv, bound concurrency, and serve each connection on its
# own worker so a slow/silent client cannot starve others. (Finding F2.)
MAX_LINE_BYTES = 64 * 1024          # a request frame above this is refused
RECV_TIMEOUT_SECONDS = 5.0          # no whole frame within this → drop the conn
MAX_CONCURRENT_CONNS = 16           # cap worker threads (bounded resource use)


class _FrameTooLarge(Exception):
    pass


def _frame(obj: Dict[str, Any]) -> bytes:
    return (json.dumps(obj) + "\n").encode("utf-8")


def _read_line(conn: socket.socket, max_bytes: int = MAX_LINE_BYTES) -> bytes:
    """Read one newline-terminated frame, bounded in size and (via the socket's
    timeout) in time. Refuses a frame over ``max_bytes`` instead of growing the
    buffer without limit."""
    data = b""
    while not data.endswith(b"\n"):
        chunk = conn.recv(4096)
        if not chunk:
            break
        data += chunk
        if len(data) > max_bytes:
            raise _FrameTooLarge(f"request frame exceeds {max_bytes} bytes")
    return data


def _peer_uid(conn: socket.socket) -> Optional[int]:
    """The connecting peer's uid as attested by the kernel (unspoofable), or None
    if this platform can't report it. Linux: SO_PEERCRED; macOS/BSD: getpeereid
    via libc (LOCAL_PEERCRED). (Finding F3.)"""
    try:
        if sys.platform.startswith("linux"):
            creds = conn.getsockopt(
                socket.SOL_SOCKET, socket.SO_PEERCRED, struct.calcsize("3i")
            )
            _pid, uid, _gid = struct.unpack("3i", creds)
            return uid
        # macOS / *BSD
        import ctypes
        import ctypes.util

        libc = ctypes.CDLL(ctypes.util.find_library("c"), use_errno=True)
        uid = ctypes.c_uint()
        gid = ctypes.c_uint()
        if libc.getpeereid(conn.fileno(), ctypes.byref(uid), ctypes.byref(gid)) != 0:
            return None
        return uid.value
    except Exception:  # pragma: no cover - exotic platforms
        return None


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
        # The kernel/ledger are single-writer; serialize the actual call so the
        # per-connection workers (added to stop one slow client starving others)
        # don't race on ledger append / nonce redeem.
        self._call_lock = threading.Lock()
        # Bound the number of concurrent workers so a flood of connections can't
        # spawn unbounded threads (CWE-770).
        self._slots = threading.BoundedSemaphore(MAX_CONCURRENT_CONNS)

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
            # Hand each connection to a bounded worker pool so one slow/silent
            # client cannot block the accept loop (and thus every other agent).
            if not self._slots.acquire(blocking=False):
                # At capacity: shed load fast rather than queueing unboundedly.
                try:
                    with conn:
                        conn.sendall(_frame({"ok": False, "decision": "busy",
                                             "reason": "server at capacity, retry"}))
                except OSError:
                    pass
                continue
            threading.Thread(target=self._handle_conn, args=(conn,), daemon=True).start()

    def _handle_conn(self, conn: socket.socket) -> None:
        try:
            conn.settimeout(RECV_TIMEOUT_SECONDS)  # deadline every recv (anti-slowloris)
            with conn:
                # Kernel-attested peer uid: even if the 0600 socket perm was lost
                # (or silently skipped on a non-POSIX FS), only same-uid processes
                # may transact. Determinable-and-mismatched fails closed.
                puid = _peer_uid(conn)
                if puid is not None and puid != os.getuid():
                    conn.sendall(_frame({"ok": False, "decision": "unauthorized",
                                         "reason": "peer uid mismatch"}))
                    return
                try:
                    raw = _read_line(conn)
                except (_FrameTooLarge, socket.timeout) as e:
                    conn.sendall(_frame({"ok": False, "decision": "error",
                                         "reason": f"{type(e).__name__}: {e}"}))
                    return
                except OSError:
                    return
                if not raw:
                    return
                conn.sendall(_frame(self._handle(raw)))
        except OSError:
            pass  # peer hung up mid-response; nothing to do
        finally:
            self._slots.release()

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
            with self._call_lock:  # serialize single-writer kernel/ledger access
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
