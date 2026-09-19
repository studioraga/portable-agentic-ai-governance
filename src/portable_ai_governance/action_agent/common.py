from __future__ import annotations
import hashlib, json, os
from pathlib import Path

def canonical_json_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()

def sha256_bytes(value: bytes):
    return hashlib.sha256(value).hexdigest()

def sha256_file(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def load_json(path):
    return json.loads(Path(path).read_text())

def write_private_json(path, value):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    p.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.chmod(p, 0o600)
    return p

def secure_tree(root):
    root = Path(root)
    for p in [root, *root.rglob("*")]:
        try:
            os.chmod(p, 0o700 if p.is_dir() else 0o600)
        except FileNotFoundError:
            pass
