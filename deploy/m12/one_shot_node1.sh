#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.."&&pwd)";OUT="${1:-$ROOT/var/m12-material}"
rm -rf "$OUT";python3 "$ROOT/scripts/m12/build_m12_material.py" --out "$OUT";"$ROOT/deploy/m12/deploy_node.sh" node1 "$OUT" "${2:-$HOME/.config/portable-ai-governance/m12}"
echo "PASS: Node1 M12 vulnerability/exploitation intelligence authority complete at $OUT"
