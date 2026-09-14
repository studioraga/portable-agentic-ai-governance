from __future__ import annotations

import hashlib
import hmac
import json
import stat
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from .types import Principal


class IdentityError(RuntimeError):
    pass


class IdentityProvider(Protocol):
    def authenticate(self, credential: str) -> Principal: ...
    def health(self) -> tuple[bool, str]: ...


@dataclass(frozen=True)
class ApiKeyIdentity:
    name: str
    digest: str
    roles: tuple[str, ...]
    attributes: dict[str, str] | None = None


class LocalIdentityProvider:
    """Bootstrap identity provider. Production startup rejects this provider."""

    def __init__(self, identities: list[ApiKeyIdentity]):
        self._identities = identities

    @staticmethod
    def digest_token(token: str) -> str:
        return hashlib.sha256(token.encode()).hexdigest()

    def health(self) -> tuple[bool, str]:
        return True, "local identity provider available"

    def authenticate(self, token: str) -> Principal:
        digest = self.digest_token(token)
        for identity in self._identities:
            if hmac.compare_digest(identity.digest, digest):
                return Principal(identity.name, identity.roles, dict(identity.attributes or {}))
        raise IdentityError("invalid credential")


class FileIdentityProvider:
    """Offline enterprise bootstrap adapter with hashed tokens and owner-only file protection."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self._identities = self._load()

    @staticmethod
    def _mode(path: Path) -> int:
        return stat.S_IMODE(path.stat().st_mode)

    def health(self) -> tuple[bool, str]:
        if not self.path.is_file():
            return False, "identity file missing"
        mode = self._mode(self.path)
        if mode & 0o077:
            return False, f"identity file permissions too open: {oct(mode)}"
        return True, "file identity provider available"

    def _load(self) -> list[ApiKeyIdentity]:
        if not self.path.is_file():
            raise IdentityError(f"identity file missing: {self.path}")
        mode = self._mode(self.path)
        if mode & 0o077:
            raise IdentityError(f"identity file permissions too open: {oct(mode)}")
        try:
            root = json.loads(self.path.read_text(encoding="utf-8"))
            records = root["identities"]
            if not isinstance(records, list) or not records:
                raise ValueError("identities must be a non-empty list")
            out = []
            names: set[str] = set()
            digests: set[str] = set()
            for item in records:
                name = str(item["name"])
                digest = str(item["token_sha256"])
                roles = tuple(str(x) for x in item.get("roles", ()))
                attrs = {str(k): str(v) for k, v in item.get("attributes", {}).items()}
                if not name or len(digest) != 64 or not roles:
                    raise ValueError("invalid identity record")
                if name in names or digest in digests:
                    raise ValueError("duplicate identity name or token digest")
                names.add(name); digests.add(digest)
                out.append(ApiKeyIdentity(name, digest, roles, attrs))
            return out
        except Exception as exc:
            if isinstance(exc, IdentityError):
                raise
            raise IdentityError(f"identity file invalid: {exc}") from exc

    def authenticate(self, token: str) -> Principal:
        digest = LocalIdentityProvider.digest_token(token)
        for identity in self._identities:
            if hmac.compare_digest(identity.digest, digest):
                return Principal(identity.name, identity.roles, dict(identity.attributes or {}))
        raise IdentityError("invalid credential")
