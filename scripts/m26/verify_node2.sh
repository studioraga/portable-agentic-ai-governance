#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd); MAT=${1:?usage: verify_node2.sh MATERIAL_DIR}
export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
if find "$MAT" -maxdepth 1 -type f -iname '*private*.pem' | grep -q .; then echo 'FAIL: private key present in verifier material';exit 1;fi
python3 "$ROOT/scripts/m26/validate_m26_node.py" --material "$MAT" --repo-root "$ROOT"
echo 'PASS: Node2 M26 verifier-only operational-security evidence verified'
