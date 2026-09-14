#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
M2_MATERIAL="${1:?usage one_shot_node2_full.sh <m2-material-dir> <m3-verifier-material-dir>}"; M3_MATERIAL="${2:?}"
"$ROOT/deploy/m2/one_shot_node2.sh" "$M2_MATERIAL"
"$ROOT/deploy/m3/one_shot_node2.sh" "$M3_MATERIAL"
"$ROOT/scripts/m3/validate_combined_node.sh" "$HOME/.config/portable-ai-governance/m2/production.env" "$HOME/.config/portable-ai-governance/m3/m3.env"
echo 'PASS: Node2 full M0-M3 one-shot deployment complete'
