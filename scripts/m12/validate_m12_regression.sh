#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.."&&pwd)";cd "$ROOT";export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
git diff --check
python3 -m pytest -q
./scripts/m11/validate_m11_local.sh
./scripts/m12/validate_m12_local.sh
echo 'PASS: full M0-M12 regression + M11/M12 acceptance complete'
