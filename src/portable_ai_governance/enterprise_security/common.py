from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

M21_1_BASELINE_COMMIT = "ea952069938a6435ccb298f5424bab158197ce05"
M21_1_BASELINE_TAG = "m21-embedded-linux-platform-security-v0.21.1"
M22_VERSION = "0.22.0"

def sha256_file(path: str | Path) -> str:
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda:f.read(1024*1024), b""):
            h.update(block)
    return h.hexdigest()

def write_json(path: str | Path, obj: Any) -> None:
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n")
    p.chmod(0o600)
