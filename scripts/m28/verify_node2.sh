#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd);M=${1:?material dir required};if find "$M" -maxdepth 1 -iname '*private*.pem' | grep -q .;then echo 'FAIL: private key in verifier material';exit 2;fi;PYTHONPATH="$ROOT/src" python3 "$ROOT/scripts/m28/validate_m28_node.py" --material "$M" --repo-root "$ROOT";echo 'PASS: Node2 M28 verifier-only organizational evidence verified'
