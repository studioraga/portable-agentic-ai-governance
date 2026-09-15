#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"; M2="${1:?m2 material root}"; M3="${2:?m3 verifier material}"; M4="${3:?m4 verifier material}"
"$ROOT/deploy/m3/one_shot_node2_full.sh" "$M2" "$M3"
"$ROOT/deploy/m4/one_shot_node2.sh" "$M4" "$M3/artifact-locks.json"
"$ROOT/scripts/m4/validate_combined_node.sh" "$HOME/.config/portable-ai-governance/m2/production.env" "$HOME/.config/portable-ai-governance/m3/m3.env" "$HOME/.config/portable-ai-governance/m4/m4.env"
echo 'PASS: Node2 full M0-M4 one-shot deployment complete'
