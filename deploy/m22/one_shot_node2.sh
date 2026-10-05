#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)";SRC="$1";DEST="${2:-$HOME/.config/portable-ai-governance/m22}"
"$ROOT/deploy/m22/deploy_node.sh" node2 "$SRC" "$DEST"
"$ROOT/scripts/m22/verify_node2.sh" "$DEST"
echo 'PASS: Node2 M22 independent enterprise-control verifier complete'
