#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"; M="${1:-$HOME/.config/portable-ai-governance/m22}"
export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
if find "$M" -maxdepth 1 -type f -iname '*private*.pem' | grep -q .; then echo 'FAIL: Node2 must not receive M22 private signing key';exit 2;fi
python3 "$ROOT/scripts/m22/validate_m22_node.py" --material "$M" --repo-root "$ROOT"
echo 'PASS: Node2 M22 verifier-only enterprise-control material verified'
