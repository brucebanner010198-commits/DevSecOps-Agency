import os
import socket
import threading
import time

import pytest

from desktop.apps import FilesApp
from desktop.sidecar import SideCar
from desktop.transport import (
    MAX_LINE_BYTES,
    SideCarServer,
    _FrameTooLarge,
    _peer_uid,
    _read_line,
    call_sidecar,
)
from trust_spine.capabilities import FS_READ, FS_WRITE, CapabilityBroker
from trust_spine.kernel import TrustKernel
from trust_spine.ledger import Ledger
from trust_spine.policy import Policy
from trust_spine.verifier import Verifier


def test_socket_round_trip(tmp_path):
    broker = CapabilityBroker()
    broker.grant("assistant", {FS_READ, FS_WRITE})
    led = Ledger(str(tmp_path / "led"))
    kernel = TrustKernel(led, Verifier(Policy(), capability_broker=broker))
    sc = SideCar(kernel, {"files": FilesApp()})

    # AF_UNIX paths are capped (~104 chars on macOS); keep it short, not under tmp_path.
    sock = f"/tmp/tsb2_{os.getpid()}.sock"
    server = SideCarServer(sc, sock).start()
    try:
        resp = call_sidecar(sock, "assistant", "files", "list", {})
        assert resp["ok"] is True
        assert "readme.txt" in resp["result"]

        w = call_sidecar(
            sock, "assistant", "files", "write", {"path": "a.txt", "content": "x"}
        )
        assert w["ok"] is True
        assert led.verify_receipt(w["receipt_id"])["ok"] is True
    finally:
        server.stop()
    assert not os.path.exists(sock)


def test_actor_token_authentication_blocks_impersonation(tmp_path):
    """Red-team fix: the `actor` drives every capability/attribution decision, so
    a request over the socket must prove it owns the actor it claims. A connection
    without the bound token — or impersonating another actor — is rejected before
    the call reaches the kernel."""
    broker = CapabilityBroker()
    broker.grant("assistant", {FS_READ, FS_WRITE})
    led = Ledger(str(tmp_path / "led"))
    kernel = TrustKernel(led, Verifier(Policy(), capability_broker=broker))
    sc = SideCar(kernel, {"files": FilesApp()})

    sock = f"/tmp/tsb2auth_{os.getpid()}.sock"
    tokens = {"assistant": "s3cret-token"}
    server = SideCarServer(sc, sock, tokens=tokens).start()
    try:
        ok = call_sidecar(sock, "assistant", "files", "list", {}, token="s3cret-token")
        assert ok["ok"] is True

        missing = call_sidecar(sock, "assistant", "files", "list", {})
        assert missing["ok"] is False and missing["decision"] == "unauthorized"

        # impersonating the privileged actor with the wrong token → rejected
        spoof = call_sidecar(sock, "assistant", "files", "list", {}, token="wrong")
        assert spoof["ok"] is False and spoof["decision"] == "unauthorized"
    finally:
        server.stop()


# =============================================================================
# Second red-team pass (2026-06-16) — findings F2, F3
# =============================================================================

def _server(tmp_path, name):
    broker = CapabilityBroker()
    broker.grant("assistant", {FS_READ, FS_WRITE})
    led = Ledger(str(tmp_path / "led"))
    kernel = TrustKernel(led, Verifier(Policy(), capability_broker=broker))
    sc = SideCar(kernel, {"files": FilesApp()})
    sock = f"/tmp/{name}_{os.getpid()}.sock"
    return SideCarServer(sc, sock).start(), sock


def test_slow_client_does_not_block_other_agents(tmp_path):
    """F2: a connection that opens and never completes its frame must not stall
    the server for everyone else. Previously the single-flight blocking accept
    loop let one silent client starve every agent indefinitely."""
    server, sock = _server(tmp_path, "tsb2slow")
    attacker = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        attacker.connect(sock)
        attacker.sendall(b'{"actor":"x","app":"files"')  # partial frame, no newline
        time.sleep(0.2)  # ensure the server has picked up the stalled connection

        t0 = time.time()
        resp = call_sidecar(sock, "assistant", "files", "list", {})
        elapsed = time.time() - t0
        assert resp["ok"] is True
        assert elapsed < 3.0, f"legit call blocked for {elapsed:.2f}s by a silent client"
    finally:
        attacker.close()
        server.stop()


def test_read_line_refuses_oversized_frame():
    """F2: `_read_line` is bounded, so an attacker cannot drive unbounded memory
    growth by never sending a newline (CWE-770). The flood runs on its own thread
    because the data exceeds the socket buffer (sendall would otherwise block
    waiting for the reader we are about to start)."""
    a, b = socket.socketpair()

    def flood():
        try:
            b.sendall(b"x" * (MAX_LINE_BYTES + 4096))  # no newline, over the cap
        except OSError:
            pass  # reader closed after refusing

    t = threading.Thread(target=flood, daemon=True)
    t.start()
    try:
        with pytest.raises(_FrameTooLarge):
            _read_line(a)
    finally:
        a.close()
        b.close()
        t.join(timeout=2)


def test_peer_uid_is_readable_for_same_uid_connection(tmp_path):
    """F3: the transport can read the kernel-attested peer uid, so the same-uid
    enforcement (which fails closed even if the 0600 socket perm was lost) is
    live rather than a silent no-op on this platform."""
    srv = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    path = f"/tmp/tsb2peer_{os.getpid()}.sock"
    if os.path.exists(path):
        os.unlink(path)
    srv.bind(path)
    srv.listen(1)
    cli = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        cli.connect(path)
        conn, _ = srv.accept()
        assert _peer_uid(conn) == os.getuid()
        conn.close()
    finally:
        cli.close()
        srv.close()
        os.unlink(path)
