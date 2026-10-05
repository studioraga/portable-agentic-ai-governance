#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd);MAT=${1:?usage: verify_node2.sh MATERIAL};RECEIPT=${2:-$MAT/node2-independent-verification.json}
[ ! -f "$MAT/signing-private.pem" ] || { echo 'FAIL: verifier material contains private key'; exit 2; }
PYTHONPATH="$ROOT/src" python3 "$ROOT/scripts/m29/validate_m29_node.py" --material "$MAT" --repo-root "$ROOT"
python3 "$ROOT/scripts/m29/write_node2_receipt.py" --material "$MAT" --out "$RECEIPT"
echo "PASS: Node2 M29 independent cross-domain evidence verified; receipt=$RECEIPT"
