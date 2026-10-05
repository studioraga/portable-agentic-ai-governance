#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd);cd "$ROOT";export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
python3 -m pytest -q tests/application_security tests/acceptance/test_framework_mapping.py
./scripts/m27/validate_m27_local.sh
./scripts/m26/validate_m26_local.sh
git diff --check
echo 'PASS: M27 regression gate'
