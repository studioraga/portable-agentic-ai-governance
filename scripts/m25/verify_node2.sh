#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd);M=${1:?verifier material directory};export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
if find "$M" -type f -iname '*private*.pem' | grep -q .;then echo 'FAIL: private key present on Node2 material';exit 2;fi
python3 "$ROOT/scripts/m25/validate_m25_node.py" --material "$M" --repo-root "$ROOT"
echo 'PASS: Node2 M25 verifier-only network evidence verified'
