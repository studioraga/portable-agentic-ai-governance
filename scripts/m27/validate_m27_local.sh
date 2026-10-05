#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd);TMP=$(mktemp -d);trap 'rm -rf "$TMP"' EXIT
export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
python3 "$ROOT/scripts/m27/build_m27_material.py" --out "$TMP/material"
python3 "$ROOT/scripts/m27/validate_m27_node.py" --material "$TMP/material" --repo-root "$ROOT"
rm "$TMP/material/signing-private.pem"
python3 "$ROOT/scripts/m27/validate_m27_node.py" --material "$TMP/material" --repo-root "$ROOT"
echo 'PASS: M27 local producer and verifier-only validation'
