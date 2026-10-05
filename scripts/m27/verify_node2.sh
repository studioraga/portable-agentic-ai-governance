#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd);MAT=${1:?usage: verify_node2.sh MATERIAL_DIR};export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
if find "$MAT" -maxdepth 1 -iname '*private*.pem' | grep -q .; then echo 'FAIL: private key present in Node2 verifier material'; exit 2; fi
python3 "$ROOT/scripts/m27/validate_m27_node.py" --material "$MAT" --repo-root "$ROOT"
echo 'PASS: Node2 M27 verifier-only AppSec evidence verified'
