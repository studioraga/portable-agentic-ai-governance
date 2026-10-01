#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)";SRC="${1:-$HOME/.config/portable-ai-governance/m18}";export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
if find "$SRC" -maxdepth 1 -type f -iname '*private*' -print | grep -q .; then echo 'FAIL: Node2 M18 verifier install contains private signing material';exit 2;fi
python3 "$ROOT/scripts/m18/validate_m18_node.py" --material "$SRC" --repo-root "$ROOT"
echo 'PASS: Node2 M18 verifier-only material verified'
