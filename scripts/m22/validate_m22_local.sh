#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"; export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
python3 -m pytest -q tests/enterprise_security
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
python3 scripts/m22/build_m22_material.py --out "$T/m22-material"
python3 scripts/m22/validate_m22_node.py --material "$T/m22-material" --repo-root "$ROOT"
rm -f "$T/m22-material/signing-private.pem"
python3 scripts/m22/validate_m22_node.py --material "$T/m22-material" --repo-root "$ROOT"
echo 'PASS: M22 local producer + verifier-only validation complete'
