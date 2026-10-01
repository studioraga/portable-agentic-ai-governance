from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


# Immutable M20 baseline on which M21 was designed and validated.
M20_BASELINE_COMMIT = (
    "8b800814e576bcb08e12dc47c1039c5251c79d46"
)

# Immutable release tag identifying the M20 production-freeze baseline.
M20_BASELINE_TAG = (
    "m20-cra-enterprise-final-freeze-v0.20.0"
)


def sha256_file(path: str | Path) -> str:
    path = Path(path)

    digest = hashlib.sha256()

    with path.open("rb") as file_obj:
        for block in iter(
            lambda: file_obj.read(1024 * 1024),
            b"",
        ):
            digest.update(block)

    return digest.hexdigest()


def write_json(
    path: str | Path,
    obj: Any,
) -> None:
    path = Path(path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        json.dumps(
            obj,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )

    path.chmod(0o600)
