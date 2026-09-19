#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"; M7="${1:?m7 verifier material}"; M6MAN="${2:?m6 manifest}"
"$ROOT/scripts/m7/preflight_dependencies.sh"
[ ! -e "$M7/signing-private.pem" ] || { echo 'FAIL: verifier material contains signing-private.pem'; exit 2; }
"$ROOT/deploy/m7/deploy_node.sh" "$M7" "$M6MAN"
"$ROOT/scripts/m7/preflight_m7.sh" "$HOME/.config/portable-ai-governance/m7/m7.env"
echo 'PASS: Node2 M7 one-shot deployment complete'
