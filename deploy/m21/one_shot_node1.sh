#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)";N2="$1";OUT="${2:-$ROOT/var/m21-material}";TMP="$(mktemp -d)";trap 'rm -rf "$TMP"' EXIT
export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
python3 "$ROOT/scripts/m21/collect_platform_profile.py" --role release_authority --out "$TMP/node1.json"
python3 "$ROOT/scripts/m21/build_m21_material.py" --node1-profile "$TMP/node1.json" --node2-profile "$N2" --out "$OUT"
"$ROOT/deploy/m21/deploy_node.sh" node1 "$OUT" "$HOME/.config/portable-ai-governance/m21"
echo 'PASS: Node1 M21 live platform-security authority complete'
