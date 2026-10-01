#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)";M="${1:-$ROOT/var/m20-material}";python3 "$ROOT/scripts/m20/validate_m20_node.py" --material "$M" --repo-root "$ROOT";[[ -f "$M/signing-private.pem" ]]||{ echo 'FAIL: Node1 missing M20 private key';exit 2;};T="$(mktemp -d)";trap 'rm -rf "$T"' EXIT;"$ROOT/deploy/m20/package_verifier_material.sh" "$M" "$T/v.tar.gz" >/dev/null;tar -tzf "$T/v.tar.gz"|grep -q signing-private.pem&&exit 2||true;echo 'PASS: Node1 M20 authority + verifier-package isolation verified'
