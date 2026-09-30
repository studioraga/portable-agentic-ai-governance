#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.."&&pwd)";MAT="${1:-$HOME/.config/portable-ai-governance/m13}"
if find "$MAT" -maxdepth 1 -type f \( -name 'signing-private.pem' -o -name '*private*.pem' \) -print|grep -q .;then echo 'FAIL: Node2 contains M13 private signing material' >&2;exit 2;fi
python3 "$ROOT/scripts/m13/validate_m13_node.py" --material "$MAT" --repo-root "$ROOT"
echo 'PASS: Node2 M13 verifier-only material verified'
