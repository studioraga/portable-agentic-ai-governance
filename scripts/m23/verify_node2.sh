#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)";M="${1:-$HOME/.config/portable-ai-governance/m23}";export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
if find "$M" -maxdepth 1 -type f -iname '*private*.pem' | grep -q .;then echo 'FAIL: Node2 must not receive M23 private keys';exit 2;fi
python3 "$ROOT/scripts/m23/validate_m23_node.py" --material "$M" --repo-root "$ROOT"
echo 'PASS: Node2 M23 verifier-only identity/MFA/PAM evidence verified'
