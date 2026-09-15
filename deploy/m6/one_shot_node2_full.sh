#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"; M2="${1:?m2 material}"; M3="${2:?m3 material}"; M4="${3:?m4 material}"; M5="${4:?m5 material}"; M6="${5:?m6 material}"
"$ROOT/deploy/m5/one_shot_node2_full.sh" "$M2" "$M3" "$M4" "$M5"
"$ROOT/deploy/m6/one_shot_node2.sh" "$M6" "$M5/compliance-risk-manifest.json"
"$ROOT/scripts/m6/validate_combined_node.sh" "$HOME/.config/portable-ai-governance/m2/production.env" "$HOME/.config/portable-ai-governance/m3/m3.env" "$HOME/.config/portable-ai-governance/m4/m4.env" "$HOME/.config/portable-ai-governance/m5/m5.env" "$HOME/.config/portable-ai-governance/m6/m6.env"
echo 'PASS: Node2 full M0-M6 one-shot deployment complete'
