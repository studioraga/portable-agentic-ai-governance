#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.."&&pwd)";OUT="${1:-$ROOT/var/m11-material}"
export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
python3 "$ROOT/scripts/m11/build_m11_material.py" --out "$OUT"
python3 "$ROOT/scripts/m11/validate_m11_node.py" --material "$OUT" --repo-root "$ROOT"
echo "PASS: Node1 M11 CRA release-authority foundation complete at $OUT"
