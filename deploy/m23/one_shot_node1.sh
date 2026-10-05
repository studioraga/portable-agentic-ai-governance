#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)";OUT="${1:-$ROOT/var/m23-material}";export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
python3 "$ROOT/scripts/m23/build_m23_material.py" --out "$OUT"
"$ROOT/deploy/m23/deploy_node.sh" node1 "$OUT" "$HOME/.config/portable-ai-governance/m23"
"$ROOT/scripts/m23/verify_node1.sh" "$OUT"
echo 'PASS: Node1 M23 enterprise identity/MFA/PAM authority complete'
