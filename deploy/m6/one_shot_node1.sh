#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"; M3="${1:?m3 material}"; M4="${2:?m4 material}"; M5="${3:?m5 material}"; M6="${4:?m6 output/material}"
"$ROOT/scripts/m6/preflight_dependencies.sh"
python3 "$ROOT/scripts/m6/build_m6_material.py" --m3-material "$M3" --m4-material "$M4" --m5-material "$M5" --out "$M6"
"$ROOT/deploy/m6/deploy_node.sh" "$M6" "$M5/compliance-risk-manifest.json"
"$ROOT/scripts/m6/preflight_m6.sh" "$HOME/.config/portable-ai-governance/m6/m6.env"
echo 'PASS: Node1 M6 one-shot deployment complete'
