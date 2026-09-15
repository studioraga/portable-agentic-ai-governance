#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"; MAT="${1:?m4 verifier material}"; M3LOCK="${2:?m3 artifact lock}"
[ ! -f "$MAT/signing-private.pem" ] || { echo 'FAIL: M4 private signing key present on verifier node'; exit 2; }
"$ROOT/deploy/m4/deploy_node.sh" "$MAT" "$M3LOCK"
"$ROOT/scripts/m4/preflight_m4.sh" "$HOME/.config/portable-ai-governance/m4/m4.env"
python3 "$ROOT/scripts/m4/validate_m4_node.py" "$HOME/.config/portable-ai-governance/m4/m4.env"
echo 'PASS: Node2 M4 one-shot deployment complete'
