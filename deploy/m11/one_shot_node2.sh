#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.."&&pwd)";SRC="${1:?verifier-only M11 material directory}";DEST="${2:-$HOME/.config/portable-ai-governance/m11}"
if test -f "$SRC/signing-private.pem";then echo 'FAIL: Node2 must not receive M11 private signing key' >&2;exit 2;fi
"$ROOT/deploy/m11/deploy_node.sh" "$SRC" "$DEST"
echo 'PASS: Node2 M11 independent-verifier foundation complete'
