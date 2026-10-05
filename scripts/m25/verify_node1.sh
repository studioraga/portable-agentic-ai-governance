#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd);M=${1:-$ROOT/var/m25-material};export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
test -f "$M/signing-private.pem" || { echo 'FAIL: Node1 M25 signing private key missing';exit 2; }
python3 "$ROOT/scripts/m25/validate_m25_node.py" --material "$M" --repo-root "$ROOT"
TMP=$(mktemp -d);trap 'rm -rf "$TMP"' EXIT;cp -a "$M/." "$TMP/";rm -f "$TMP"/*private*.pem "$TMP/signing-private.pem"
python3 "$ROOT/scripts/m25/validate_m25_node.py" --material "$TMP" --repo-root "$ROOT"
echo 'PASS: Node1 M25 authority and verifier-package isolation verified'
