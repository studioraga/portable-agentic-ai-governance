#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.."&&pwd)";cd "$ROOT";export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
python3 -m pytest -q tests/cra_foundation/test_m11_cra_foundation.py tests/acceptance/test_framework_mapping.py
TMP="$(mktemp -d)";trap 'rm -rf "$TMP"' EXIT
python3 "$ROOT/scripts/m11/build_m11_material.py" --out "$TMP/m11-material"
python3 "$ROOT/scripts/m11/validate_m11_node.py" --material "$TMP/m11-material" --repo-root "$ROOT"
test -f "$TMP/m11-material/signing-private.pem"
rm -f "$TMP/m11-material/signing-private.pem"
python3 "$ROOT/scripts/m11/validate_m11_node.py" --material "$TMP/m11-material" --repo-root "$ROOT"
echo 'PASS: M11 CRA Product Security Foundation local + verifier-only validation complete'
