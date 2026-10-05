#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd); MAT=${1:-$ROOT/var/m26-material}
export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
test -f "$MAT/signing-private.pem" || { echo 'FAIL: Node1 private signing key missing'; exit 1; }
python3 "$ROOT/scripts/m26/validate_m26_node.py" --material "$MAT" --repo-root "$ROOT"
TMP=$(mktemp -d);trap 'rm -rf "$TMP"' EXIT;cp -a "$MAT/." "$TMP/";rm "$TMP/signing-private.pem";python3 "$ROOT/scripts/m26/validate_m26_node.py" --material "$TMP" --repo-root "$ROOT"
echo 'PASS: Node1 M26 authority and verifier-package isolation verified'
