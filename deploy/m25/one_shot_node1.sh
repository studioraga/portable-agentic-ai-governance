#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd);OUT=${1:-$ROOT/var/m25-material};export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
python3 "$ROOT/scripts/m25/build_m25_material.py" --out "$OUT";"$ROOT/scripts/m25/verify_node1.sh" "$OUT";"$ROOT/deploy/m25/package_verifier_material.sh" "$OUT" "$ROOT/var/m25-verifier.tar.gz"
