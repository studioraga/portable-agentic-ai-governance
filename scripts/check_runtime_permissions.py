#!/usr/bin/env python3

from __future__ import annotations

import os
import stat
import tempfile
from pathlib import Path

from portable_ai_governance.kernel.evidence import (
    EvidenceLedger,
)


def require(
    name: str,
    condition: bool,
) -> None:
    if not condition:
        raise SystemExit(
            f"FAIL {name}"
        )

    print(
        f"PASS {name}"
    )


with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)

    evidence = root / "governance.jsonl"

    ledger = EvidenceLedger(
        evidence,
        b"x" * 32,
    )

    ledger.append(
        "permission_test",
        {"ok": True},
    )

    file_mode = stat.S_IMODE(
        evidence.stat().st_mode
    )

    require(
        "evidence-ledger-mode-0600",
        file_mode == 0o600,
    )


print(
    "RUNTIME-PERMISSION TESTS PASS"
)
