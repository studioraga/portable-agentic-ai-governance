#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.."&&pwd)";MAT="${1:-$ROOT/var/m12-material}"
test -f "$MAT/signing-private.pem"||{ echo 'FAIL: Node1 M12 private signing key missing' >&2;exit 2;}
python3 "$ROOT/scripts/m12/validate_m12_node.py" --material "$MAT" --repo-root "$ROOT"
TMP="$(mktemp -d)";trap 'rm -rf "$TMP"' EXIT
"$ROOT/deploy/m12/package_verifier_material.sh" "$MAT" "$TMP/m12-verifier.tar.gz"
if tar -tzf "$TMP/m12-verifier.tar.gz"|grep -Eq '(^|/)(signing-private\.pem|[^/]*private[^/]*\.pem)$';then echo 'FAIL: private material leaked into M12 verifier package' >&2;exit 2;fi
echo 'PASS: Node1 M12 authority + verifier-package isolation verified'
