#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.."&&pwd)";export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
python3 -m pytest -q "$ROOT/tests/cra_reporting"
TMP="$(mktemp -d)";trap 'rm -rf "$TMP"' EXIT
python3 "$ROOT/scripts/m14/build_m14_material.py" --out "$TMP/m14-material"
python3 "$ROOT/scripts/m14/validate_m14_node.py" --material "$TMP/m14-material" --repo-root "$ROOT"
rm -f "$TMP/m14-material/signing-private.pem"
python3 "$ROOT/scripts/m14/validate_m14_node.py" --material "$TMP/m14-material" --repo-root "$ROOT"
echo 'PASS: M14 CRA Reporting & ENISA SRP Evidence Pack local + verifier-only validation complete'
