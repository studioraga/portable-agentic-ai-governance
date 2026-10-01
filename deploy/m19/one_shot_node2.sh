#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)";SRC="${1:?verifier material}";DST="${2:-$HOME/.config/portable-ai-governance/m19}";export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
if [[ -e "$SRC/signing-private.pem" ]];then echo 'FAIL: Node2 must not receive M19 private signing key';exit 2;fi
T="$(mktemp)";trap 'rm -f "$T"' EXIT
python3 "$ROOT/scripts/m19/collect_node_profile.py" --role node2 --out "$T"
python3 "$ROOT/scripts/m19/validate_m19_node.py" --material "$SRC" --repo-root "$ROOT" --current-node2-profile "$T"
"$ROOT/deploy/m19/deploy_node.sh" node2 "$SRC" "$DST"
echo 'PASS: Node2 M19 independent production-validation verifier complete'
