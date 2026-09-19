#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)";M7="${1:?}";M8="${2:?}";"$ROOT/scripts/m8/preflight_dependencies.sh";python3 "$ROOT/scripts/m8/build_m8_material.py" --m7-material "$M7" --out "$M8";"$ROOT/deploy/m8/deploy_node.sh" "$M8" "$M7/tool-agent-manifest.json";"$ROOT/scripts/m8/preflight_m8.sh" "$HOME/.config/portable-ai-governance/m8/m8.env";echo 'PASS: Node1 M8 one-shot deployment complete'
