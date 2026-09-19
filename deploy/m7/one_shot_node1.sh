#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"; M6="${1:?m6 material}"; M7="${2:?m7 output/material}"
"$ROOT/scripts/m7/preflight_dependencies.sh"
python3 "$ROOT/scripts/m7/build_m7_material.py" --m6-material "$M6" --out "$M7"
"$ROOT/deploy/m7/deploy_node.sh" "$M7" "$M6/evidence-analyst-manifest.json"
"$ROOT/scripts/m7/preflight_m7.sh" "$HOME/.config/portable-ai-governance/m7/m7.env"
echo 'PASS: Node1 M7 one-shot deployment complete'
