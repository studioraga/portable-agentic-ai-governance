#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)";cd "$ROOT";export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
git -c safe.directory="$ROOT" diff --check
python3 -m pytest -q
./scripts/m20/validate_m20_local.sh
./scripts/m21/validate_m21_local.sh
echo 'PASS: full M0-M21 regression + M20/M21 acceptance complete'
