#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.."&&pwd)";export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
python3 -m pytest -q "$ROOT/tests/cra_psirt"
TMP="$(mktemp -d)";trap 'rm -rf "$TMP"' EXIT
python3 "$ROOT/scripts/m15/build_m15_material.py" --out "$TMP/m15-material"
python3 "$ROOT/scripts/m15/validate_m15_node.py" --material "$TMP/m15-material" --repo-root "$ROOT"
rm -f "$TMP/m15-material/signing-private.pem"
python3 "$ROOT/scripts/m15/validate_m15_node.py" --material "$TMP/m15-material" --repo-root "$ROOT"
echo 'PASS: M15 CRA PSIRT / CVD / User Notification local + verifier-only validation complete'
