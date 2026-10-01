#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)";M="${1:-$ROOT/var/m21-material}";export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
test -f "$M/signing-private.pem" || { echo 'FAIL: Node1 M21 private signing key missing'; exit 2; }
python3 "$ROOT/scripts/m21/validate_m21_node.py" --material "$M" --repo-root "$ROOT"
T="$(mktemp -d)";trap 'rm -rf "$T"' EXIT
"$ROOT/deploy/m21/package_verifier_material.sh" "$M" "$T/m21-verifier.tar.gz"
if tar -tzf "$T/m21-verifier.tar.gz" | grep -Eq 'private.*pem'; then echo 'FAIL: private key leaked'; exit 2; fi
echo 'PASS: Node1 M21 authority + verifier-package isolation verified'
