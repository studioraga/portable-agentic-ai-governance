#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.."&&pwd)";MAT="${1:-$ROOT/var/m13-material}"
test -f "$MAT/signing-private.pem"||{ echo 'FAIL: Node1 M13 private signing key missing' >&2;exit 2;}
python3 "$ROOT/scripts/m13/validate_m13_node.py" --material "$MAT" --repo-root "$ROOT"
TMP="$(mktemp -d)";trap 'rm -rf "$TMP"' EXIT
"$ROOT/deploy/m13/package_verifier_material.sh" "$MAT" "$TMP/m13-verifier.tar.gz"
if tar -tzf "$TMP/m13-verifier.tar.gz"|grep -Eq '(^|/)(signing-private\.pem|[^/]*private[^/]*\.pem)$';then echo 'FAIL: private material leaked into M13 verifier package' >&2;exit 2;fi
echo 'PASS: Node1 M13 authority + verifier-package isolation verified'
