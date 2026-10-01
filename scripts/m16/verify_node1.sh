#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.."&&pwd)";SRC="${1:?M16 material required}";export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
python3 "$ROOT/scripts/m16/validate_m16_node.py" --material "$SRC" --repo-root "$ROOT"
test -f "$SRC/signing-private.pem" || { echo 'FAIL: Node1 M16 private signing key missing';exit 2;}
TMP="$(mktemp -d)";trap 'rm -rf "$TMP"' EXIT
"$ROOT/deploy/m16/package_verifier_material.sh" "$SRC" "$TMP/m16-verifier.tar.gz"
if tar -tzf "$TMP/m16-verifier.tar.gz"|grep -Eq 'signing-private.pem|private.*pem';then echo 'FAIL: private key leaked';exit 2;fi
echo 'PASS: Node1 M16 authority + verifier-package isolation verified'
