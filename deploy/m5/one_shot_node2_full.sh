#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"; M2="${1:?m2 material root}"; M3="${2:?m3 verifier material}"; M4="${3:?m4 verifier material}"; M5="${4:?m5 verifier material}"
"$ROOT/deploy/m4/one_shot_node2_full.sh" "$M2" "$M3" "$M4"
"$ROOT/deploy/m5/one_shot_node2.sh" "$M5" "$M4/ai-security-manifest.json"
"$ROOT/scripts/m5/validate_combined_node.sh" "$HOME/.config/portable-ai-governance/m2/production.env" "$HOME/.config/portable-ai-governance/m3/m3.env" "$HOME/.config/portable-ai-governance/m4/m4.env" "$HOME/.config/portable-ai-governance/m5/m5.env"
echo 'PASS: Node2 full M0-M5 one-shot deployment complete'
