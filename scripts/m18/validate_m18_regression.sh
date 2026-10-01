#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)";cd "$ROOT";export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
git diff --check
python3 -m pytest -q
for m in 11 12 13 14 15 16 17 18; do "./scripts/m${m}/validate_m${m}_local.sh"; done
echo 'PASS: full M0-M18 regression + M11/M12/M13/M14/M15/M16/M17/M18 acceptance complete'
