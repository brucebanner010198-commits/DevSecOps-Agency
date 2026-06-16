import os

from desktop.apps import FilesApp
from desktop.sidecar import SideCar
from desktop.transport import SideCarServer, call_sidecar
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
