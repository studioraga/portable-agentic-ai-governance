#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.."&&pwd)";SRC="${1:?M15 verifier material required}";DST="${2:-$HOME/.config/portable-ai-governance/m15}"
if find "$SRC" -maxdepth 1 -type f \( -name 'signing-private.pem' -o -name '*private*.pem' \) -print|grep -q .;then echo 'FAIL: Node2 must not receive M15 private signing key' >&2;exit 2;fi
"$ROOT/deploy/m15/deploy_node.sh" node2 "$SRC" "$DST"
python3 "$ROOT/scripts/m15/validate_m15_node.py" --material "$DST" --repo-root "$ROOT"
echo 'PASS: Node2 M15 independent-verifier PSIRT/CVD/user-notification foundation complete'
