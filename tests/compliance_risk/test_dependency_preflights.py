from __future__ import annotations

import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _run(path: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    return subprocess.run(
        [str(ROOT / path)],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def test_m4_dependency_preflight_has_no_tomllib_requirement() -> None:
    text = (ROOT / "scripts/m4/preflight_dependencies.sh").read_text()
    assert "import tomllib" not in text
    result = _run("scripts/m4/preflight_dependencies.sh")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "M4 DEPENDENCY PREFLIGHT: PASS" in result.stdout


def test_m5_dependency_preflight_has_no_tomllib_requirement() -> None:
    text = (ROOT / "scripts/m5/preflight_dependencies.sh").read_text()
    assert "import tomllib" not in text
    result = _run("scripts/m5/preflight_dependencies.sh")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "M5 DEPENDENCY PREFLIGHT: PASS" in result.stdout
