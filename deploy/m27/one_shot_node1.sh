#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd);OUT="$ROOT/var/m27-material";export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
python3 "$ROOT/scripts/m27/build_m27_material.py" --out "$OUT"
"$ROOT/scripts/m27/verify_node1.sh" "$OUT"
"$ROOT/deploy/m27/package_verifier_material.sh" "$OUT" "$ROOT/var/m27-verifier.tar.gz"
echo "PASS: Node1 M27 material generated at $OUT"
