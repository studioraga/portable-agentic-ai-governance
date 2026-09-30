#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.."&&pwd)";SRC="${1:?M12 verifier material required}";DEST="${2:-$HOME/.config/portable-ai-governance/m12}"
"$ROOT/deploy/m12/deploy_node.sh" node2 "$SRC" "$DEST";echo 'PASS: Node2 M12 independent-verifier foundation complete'
