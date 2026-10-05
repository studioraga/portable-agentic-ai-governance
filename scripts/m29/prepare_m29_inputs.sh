#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd);cd "$ROOT";export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
# M21 is a frozen platform prerequisite; reuse its existing signed material.
[ -d var/m21-material ] || { echo 'FAIL: var/m21-material missing; recreate/validate M21 first'; exit 2; }
for m in 22 23 24 25 26 27 28; do
  echo "=== regenerate M${m} evidence against current source tree ==="
  python3 "scripts/m${m}/build_m${m}_material.py" --out "var/m${m}-material"
done
echo 'PASS: M21-M28 prerequisite evidence available for M29'
