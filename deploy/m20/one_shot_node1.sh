#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)";M19="${1:?M19 production-validation-summary.json}";OUT="${2:-$ROOT/var/m20-material}";export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}";python3 "$ROOT/scripts/m20/build_m20_material.py" --m19-summary "$M19" --out "$OUT";python3 "$ROOT/scripts/m20/validate_m20_node.py" --material "$OUT" --repo-root "$ROOT";"$ROOT/deploy/m20/deploy_node.sh" "$OUT" "$HOME/.config/portable-ai-governance/m20";echo 'PASS: Node1 M20 enterprise release authority complete'
