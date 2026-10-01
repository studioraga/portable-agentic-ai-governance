#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.."&&pwd)";SRC="${1:?M16 verifier material required}";DST="${2:-$HOME/.config/portable-ai-governance/m16}"
if find "$SRC" -maxdepth 1 -type f \( -name 'signing-private.pem' -o -name '*private*.pem' \) -print|grep -q .;then echo 'FAIL: Node2 must not receive M16 private signing key' >&2;exit 2;fi
"$ROOT/deploy/m16/deploy_node.sh" node2 "$SRC" "$DST"
python3 "$ROOT/scripts/m16/validate_m16_node.py" --material "$DST" --repo-root "$ROOT"
echo 'PASS: Node2 M16 independent-verifier secure-update/product-lifecycle foundation complete'
