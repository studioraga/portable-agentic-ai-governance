#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)";cd "$ROOT";export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
python3 -m pytest -q tests/cra_annex_evidence
T="$(mktemp -d)";trap 'rm -rf "$T"' EXIT
python3 scripts/m17/build_m17_material.py --out "$T/m17-material"
python3 scripts/m17/validate_m17_node.py --material "$T/m17-material" --repo-root "$ROOT"
python3 scripts/m17/validate_m17_node.py --material "$T/m17-material" --repo-root "$ROOT"
echo "PASS: M17 CRA Annex-I Compliance Evidence local + verifier-only validation complete"
