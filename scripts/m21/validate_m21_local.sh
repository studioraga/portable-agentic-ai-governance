#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"; export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
python3 -m pytest -q tests/platform_security
T="$(mktemp -d)";trap 'rm -rf "$T"' EXIT
python3 scripts/m21/build_m21_material.py --node1-profile tests/fixtures/m21/node1-profile.json --node2-profile tests/fixtures/m21/node2-profile.json --out "$T/m21-material"
python3 scripts/m21/validate_m21_node.py --material "$T/m21-material" --repo-root "$ROOT"
rm -f "$T/m21-material/signing-private.pem"
python3 scripts/m21/validate_m21_node.py --material "$T/m21-material" --repo-root "$ROOT"
echo 'PASS: M21 Embedded Linux & Platform Security local + verifier-only validation complete'
