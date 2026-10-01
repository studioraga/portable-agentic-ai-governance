#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)";cd "$ROOT";export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
python3 -m pytest -q tests/cra_technical_file
T="$(mktemp -d)";trap 'rm -rf "$T"' EXIT
python3 scripts/m18/build_m18_material.py --out "$T/m18-material"
python3 scripts/m18/validate_m18_node.py --material "$T/m18-material" --repo-root "$ROOT"
./deploy/m18/package_verifier_material.sh "$T/m18-material" "$T/m18-verifier.tar.gz"
mkdir -m700 "$T/extract";tar -xzf "$T/m18-verifier.tar.gz" -C "$T/extract"
python3 scripts/m18/validate_m18_node.py --material "$T/extract/m18-material" --repo-root "$ROOT"
if find "$T/extract" -type f -iname '*private*' -print | grep -q .; then echo 'FAIL: verifier material contains private key';exit 2;fi
echo 'PASS: M18 CRA Annex-VII Technical Documentation / Technical File local + verifier-only validation complete'
