#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)";OUT="${1:-$ROOT/var/m18-material}";export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
python3 "$ROOT/scripts/m18/build_m18_material.py" --out "$OUT"
python3 "$ROOT/scripts/m18/validate_m18_node.py" --material "$OUT" --repo-root "$ROOT"
"$ROOT/deploy/m18/deploy_node.sh" node1 "$OUT" "$HOME/.config/portable-ai-governance/m18"
install -m600 "$OUT/signing-private.pem" "$HOME/.config/portable-ai-governance/m18/signing-private.pem"
echo "PASS: Node1 M18 Annex-VII technical-file authority complete at $OUT"
