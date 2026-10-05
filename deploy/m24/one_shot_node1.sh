#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd);OUT=${1:-$ROOT/var/m24-material};export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
python3 "$ROOT/scripts/m24/build_m24_material.py" --out "$OUT";"$ROOT/scripts/m24/verify_node1.sh" "$OUT";"$ROOT/deploy/m24/package_verifier_material.sh" "$OUT" "$ROOT/var/m24-verifier.tar.gz"
