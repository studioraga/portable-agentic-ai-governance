#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd);export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}";TMP=$(mktemp -d);trap 'rm -rf "$TMP"' EXIT
python3 "$ROOT/scripts/m24/build_m24_material.py" --out "$TMP/material"
python3 "$ROOT/scripts/m24/validate_m24_node.py" --material "$TMP/material" --repo-root "$ROOT"
rm -f "$TMP/material/signing-private.pem"
python3 "$ROOT/scripts/m24/validate_m24_node.py" --material "$TMP/material" --repo-root "$ROOT"
echo 'PASS: M24 local producer and verifier-only validation'
