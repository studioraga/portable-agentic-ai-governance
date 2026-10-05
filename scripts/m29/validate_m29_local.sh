#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd);cd "$ROOT";export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
TMP=$(mktemp -d);trap 'rm -rf "$TMP"' EXIT
./scripts/m29/prepare_m29_inputs.sh
python3 scripts/m29/build_m29_material.py --out "$TMP/material"
python3 scripts/m29/validate_m29_node.py --material "$TMP/material" --repo-root "$ROOT"
rm -f "$TMP/material/signing-private.pem"
python3 scripts/m29/validate_m29_node.py --material "$TMP/material" --repo-root "$ROOT"
echo 'PASS: M29 local producer and verifier-only cross-domain validation'
