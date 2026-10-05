#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd);cd "$ROOT";export PYTHONPATH="$PWD/src${PYTHONPATH:+:$PYTHONPATH}"
python3 -m pytest -q tests/asset_security
./scripts/m23/validate_m23_local.sh
./scripts/m24/validate_m24_local.sh
git diff --check
echo 'PASS: M24 regression gate'
