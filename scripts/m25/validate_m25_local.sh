#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd);export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}";TMP=$(mktemp -d);trap 'rm -rf "$TMP"' EXIT
python3 "$ROOT/scripts/m25/build_m25_material.py" --out "$TMP/material"
python3 "$ROOT/scripts/m25/validate_m25_node.py" --material "$TMP/material" --repo-root "$ROOT"
rm -f "$TMP/material/signing-private.pem"
python3 "$ROOT/scripts/m25/validate_m25_node.py" --material "$TMP/material" --repo-root "$ROOT"
echo 'PASS: M25 local producer and verifier-only validation'
