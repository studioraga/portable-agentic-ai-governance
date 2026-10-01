#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.."&&pwd)";SRC="${1:?M14 verifier material required}";DST="${2:-$HOME/.config/portable-ai-governance/m14}"
if find "$SRC" -maxdepth 1 -type f \( -name 'signing-private.pem' -o -name '*private*.pem' \) -print|grep -q .;then echo 'FAIL: Node2 must not receive M14 private signing key' >&2;exit 2;fi
"$ROOT/deploy/m14/deploy_node.sh" node2 "$SRC" "$DST"
python3 "$ROOT/scripts/m14/validate_m14_node.py" --material "$DST" --repo-root "$ROOT"
echo 'PASS: Node2 M14 independent-verifier evidence-pack foundation complete'
