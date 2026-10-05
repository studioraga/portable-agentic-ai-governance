from __future__ import annotations
import json
from pathlib import Path

def load_json(path: str | Path):
    return json.loads(Path(path).read_text())

def control_ids(control_catalog: dict) -> set[str]:
    return {c["control_id"] for c in control_catalog.get("controls", [])}
