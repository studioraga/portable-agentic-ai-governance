#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.."&&pwd)";OUT="${1:-$ROOT/var/m16-material}"
python3 "$ROOT/scripts/m16/build_m16_material.py" --out "$OUT"
python3 "$ROOT/scripts/m16/validate_m16_node.py" --material "$OUT" --repo-root "$ROOT"
"$ROOT/deploy/m16/deploy_node.sh" node1 "$OUT" "$HOME/.config/portable-ai-governance/m16"
echo "PASS: Node1 M16 secure-update/product-lifecycle authority complete at $OUT"
