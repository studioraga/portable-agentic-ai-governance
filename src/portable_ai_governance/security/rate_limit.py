from __future__ import annotations

import threading
import time
from dataclasses import dataclass


@dataclass
class _Bucket:
    window_start: int
    count: int


class FixedWindowRateLimiter:
    """Deterministic bounded in-process limiter; distributed adapters can replace it later."""

    def __init__(self, limit: int = 60, window_sec: int = 60):
        if limit <= 0 or window_sec <= 0:
            raise ValueError("limit and window_sec must be positive")
        self.limit = limit
        self.window_sec = window_sec
        self._lock = threading.Lock()
        self._buckets: dict[str, _Bucket] = {}

    def allow(self, key: str, *, now: int | None = None) -> tuple[bool, int]:
        current = int(time.time()) if now is None else int(now)
        window = current - (current % self.window_sec)
        with self._lock:
            bucket = self._buckets.get(key)
            if bucket is None or bucket.window_start != window:
                bucket = _Bucket(window, 0)
                self._buckets[key] = bucket
            if bucket.count >= self.limit:
                retry_after = max(1, self.window_sec - (current - window))
                return False, retry_after
            bucket.count += 1
            return True, 0
