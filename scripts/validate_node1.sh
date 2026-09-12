#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
echo '=== Portable Agentic AI Governance: Node1 validation ==='
[ -x .venv/bin/python ] || { echo 'ERROR: run ./deploy/deploy_node1.sh first'; exit 2; }
source .venv/bin/activate
export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
export PAG_REPO_ROOT="$ROOT"
export PAG_SECURITY_PROFILE="${PAG_SECURITY_PROFILE:-lab}"

python -m compileall -q src
python -c 'import portable_ai_governance; print("imports: PASS", portable_ai_governance.__version__)'
python scripts/run_self_tests.py

PYTEST_PYTHON=""
if python -m pytest --version >/dev/null 2>&1; then
  PYTEST_PYTHON="$(command -v python)"
elif [ -n "${PAG_BASE_PYTHON:-}" ] && "$PAG_BASE_PYTHON" -m pytest --version >/dev/null 2>&1; then
  PYTEST_PYTHON="$PAG_BASE_PYTHON"
elif [ -r var/state/base_python.path ]; then
  candidate="$(cat var/state/base_python.path)"
  if [ -x "$candidate" ] && "$candidate" -m pytest --version >/dev/null 2>&1; then
    PYTEST_PYTHON="$candidate"
  fi
fi

if [ -n "$PYTEST_PYTHON" ]; then
  echo "pytest available: running extended suite with $PYTEST_PYTHON"
  "$PYTEST_PYTHON" -m pytest -q
else
  echo 'pytest not installed: extended pytest suite SKIPPED; install pytest for the full acceptance gate'
fi

python scripts/check_control_mapping.py
rm -f var/evidence/governance.jsonl
python -m portable_ai_governance.cli onboard --input examples/golden_onboarding/system.json --run-id validation-golden-001 > var/runs/golden-onboarding.json
python -m portable_ai_governance.cli verify-evidence
python -m portable_ai_governance.cli validate-security

echo 'PASS: Milestone 0 + Milestone 1 Node1 validation complete'
