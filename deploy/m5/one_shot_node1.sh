#!/usr/bin/env bash
set -euo pipefail
umask 077
M4="${1:?usage: one_shot_node1.sh <m4-material-dir> <m5-material-dir>}"; M5="${2:?M5 material required}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
"$ROOT/scripts/m5/preflight_dependencies.sh"
python3 "$ROOT/scripts/m5/build_m5_material.py" --m4-material "$M4" --out "$M5"
"$ROOT/deploy/m5/deploy_node.sh" "$M5" "$M4/ai-security-manifest.json"
"$ROOT/scripts/m5/preflight_m5.sh" "$HOME/.config/portable-ai-governance/m5/m5.env"
echo 'PASS: Node1 M5 one-shot deployment complete'
