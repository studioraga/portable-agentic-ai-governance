#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd); TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
python3 "$ROOT/scripts/m26/build_m26_material.py" --out "$TMP/material"
python3 "$ROOT/scripts/m26/validate_m26_node.py" --material "$TMP/material" --repo-root "$ROOT"
rm "$TMP/material/signing-private.pem"
python3 "$ROOT/scripts/m26/validate_m26_node.py" --material "$TMP/material" --repo-root "$ROOT"
echo 'PASS: M26 local producer and verifier-only validation'
