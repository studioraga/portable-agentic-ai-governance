#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"; M2="${1:?m2 material}"; M3="${2:?m3 material}"; M4="${3:?m4 material}"; M5="${4:?m5 material}"; M6="${5:?m6 material}"; M7="${6:?m7 material}"
python3 "$ROOT/scripts/m7/verify_release_chain.py" --m4-material "$M4" --m5-material "$M5" --m6-material "$M6" --m7-material "$M7"
"$ROOT/deploy/m6/one_shot_node2_full.sh" "$M2" "$M3" "$M4" "$M5" "$M6"
"$ROOT/deploy/m7/one_shot_node2.sh" "$M7" "$M6/evidence-analyst-manifest.json"
"$ROOT/scripts/m7/validate_combined_node.sh" "$HOME/.config/portable-ai-governance/m2/production.env" "$HOME/.config/portable-ai-governance/m3/m3.env" "$HOME/.config/portable-ai-governance/m4/m4.env" "$HOME/.config/portable-ai-governance/m5/m5.env" "$HOME/.config/portable-ai-governance/m6/m6.env" "$HOME/.config/portable-ai-governance/m7/m7.env"
echo 'PASS: Node2 full M0-M7 one-shot deployment complete'
