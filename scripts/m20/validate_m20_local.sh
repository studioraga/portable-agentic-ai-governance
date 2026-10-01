#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)";export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}";T="$(mktemp -d)";trap 'rm -rf "$T"' EXIT
python3 -m pytest -q "$ROOT/tests/cra_final_freeze"
python3 "$ROOT/scripts/m20/build_m20_material.py" --m19-summary "$ROOT/tests/fixtures/m20/m19-production-validation-summary.json" --out "$T/m20-material"
python3 "$ROOT/scripts/m20/validate_m20_node.py" --material "$T/m20-material" --repo-root "$ROOT"
python3 "$ROOT/scripts/m20/run_secure_agentic_demo.py" --mode node1 --out "$T/demo" --case "$ROOT/examples/secure-agentic-node1-node2/case.json"
python3 "$ROOT/scripts/m20/run_secure_agentic_demo.py" --mode node2 --trace "$T/demo/secure-agentic-trace.json" --public-key "$T/demo/human-review-public.pem"
echo 'PASS: M20 Enterprise One-Shot Deployment / Final Production Freeze local validation complete'
