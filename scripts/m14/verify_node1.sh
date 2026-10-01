#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.."&&pwd)";MAT="${1:-$ROOT/var/m14-material}"
test -f "$MAT/signing-private.pem"||{ echo 'FAIL: Node1 M14 private signing key missing' >&2;exit 2;}
python3 "$ROOT/scripts/m14/validate_m14_node.py" --material "$MAT" --repo-root "$ROOT"
TMP="$(mktemp -d)";trap 'rm -rf "$TMP"' EXIT
"$ROOT/deploy/m14/package_verifier_material.sh" "$MAT" "$TMP/m14-verifier.tar.gz"
if tar -tzf "$TMP/m14-verifier.tar.gz"|grep -Eq '(^|/)(signing-private\.pem|[^/]*private[^/]*\.pem)$';then echo 'FAIL: private material leaked into M14 verifier package' >&2;exit 2;fi
echo 'PASS: Node1 M14 authority + verifier-package isolation verified'
