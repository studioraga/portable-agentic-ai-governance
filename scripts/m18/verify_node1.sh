#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)";SRC="${1:-$ROOT/var/m18-material}";export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
python3 "$ROOT/scripts/m18/validate_m18_node.py" --material "$SRC" --repo-root "$ROOT"
test -f "$SRC/signing-private.pem" || { echo 'FAIL: Node1 M18 authority missing private signing key'; exit 2; }
T="$(mktemp -d)";trap 'rm -rf "$T"' EXIT
"$ROOT/deploy/m18/package_verifier_material.sh" "$SRC" "$T/m18-verifier.tar.gz"
if tar -tzf "$T/m18-verifier.tar.gz" | grep -Eq '(^|/)(signing-private\.pem|[^/]*private[^/]*\.pem)$'; then echo 'FAIL: verifier archive leaked private key';exit 2;fi
echo 'PASS: Node1 M18 authority + verifier-package isolation verified'
