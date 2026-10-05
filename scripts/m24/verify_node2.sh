#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd);M=${1:?usage: verify_node2.sh MATERIAL_DIR};export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
if find "$M" -maxdepth 1 -type f -iname '*private*.pem' -o -name 'signing-private.pem' | grep -q .; then echo 'FAIL: private key found in Node2 material';exit 2;fi
python3 "$ROOT/scripts/m24/validate_m24_node.py" --material "$M" --repo-root "$ROOT"
echo 'PASS: Node2 M24 verifier-only asset/data evidence verified'
