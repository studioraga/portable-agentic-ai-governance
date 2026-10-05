#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)";cd "$ROOT";export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
python3 -m pytest -q
./scripts/m22/validate_m22_local.sh
./scripts/m23/validate_m23_local.sh
echo 'PASS: M0-M23 regression and M22->M23 compatibility validation complete'
