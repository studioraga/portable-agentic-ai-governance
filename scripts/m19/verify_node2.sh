#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)";M="${1:-$HOME/.config/portable-ai-governance/m19}";export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
[[ ! -e "$M/signing-private.pem" ]] || { echo 'FAIL: Node2 contains M19 private signing key';exit 2;}
T="$(mktemp)";trap 'rm -f "$T"' EXIT
python3 "$ROOT/scripts/m19/collect_node_profile.py" --role node2 --out "$T"
python3 "$ROOT/scripts/m19/validate_m19_node.py" --material "$M" --repo-root "$ROOT" --current-node2-profile "$T"
echo 'PASS: Node2 M19 verifier-only production-validation material verified'
