from __future__ import annotations
import hashlib, json
from pathlib import Path


def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_lock(lock_path: str | Path, base_dir: str | Path) -> tuple[bool, list[str]]:
    lock = json.loads(Path(lock_path).read_text(encoding="utf-8"))
    errors: list[str] = []
    base = Path(base_dir)
    for item in lock.get("artifacts", []):
        path = (base / item["path"]).resolve()
        if not path.is_file():
            errors.append(f"missing: {item['path']}")
            continue
        got = sha256_file(path)
        if got != item["sha256"]:
            errors.append(f"digest mismatch: {item['path']}")
    return not errors, errors
