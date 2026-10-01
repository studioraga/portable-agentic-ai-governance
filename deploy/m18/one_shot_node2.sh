#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)";SRC="${1:?verifier material directory required}";DST="${2:-$HOME/.config/portable-ai-governance/m18}";export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
"$ROOT/deploy/m18/deploy_node.sh" node2 "$SRC" "$DST"
python3 "$ROOT/scripts/m18/validate_m18_node.py" --material "$DST" --repo-root "$ROOT"
echo 'PASS: Node2 M18 independent-verifier foundation complete'
