#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)";SRC="${1:?verifier material}";DST="${2:-$HOME/.config/portable-ai-governance/m20}";[[ ! -e "$SRC/signing-private.pem" ]]||{ echo 'FAIL: Node2 must not receive M20 private signing key';exit 2;};"$ROOT/deploy/m20/deploy_node.sh" "$SRC" "$DST";python3 "$ROOT/scripts/m20/validate_m20_node.py" --material "$DST" --repo-root "$ROOT";echo 'PASS: Node2 M20 enterprise verifier complete'
