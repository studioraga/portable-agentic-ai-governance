#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.."&&pwd)";OUT="${1:-$ROOT/var/m15-material}"
python3 "$ROOT/scripts/m15/build_m15_material.py" --out "$OUT"
python3 "$ROOT/scripts/m15/validate_m15_node.py" --material "$OUT" --repo-root "$ROOT"
"$ROOT/deploy/m15/deploy_node.sh" node1 "$OUT" "$HOME/.config/portable-ai-governance/m15"
echo "PASS: Node1 M15 PSIRT/CVD/user-notification authority complete at $OUT"
