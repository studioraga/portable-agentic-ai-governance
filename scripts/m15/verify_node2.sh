#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.."&&pwd)";SRC="${1:?M15 verifier material required}";export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
if find "$SRC" -maxdepth 1 -type f \( -name 'signing-private.pem' -o -name '*private*.pem' \) -print|grep -q .;then echo 'FAIL: Node2 must not hold M15 private signing key' >&2;exit 2;fi
python3 "$ROOT/scripts/m15/validate_m15_node.py" --material "$SRC" --repo-root "$ROOT"
echo 'PASS: Node2 M15 verifier-only material verified'
