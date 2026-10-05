#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd);MAT=${1:-$ROOT/var/m27-material};export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
test -f "$MAT/signing-private.pem" || { echo 'FAIL: Node1 M27 private key missing'; exit 2; }
python3 "$ROOT/scripts/m27/validate_m27_node.py" --material "$MAT" --repo-root "$ROOT"
echo 'PASS: Node1 M27 AppSec authority verified'
