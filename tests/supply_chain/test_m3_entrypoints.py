from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def _run_help(script: Path) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    return subprocess.run(
        [sys.executable, str(script), "--help"],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def test_validate_m3_node_direct_entrypoint_without_pythonpath():
    result = _run_help(ROOT / "scripts/m3/validate_m3_node.py")
    assert result.returncode == 0, result.stderr


def test_build_m3_material_direct_entrypoint_without_pythonpath():
    result = _run_help(ROOT / "scripts/m3/build_m3_material.py")
    assert result.returncode == 0, result.stderr
