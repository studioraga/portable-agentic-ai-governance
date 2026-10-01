#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)";OUT="${1:-$ROOT/var/m17-material}"
export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}";python3 "$ROOT/scripts/m17/build_m17_material.py" --out "$OUT";python3 "$ROOT/scripts/m17/validate_m17_node.py" --material "$OUT" --repo-root "$ROOT";echo "PASS: Node1 M17 Annex-I evidence authority complete at $OUT"
