#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)";SRC="${1:?material directory required}";export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
test ! -e "$SRC/signing-private.pem" || { echo 'FAIL: Node2 must not receive M17 private signing key'; exit 2; }
python3 "$ROOT/scripts/m17/validate_m17_node.py" --material "$SRC" --repo-root "$ROOT"
echo "PASS: Node2 M17 verifier-only material verified"
