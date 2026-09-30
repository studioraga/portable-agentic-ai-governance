#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.."&&pwd)";OUT="${1:-$ROOT/var/m13-material}"
rm -rf "$OUT";python3 "$ROOT/scripts/m13/build_m13_material.py" --out "$OUT";"$ROOT/deploy/m13/deploy_node.sh" node1 "$OUT" "${2:-$HOME/.config/portable-ai-governance/m13}"
echo "PASS: Node1 M13 incident-classification/statutory-clock authority complete at $OUT"
