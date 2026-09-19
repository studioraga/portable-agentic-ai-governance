#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.."&&pwd)";M10="${1:?m10 verifier material}";M9MAN="${2:?m9 manifest}"
"$ROOT/scripts/m10/preflight_dependencies.sh"
"$ROOT/deploy/m10/deploy_node.sh" "$M10" "$M9MAN"
echo 'PASS: Node2 M10 one-shot deployment complete'
