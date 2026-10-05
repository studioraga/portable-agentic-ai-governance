#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd);cd "$ROOT";export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}";TMP=$(mktemp -d);trap 'rm -rf "$TMP"' EXIT
python3 scripts/m28/build_m28_material.py --out "$TMP/material"
python3 scripts/m28/validate_m28_node.py --material "$TMP/material" --repo-root "$ROOT"
rm -f "$TMP/material/signing-private.pem"
python3 scripts/m28/validate_m28_node.py --material "$TMP/material" --repo-root "$ROOT"
echo 'PASS: M28 local producer and verifier-only validation'
