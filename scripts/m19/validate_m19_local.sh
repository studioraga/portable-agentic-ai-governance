#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)";cd "$ROOT";export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
python3 -m pytest -q tests/cra_production_validation
T="$(mktemp -d)";trap 'rm -rf "$T"' EXIT
python3 scripts/m19/build_m19_material.py --out "$T/m19-material" --node1-profile tests/fixtures/m19/node1-runtime-profile.json --node2-profile tests/fixtures/m19/node2-runtime-profile.json
python3 scripts/m19/validate_m19_node.py --material "$T/m19-material" --repo-root "$ROOT"
python3 - "$T/m19-material/production-validation-summary.json" <<'SIMCHECK'
import json,sys
s=json.load(open(sys.argv[1]));assert s['validation_mode']=='SIMULATED';assert s['production_validation_complete'] is False;print('PASS: simulated acceptance cannot claim production validation')
SIMCHECK
./deploy/m19/package_verifier_material.sh "$T/m19-material" "$T/m19-verifier.tar.gz"
mkdir -m700 "$T/extract";tar -xzf "$T/m19-verifier.tar.gz" -C "$T/extract"
python3 scripts/m19/validate_m19_node.py --material "$T/extract/m19-material" --repo-root "$ROOT"
if find "$T/extract" -type f -iname '*private*' -print | grep -q .;then echo 'FAIL: verifier material contains private key';exit 2;fi
echo 'PASS: M19 CRA Node1/Node2 Production Validation local + verifier-only validation complete'
