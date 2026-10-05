#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd);cd "$ROOT";export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
python3 -m pytest -q tests/enterprise_validation tests/acceptance/test_framework_mapping.py
./scripts/m29/validate_m29_local.sh
./scripts/m28/validate_m28_local.sh
git diff --check
echo 'PASS: M29 regression gate'
