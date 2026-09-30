#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
python3 -m pytest -q "$ROOT/tests/cra_vulnerability_intel"
TMP="$(mktemp -d)";trap 'rm -rf "$TMP"' EXIT
python3 "$ROOT/scripts/m12/build_m12_material.py" --out "$TMP/m12-material"
python3 "$ROOT/scripts/m12/validate_m12_node.py" --material "$TMP/m12-material" --repo-root "$ROOT"
rm -f "$TMP/m12-material/signing-private.pem"
python3 "$ROOT/scripts/m12/validate_m12_node.py" --material "$TMP/m12-material" --repo-root "$ROOT"
echo 'PASS: M12 CRA Vulnerability & Exploitation Intelligence local + verifier-only validation complete'
