#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd);cd "$ROOT";export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
python3 -m pytest -q tests/operational_security tests/acceptance/test_framework_mapping.py
./scripts/m26/validate_m26_local.sh
./scripts/m25/validate_m25_local.sh
git diff --check
echo 'PASS: M26 regression gate'
