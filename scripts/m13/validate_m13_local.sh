#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.."&&pwd)";export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
python3 -m pytest -q "$ROOT/tests/cra_incident_clock"
TMP="$(mktemp -d)";trap 'rm -rf "$TMP"' EXIT
python3 "$ROOT/scripts/m13/build_m13_material.py" --out "$TMP/m13-material"
python3 "$ROOT/scripts/m13/validate_m13_node.py" --material "$TMP/m13-material" --repo-root "$ROOT"
rm -f "$TMP/m13-material/signing-private.pem"
python3 "$ROOT/scripts/m13/validate_m13_node.py" --material "$TMP/m13-material" --repo-root "$ROOT"
echo 'PASS: M13 CRA Incident Classification & Statutory Clock local + verifier-only validation complete'
