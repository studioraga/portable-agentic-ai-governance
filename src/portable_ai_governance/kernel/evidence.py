from __future__ import annotations
import hashlib, hmac, json, os, time
from pathlib import Path
from typing import Any

class EvidenceLedger:
    """Append-only HMAC-chained evidence ledger adapted from the source project's signed provenance design."""
    def __init__(self, path: str | Path, signing_key: bytes, key_id: str = "local-v1"):
        if len(signing_key) < 32:
            raise ValueError("evidence signing key must be at least 32 bytes")
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.key = signing_key
        self.key_id = key_id

    @staticmethod
    def _canonical(obj: dict[str, Any]) -> bytes:
        return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()

    def _last_hash(self) -> str | None:
        if not self.path.exists() or not self.path.stat().st_size:
            return None
        last = self.path.read_text(encoding="utf-8").splitlines()[-1]
        return json.loads(last)["envelope_sha256"]

    def append(self, event_type: str, payload: dict[str, Any]) -> dict[str, Any]:
        core = {
            "event_type": event_type,
            "timestamp": int(time.time()),
            "key_id": self.key_id,
            "previous_envelope_sha256": self._last_hash(),
            "payload": payload,
            "payload_sha256": hashlib.sha256(self._canonical(payload)).hexdigest(),
        }
        envelope_sha = hashlib.sha256(self._canonical(core)).hexdigest()
        signature = hmac.new(self.key, envelope_sha.encode(), hashlib.sha256).hexdigest()
        envelope = {**core, "envelope_sha256": envelope_sha, "signature": signature}
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(envelope, sort_keys=True) + "\n")
            fh.flush(); os.fsync(fh.fileno())
        return envelope

    def verify(self) -> tuple[bool, str]:
        previous = None
        if not self.path.exists():
            return True, "empty ledger"
        for line_no, line in enumerate(self.path.read_text(encoding="utf-8").splitlines(), start=1):
            e = json.loads(line)
            if e["previous_envelope_sha256"] != previous:
                return False, f"chain mismatch at line {line_no}"
            payload_sha = hashlib.sha256(self._canonical(e["payload"])).hexdigest()
            if not hmac.compare_digest(payload_sha, e["payload_sha256"]):
                return False, f"payload digest mismatch at line {line_no}"
            core = {k: e[k] for k in ("event_type","timestamp","key_id","previous_envelope_sha256","payload","payload_sha256")}
            envelope_sha = hashlib.sha256(self._canonical(core)).hexdigest()
            if not hmac.compare_digest(envelope_sha, e["envelope_sha256"]):
                return False, f"envelope digest mismatch at line {line_no}"
            sig = hmac.new(self.key, envelope_sha.encode(), hashlib.sha256).hexdigest()
            if not hmac.compare_digest(sig, e["signature"]):
                return False, f"signature mismatch at line {line_no}"
            previous = envelope_sha
        return True, "verified"
