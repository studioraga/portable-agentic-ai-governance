#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.."&&pwd)";M8="${1:?m8 material}";M9="${2:?m9 material}"
"$ROOT/scripts/m9/preflight_dependencies.sh";python3 "$ROOT/scripts/m9/build_m9_material.py" --m8-material "$M8" --out "$M9";"$ROOT/deploy/m9/deploy_node.sh" "$M9" "$M8/action-agent-manifest.json";echo 'PASS: Node1 M9 one-shot deployment complete'
