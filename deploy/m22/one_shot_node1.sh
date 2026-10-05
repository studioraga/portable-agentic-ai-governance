#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)";OUT="${1:-$ROOT/var/m22-material}";export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
python3 "$ROOT/scripts/m22/build_m22_material.py" --out "$OUT"
"$ROOT/deploy/m22/deploy_node.sh" node1 "$OUT" "$HOME/.config/portable-ai-governance/m22"
"$ROOT/scripts/m22/verify_node1.sh" "$OUT"
echo 'PASS: Node1 M22 enterprise-control authority complete'
