from __future__ import annotations
import json, os, time
from pathlib import Path

class ReplayDetected(RuntimeError):
    pass

class PersistentNonceCache:
    """Persistent bounded anti-replay cache; fail closed on malformed state."""
    def __init__(self, path: str | Path, *, ttl_sec: int = 600, max_entries: int = 10000):
        self.path = Path(path)
        self.ttl_sec = ttl_sec
        self.max_entries = max_entries
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _load(self) -> dict[str, int]:
        if not self.path.exists():
            return {}
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                raise ValueError("cache root must be object")
            return {str(k): int(v) for k, v in data.items()}
        except Exception as exc:
            raise RuntimeError(f"nonce cache unreadable; fail closed: {exc}") from exc

    def consume(self, nonce: str, *, now: int | None = None) -> None:
        current = int(time.time()) if now is None else int(now)
        data = {k: v for k, v in self._load().items() if current - v <= self.ttl_sec}
        if nonce in data:
            raise ReplayDetected("nonce replay detected")
        data[nonce] = current
        if len(data) > self.max_entries:
            data = dict(sorted(data.items(), key=lambda x: x[1], reverse=True)[: self.max_entries])
        tmp = self.path.with_suffix(self.path.suffix + ".tmp")
        tmp.write_text(json.dumps(data, sort_keys=True), encoding="utf-8")
        os.chmod(tmp, 0o600)
        os.replace(tmp, self.path)
