#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.."&&pwd)";export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
python3 -m pytest -q "$ROOT/tests/cra_secure_update"
TMP="$(mktemp -d)";trap 'rm -rf "$TMP"' EXIT
python3 "$ROOT/scripts/m16/build_m16_material.py" --out "$TMP/m16-material"
python3 "$ROOT/scripts/m16/validate_m16_node.py" --material "$TMP/m16-material" --repo-root "$ROOT"
rm -f "$TMP/m16-material/signing-private.pem"
python3 "$ROOT/scripts/m16/validate_m16_node.py" --material "$TMP/m16-material" --repo-root "$ROOT"
echo 'PASS: M16 CRA Secure Update & Product Lifecycle local + verifier-only validation complete'
