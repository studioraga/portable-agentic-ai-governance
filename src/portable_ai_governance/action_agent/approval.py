from __future__ import annotations
import fcntl, json, os, tempfile, time
from dataclasses import asdict, dataclass, fields
from pathlib import Path
from .common import canonical_json_bytes, sha256_bytes
from ..supply_chain.signing import sign_blob, verify_blob

SIGNED_APPROVAL_SCHEMA = "pag-m8-signed-approval-v1"

class ApprovalError(RuntimeError):
    pass

@dataclass(frozen=True)
class ApprovalRequest:
    request_id: str
    run_id: str
    call_id: str
    tool_name: str
    resource: str
    requester: str
    arguments_sha256: str

@dataclass(frozen=True)
class ApprovalGrant:
    approval_id: str
    request_sha256: str
    tool_name: str
    resource: str
    requester: str
    approver: str
    arguments_sha256: str
    issued_at: int
    expires_at: int
    max_uses: int = 1

@dataclass(frozen=True)
class SignedApproval:
    grant: ApprovalGrant
    signature: str

def request_sha256(req: ApprovalRequest) -> str:
    return sha256_bytes(canonical_json_bytes(asdict(req)))

def _write_grant(path: Path, grant: ApprovalGrant) -> None:
    path.write_bytes(canonical_json_bytes(asdict(grant)))
    os.chmod(path, 0o600)

def _is_sha256(value: str) -> bool:
    return len(value) == 64 and all(c in "0123456789abcdef" for c in value)

class ApprovalIssuer:
    """Release/operator-side Ed25519 approval signer. Never deployed to verifier-only nodes."""
    def __init__(self, private_key):
        self.private_key = Path(private_key)
        if not self.private_key.is_file():
            raise ApprovalError("approval private key missing")

    def sign(self, grant: ApprovalGrant) -> str:
        with tempfile.TemporaryDirectory() as td:
            blob = Path(td) / "grant.json"
            sig = Path(td) / "grant.sig"
            _write_grant(blob, grant)
            sign_blob(blob, self.private_key, sig)
            return sig.read_text().strip()

class ApprovalVerifier:
    """Verifier-side Ed25519 approval verification using public material only."""
    def __init__(self, public_key, *, max_ttl_seconds: int = 1800, clock_skew_seconds: int = 60):
        self.public_key = Path(public_key)
        if not self.public_key.is_file():
            raise ApprovalError("approval public key missing")
        self.max_ttl_seconds = int(max_ttl_seconds)
        self.clock_skew_seconds = int(clock_skew_seconds)
        if not 60 <= self.max_ttl_seconds <= 3600:
            raise ApprovalError("approval TTL policy outside supported range")
        if not 0 <= self.clock_skew_seconds <= 300:
            raise ApprovalError("approval clock skew policy outside supported range")

    def verify(self, signed: SignedApproval, *, now: int | None = None) -> None:
        g = signed.grant
        n = int(time.time()) if now is None else int(now)
        with tempfile.TemporaryDirectory() as td:
            blob = Path(td) / "grant.json"
            sig = Path(td) / "grant.sig"
            _write_grant(blob, g)
            sig.write_text(signed.signature + "\n")
            if not verify_blob(blob, self.public_key, sig):
                raise ApprovalError("approval signature invalid")
        if g.requester == g.approver:
            raise ApprovalError("self-approval prohibited")
        if g.max_uses != 1:
            raise ApprovalError("approval must be single-use")
        if g.issued_at > n + self.clock_skew_seconds:
            raise ApprovalError("approval issued in the future")
        if g.expires_at <= g.issued_at or n >= g.expires_at:
            raise ApprovalError("approval expired")
        if g.expires_at - g.issued_at > self.max_ttl_seconds:
            raise ApprovalError("approval TTL exceeds signed policy maximum")

def signed_approval_to_dict(x: SignedApproval) -> dict:
    return {"schema": SIGNED_APPROVAL_SCHEMA, "grant": asdict(x.grant), "signature": x.signature}

def signed_approval_from_dict(d: dict) -> SignedApproval:
    if not isinstance(d, dict) or set(d) != {"schema", "grant", "signature"}:
        raise ApprovalError("invalid signed approval envelope")
    if d.get("schema") != SIGNED_APPROVAL_SCHEMA:
        raise ApprovalError("unexpected signed approval schema")
    grant_doc = d.get("grant")
    if not isinstance(grant_doc, dict):
        raise ApprovalError("approval grant must be an object")
    required = {f.name for f in fields(ApprovalGrant)}
    if set(grant_doc) != required:
        raise ApprovalError("approval grant fields invalid")
    try:
        grant = ApprovalGrant(**grant_doc)
    except (TypeError, ValueError) as exc:
        raise ApprovalError("approval grant values invalid") from exc
    for name in ("approval_id", "tool_name", "resource", "requester", "approver"):
        if not isinstance(getattr(grant, name), str) or not getattr(grant, name):
            raise ApprovalError(f"approval {name} invalid")
    if not _is_sha256(str(grant.request_sha256)) or not _is_sha256(str(grant.arguments_sha256)):
        raise ApprovalError("approval digest fields invalid")
    if not isinstance(grant.issued_at, int) or not isinstance(grant.expires_at, int) or not isinstance(grant.max_uses, int):
        raise ApprovalError("approval time/use fields invalid")
    signature = d.get("signature")
    if not isinstance(signature, str) or not signature.strip():
        raise ApprovalError("approval signature missing")
    return SignedApproval(grant, signature.strip())

class ApprovalUseStore:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        if not self.path.exists():
            self.path.touch(mode=0o600)
        os.chmod(self.path, 0o600)

    def claim(self, approval_id: str, *, run_id: str, call_id: str, request_sha256_value: str = "") -> None:
        with self.path.open("a+", encoding="utf-8") as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            f.seek(0)
            for line in f:
                if line.strip() and json.loads(line).get("approval_id") == approval_id:
                    raise ApprovalError("approval already used")
            f.seek(0, 2)
            record = {
                "approval_id": approval_id,
                "run_id": run_id,
                "call_id": call_id,
                "request_sha256": request_sha256_value,
                "used_at": int(time.time()),
            }
            f.write(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n")
            f.flush()
            os.fsync(f.fileno())
