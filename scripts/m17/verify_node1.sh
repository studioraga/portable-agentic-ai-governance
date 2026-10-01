#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)";SRC="${1:?material directory required}";export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
python3 "$ROOT/scripts/m17/validate_m17_node.py" --material "$SRC" --repo-root "$ROOT"
test -f "$SRC/signing-private.pem"
T="$(mktemp -d)";trap 'rm -rf "$T"' EXIT
"$ROOT/deploy/m17/package_verifier_material.sh" "$SRC" "$T/m17-verifier.tar.gz"
! tar -tzf "$T/m17-verifier.tar.gz" | grep -Eq '(^|/)(signing-private\.pem|[^/]*private[^/]*\.pem)$'
echo "PASS: Node1 M17 authority + verifier-package isolation verified"
