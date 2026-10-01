#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)";M="${1:-$HOME/.config/portable-ai-governance/m21}";export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
if find "$M" -maxdepth 1 -type f -iname '*private*.pem' | grep -q .; then echo 'FAIL: Node2 must not receive M21 private signing key'; exit 2; fi
python3 "$ROOT/scripts/m21/validate_m21_node.py" --material "$M" --repo-root "$ROOT"
echo 'PASS: Node2 M21 verifier-only platform-security material verified'
