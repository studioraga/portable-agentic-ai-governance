from __future__ import annotations

import stat

from portable_ai_governance.kernel.evidence import (
    EvidenceLedger,
)


def test_evidence_ledger_is_owner_only(tmp_path):
    path = tmp_path / "governance.jsonl"

    ledger = EvidenceLedger(
        path,
        b"x" * 32,
    )

    ledger.append(
        "test_event",
        {"value": 1},
    )

    mode = stat.S_IMODE(
        path.stat().st_mode
    )

    assert mode == 0o600
