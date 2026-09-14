from __future__ import annotations

import os
import stat
from pathlib import Path
from typing import Protocol


class SecretError(RuntimeError):
    pass


class SecretProvider(Protocol):
    def get(self, name: str, *, minimum_bytes: int = 32) -> bytes: ...
    def health(self) -> tuple[bool, str]: ...


class EnvironmentSecretProvider:
    """Bootstrap/lab provider. Production profiles should prefer a protected provider."""

    def __init__(self, prefix: str = "PAG_"):
        self.prefix = prefix

    def get(self, name: str, *, minimum_bytes: int = 32) -> bytes:
        key = f"{self.prefix}{name.upper()}"
        value = os.environ.get(key, "")
        raw = value.encode()
        if len(raw) < minimum_bytes:
            raise SecretError(f"{key} missing or shorter than {minimum_bytes} bytes")
        return raw

    def health(self) -> tuple[bool, str]:
        return True, "environment provider available"


class FileSecretProvider:
    """Sovereign/offline secret provider with strict owner-only filesystem controls."""

    def __init__(self, root: str | Path):
        self.root = Path(root)

    @staticmethod
    def _mode(path: Path) -> int:
        return stat.S_IMODE(path.stat().st_mode)

    def health(self) -> tuple[bool, str]:
        try:
            if not self.root.is_dir():
                return False, "secret root missing"
            mode = self._mode(self.root)
            if mode & 0o077:
                return False, f"secret root permissions too open: {oct(mode)}"
            return True, "file secret provider available"
        except OSError as exc:
            return False, str(exc)

    def get(self, name: str, *, minimum_bytes: int = 32) -> bytes:
        ok, detail = self.health()
        if not ok:
            raise SecretError(detail)
        if not name or "/" in name or ".." in name:
            raise SecretError("invalid secret name")
        path = self.root / f"{name}.key"
        try:
            resolved = path.resolve(strict=True)
            if resolved.parent != self.root.resolve(strict=True):
                raise SecretError("secret path escaped provider root")
            mode = self._mode(resolved)
            if mode & 0o077:
                raise SecretError(f"secret permissions too open: {oct(mode)}")
            raw = resolved.read_bytes().strip()
        except SecretError:
            raise
        except OSError as exc:
            raise SecretError(f"secret unavailable: {name}: {exc}") from exc
        if len(raw) < minimum_bytes:
            raise SecretError(f"secret {name} shorter than {minimum_bytes} bytes")
        return raw
