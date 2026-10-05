#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd);cd "$ROOT";export PYTHONPATH="$PWD/src${PYTHONPATH:+:$PYTHONPATH}"
python3 -m pytest -q tests/network_security tests/acceptance/test_framework_mapping.py
./scripts/m25/validate_m25_local.sh
