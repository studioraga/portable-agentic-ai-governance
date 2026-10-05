#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"; M="${1:-$ROOT/var/m22-material}"
export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
test -f "$M/signing-private.pem" || { echo 'FAIL: Node1 M22 private signing key missing'; exit 2; }
python3 "$ROOT/scripts/m22/validate_m22_node.py" --material "$M" --repo-root "$ROOT"
T="$(mktemp -d)";trap 'rm -rf "$T"' EXIT
"$ROOT/deploy/m22/package_verifier_material.sh" "$M" "$T/m22-verifier.tar.gz"
if tar -tzf "$T/m22-verifier.tar.gz" | grep -Eqi 'private.*pem'; then echo 'FAIL: private key leaked';exit 2;fi
echo 'PASS: Node1 M22 authority and verifier-package isolation verified'
