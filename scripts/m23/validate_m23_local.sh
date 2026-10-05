#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)";cd "$ROOT";export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
python3 -m pytest -q tests/enterprise_identity
T="$(mktemp -d)";trap 'rm -rf "$T"' EXIT
python3 scripts/m23/build_m23_material.py --out "$T/m23-material"
python3 scripts/m23/validate_m23_node.py --material "$T/m23-material" --repo-root "$ROOT"
rm -f "$T/m23-material"/*-private.pem
python3 scripts/m23/validate_m23_node.py --material "$T/m23-material" --repo-root "$ROOT"
echo 'PASS: M23 local producer + verifier-only validation complete'
