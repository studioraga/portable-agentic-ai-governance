#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.."&&pwd)";M9="${1:?m9 material}";M10="${2:?m10 material}"
"$ROOT/scripts/m10/preflight_dependencies.sh"
python3 "$ROOT/scripts/m10/build_m10_material.py" --m9-material "$M9" --out "$M10"
"$ROOT/deploy/m10/deploy_node.sh" "$M10" "$M9/security-ops-manifest.json"
echo 'PASS: Node1 M10 one-shot deployment complete'
