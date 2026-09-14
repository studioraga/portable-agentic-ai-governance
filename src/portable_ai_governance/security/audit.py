from __future__ import annotations

import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from ..kernel.evidence import EvidenceLedger


@dataclass(frozen=True)
class SecurityEvent:
    event_type: str
    decision: str
    principal_id: str = ""
    action: str = ""
    resource: str = ""
    reason: str = ""
    run_id: str = ""
    attributes: dict[str, Any] = field(default_factory=dict)
    timestamp: int = field(default_factory=lambda: int(time.time()))


class SecurityAuditLog:
    """Signed/chained security-event log; audit writes are evidence, not authorization."""

    def __init__(self, path: str | Path, signing_key: bytes, key_id: str = "audit-v1"):
        self.ledger = EvidenceLedger(path, signing_key, key_id=key_id)

    def record(self, event: SecurityEvent) -> str:
        envelope = self.ledger.append("security_event", asdict(event))
        return envelope["envelope_sha256"]

    def verify(self) -> tuple[bool, str]:
        return self.ledger.verify()
