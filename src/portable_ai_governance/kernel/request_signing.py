"""Portable adaptation of the source project's direction-scoped HMAC request signing pattern."""
from __future__ import annotations
import hashlib, hmac, secrets, time
from dataclasses import dataclass

@dataclass(frozen=True)
class SignedRequest:
    timestamp: int
    nonce: str
    body_sha256: str
    signature: str


def _canonical(method: str, path: str, timestamp: int, nonce: str, body_sha256: str) -> bytes:
    return "\n".join((method.upper(), path, str(timestamp), nonce, body_sha256)).encode()


def sign_request(secret: bytes, *, method: str, path: str, body: bytes, timestamp: int | None = None, nonce: str | None = None) -> SignedRequest:
    if len(secret) < 32:
        raise ValueError("signing secret must be at least 32 bytes")
    ts = int(time.time()) if timestamp is None else int(timestamp)
    n = secrets.token_hex(16) if nonce is None else nonce
    digest = hashlib.sha256(body).hexdigest()
    signature = hmac.new(secret, _canonical(method, path, ts, n, digest), hashlib.sha256).hexdigest()
    return SignedRequest(ts, n, digest, signature)


def verify_request(secret: bytes, request: SignedRequest, *, method: str, path: str, body: bytes, max_skew_sec: int = 300, now: int | None = None) -> bool:
    current = int(time.time()) if now is None else int(now)
    if abs(current - request.timestamp) > max_skew_sec:
        return False
    digest = hashlib.sha256(body).hexdigest()
    if not hmac.compare_digest(digest, request.body_sha256):
        return False
    expected = hmac.new(secret, _canonical(method, path, request.timestamp, request.nonce, request.body_sha256), hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, request.signature)
