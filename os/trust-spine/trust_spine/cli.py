"""Trust Spine CLI — inspect and verify the receipt ledger offline.

    python -m trust_spine.cli --ledger ./.trust-ledger show-log
    python -m trust_spine.cli --ledger ./.trust-ledger verify-receipt <id>
    python -m trust_spine.cli --ledger ./.trust-ledger verify-log

`verify-receipt` exits 0 on PASS, 1 on FAIL — so it is usable as a gate in a
shell pipeline or CI step.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Optional, Sequence

from .ledger import Ledger


def cmd_verify_receipt(args: argparse.Namespace) -> int:
    res = Ledger(args.ledger).verify_receipt(args.receipt_id)
    print(json.dumps(res, indent=2))
    return 0 if res.get("ok") else 1


def cmd_verify_log(args: argparse.Namespace) -> int:
    res = Ledger(args.ledger).verify_log()
    print(json.dumps(res, indent=2))
    return 0 if res.get("ok") else 1


def cmd_show_log(args: argparse.Namespace) -> int:
    led = Ledger(args.ledger)
    for i, r in enumerate(led.all()):
        print(
            f"[{i}] {r.timestamp}  actor={r.actor:<16} action={r.action:<22} "
            f"tier={r.risk_tier} decision={r.decision:<7} id={r.receipt_id}"
        )
    root = led.root()
    print(f"-- {len(led)} receipts · alg={_alg(led)} · root={root[:16]}… ")
    return 0


def _alg(led: Ledger) -> str:
    rs = led.all()
    return rs[-1].algorithm if rs else "n/a"


def main(argv: Optional[Sequence[str]] = None) -> int:
    p = argparse.ArgumentParser(
        prog="trust-spine", description="Trust Spine v0 — receipts CLI"
    )
    p.add_argument(
        "--ledger", default="./.trust-ledger", help="ledger directory (default ./.trust-ledger)"
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    vr = sub.add_parser("verify-receipt", help="verify one receipt offline")
    vr.add_argument("receipt_id")
    vr.set_defaults(func=cmd_verify_receipt)

    vl = sub.add_parser("verify-log", help="verify every signature + chain link")
    vl.set_defaults(func=cmd_verify_log)

    sl = sub.add_parser("show-log", help="print the receipt log")
    sl.set_defaults(func=cmd_show_log)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
