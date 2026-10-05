#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd);cd "$ROOT";export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
python3 -m pytest -q tests/organizational_security tests/acceptance/test_framework_mapping.py
./scripts/m28/validate_m28_local.sh
./scripts/m27/validate_m27_local.sh
git diff --check
echo 'PASS: M28 regression gate'
