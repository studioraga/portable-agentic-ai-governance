#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)";cd "$ROOT";export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
git diff --check
python3 -m pytest -q
./scripts/m11/validate_m11_local.sh
./scripts/m12/validate_m12_local.sh
./scripts/m13/validate_m13_local.sh
./scripts/m14/validate_m14_local.sh
./scripts/m15/validate_m15_local.sh
./scripts/m16/validate_m16_local.sh
./scripts/m17/validate_m17_local.sh
echo "PASS: full M0-M17 regression + M11/M12/M13/M14/M15/M16/M17 acceptance complete"
