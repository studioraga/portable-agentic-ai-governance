from __future__ import annotations
import hashlib, hmac
from dataclasses import dataclass
from .types import Principal

class IdentityError(RuntimeError):
    pass

@dataclass(frozen=True)
class ApiKeyIdentity:
    name: str
    digest: str
    roles: tuple[str, ...]

class LocalIdentityProvider:
    """Development/bootstrap identity provider. Production deployments should adapt OIDC/workload identity."""
    def __init__(self, identities: list[ApiKeyIdentity]):
        self._identities = identities

    @staticmethod
    def digest_token(token: str) -> str:
        return hashlib.sha256(token.encode()).hexdigest()

    def authenticate(self, token: str) -> Principal:
        digest = self.digest_token(token)
        for identity in self._identities:
            if hmac.compare_digest(identity.digest, digest):
                return Principal(identity.name, identity.roles)
        raise IdentityError("invalid credential")
