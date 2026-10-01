#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)";SRC="${1:?material directory required}";DST="${2:-$HOME/.config/portable-ai-governance/m17}"
"$ROOT/deploy/m17/deploy_node.sh" node2 "$SRC" "$DST";"$ROOT/scripts/m17/verify_node2.sh" "$DST";echo "PASS: Node2 M17 independent-verifier foundation complete"
