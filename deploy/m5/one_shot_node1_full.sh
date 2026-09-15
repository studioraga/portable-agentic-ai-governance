#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"; M2="${1:?m2 material root}"; M3="${2:?m3 material}"; M4="${3:?m4 material}"; M5="${4:-$ROOT/var/m5-material}"
"$ROOT/deploy/m4/one_shot_node1_full.sh" "$M2" "$M3" "$M4"
"$ROOT/deploy/m5/one_shot_node1.sh" "$M4" "$M5"
"$ROOT/scripts/m5/validate_combined_node.sh" "$HOME/.config/portable-ai-governance/m2/production.env" "$HOME/.config/portable-ai-governance/m3/m3.env" "$HOME/.config/portable-ai-governance/m4/m4.env" "$HOME/.config/portable-ai-governance/m5/m5.env"
echo 'PASS: Node1 full M0-M5 one-shot deployment complete'
