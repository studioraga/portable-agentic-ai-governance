#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd);MAT=${1:-$ROOT/var/m29-material};PYTHONPATH="$ROOT/src" python3 "$ROOT/scripts/m29/validate_m29_node.py" --material "$MAT" --repo-root "$ROOT"
[ -f "$MAT/signing-private.pem" ] || { echo 'FAIL: Node1 authority private key missing'; exit 2; }
echo 'PASS: Node1 M29 cross-domain authority material verified'
