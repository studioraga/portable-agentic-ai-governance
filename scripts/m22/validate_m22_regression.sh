#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)";cd "$ROOT";export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
python3 -m pytest -q
./scripts/m21/validate_m21_local.sh
./scripts/m22/validate_m22_local.sh
echo 'PASS: M0-M22 regression and M21->M22 compatibility validation complete'
