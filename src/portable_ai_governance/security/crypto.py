from __future__ import annotations

import hashlib
import hmac
from dataclasses import dataclass

from .secrets import SecretProvider


@dataclass(frozen=True)
class CryptoService:
    provider: SecretProvider

    def sign(self, domain: str, payload: bytes) -> str:
        key = self.provider.get(f"{domain}_signing", minimum_bytes=32)
        return hmac.new(key, payload, hashlib.sha256).hexdigest()

    def verify(self, domain: str, payload: bytes, signature: str) -> bool:
        expected = self.sign(domain, payload)
        return hmac.compare_digest(expected, signature)

    @staticmethod
    def sha256(payload: bytes) -> str:
        return hashlib.sha256(payload).hexdigest()
