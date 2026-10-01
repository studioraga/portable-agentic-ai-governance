#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.."&&pwd)";OUT="${1:-$ROOT/var/m14-material}"
python3 "$ROOT/scripts/m14/build_m14_material.py" --out "$OUT"
python3 "$ROOT/scripts/m14/validate_m14_node.py" --material "$OUT" --repo-root "$ROOT"
"$ROOT/deploy/m14/deploy_node.sh" node1 "$OUT" "$HOME/.config/portable-ai-governance/m14"
echo "PASS: Node1 M14 reporting evidence authority complete at $OUT"
