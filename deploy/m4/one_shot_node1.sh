#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"; M3MAT="${1:?usage one_shot_node1.sh <m3-material> [m4-material]}"; M4MAT="${2:-$ROOT/var/m4-material}"
python3 "$ROOT/scripts/m4/build_m4_material.py" --m3-material "$M3MAT" --out "$M4MAT"
"$ROOT/deploy/m4/deploy_node.sh" "$M4MAT" "$M3MAT/artifact-locks.json"
"$ROOT/scripts/m4/preflight_m4.sh" "$HOME/.config/portable-ai-governance/m4/m4.env"
python3 "$ROOT/scripts/m4/validate_m4_node.py" "$HOME/.config/portable-ai-governance/m4/m4.env"
if [ -f "$HOME/.config/portable-ai-governance/m2/production.env" ] && [ -f "$HOME/.config/portable-ai-governance/m3/m3.env" ]; then "$ROOT/scripts/m4/validate_combined_node.sh" "$HOME/.config/portable-ai-governance/m2/production.env" "$HOME/.config/portable-ai-governance/m3/m3.env" "$HOME/.config/portable-ai-governance/m4/m4.env"; fi
echo 'PASS: Node1 M4 one-shot deployment complete'
