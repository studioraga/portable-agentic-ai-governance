from __future__ import annotations
import hashlib, hmac, json, time
from dataclasses import dataclass, asdict

@dataclass(frozen=True)
class Approval:
    approval_id: str
    action: str
    resource: str
    requester: str
    approver: str
    expires_at: int
    max_uses: int = 1

class ApprovalSigner:
    def __init__(self, key: bytes):
        if len(key) < 32:
            raise ValueError("approval signing key must be at least 32 bytes")
        self.key = key

    def sign(self, approval: Approval) -> str:
        payload = json.dumps(asdict(approval), sort_keys=True, separators=(",", ":")).encode()
        return hmac.new(self.key, payload, hashlib.sha256).hexdigest()

    def verify(self, approval: Approval, signature: str, *, now: int | None = None) -> bool:
        expected = self.sign(approval)
        return hmac.compare_digest(expected, signature) and (now or int(time.time())) <= approval.expires_at
