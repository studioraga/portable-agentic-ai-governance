#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd);M=${1:-$ROOT/var/m28-material};test -f "$M/signing-private.pem";PYTHONPATH="$ROOT/src" python3 "$ROOT/scripts/m28/validate_m28_node.py" --material "$M" --repo-root "$ROOT";echo 'PASS: Node1 M28 authority and verifier-package isolation verified'
