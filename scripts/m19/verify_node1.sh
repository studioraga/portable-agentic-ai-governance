#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)";M="${1:-$ROOT/var/m19-material}";export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
python3 "$ROOT/scripts/m19/validate_m19_node.py" --material "$M" --repo-root "$ROOT"
[[ -f "$M/signing-private.pem" ]] || { echo 'FAIL: Node1 authority material missing private signing key';exit 2;}
T="$(mktemp -d)";trap 'rm -rf "$T"' EXIT;"$ROOT/deploy/m19/package_verifier_material.sh" "$M" "$T/m19-verifier.tar.gz" >/dev/null
if tar -tzf "$T/m19-verifier.tar.gz"|grep -q 'signing-private.pem';then echo 'FAIL: verifier package leaked private key';exit 2;fi
echo 'PASS: Node1 M19 authority + verifier-package isolation verified'
