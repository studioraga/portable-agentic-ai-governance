#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)";M="${1:-$ROOT/var/m23-material}";export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
for f in signing-private.pem federation-private.pem pam-private.pem; do test -f "$M/$f" || { echo "FAIL: Node1 M23 authority key missing: $f";exit 2;};done
python3 "$ROOT/scripts/m23/validate_m23_node.py" --material "$M" --repo-root "$ROOT"
T="$(mktemp -d)";trap 'rm -rf "$T"' EXIT
"$ROOT/deploy/m23/package_verifier_material.sh" "$M" "$T/m23-verifier.tar.gz"
if tar -tzf "$T/m23-verifier.tar.gz" | grep -Eqi 'private.*pem';then echo 'FAIL: M23 private key leaked';exit 2;fi
echo 'PASS: Node1 M23 identity/PAM authority and verifier-package isolation verified'
