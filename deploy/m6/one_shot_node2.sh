#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"; M6="${1:?m6 verifier material}"; M5MAN="${2:?m5 manifest}"
"$ROOT/scripts/m6/preflight_dependencies.sh"
[ ! -e "$M6/signing-private.pem" ] || { echo 'FAIL: verifier material contains signing-private.pem'; exit 2; }
"$ROOT/deploy/m6/deploy_node.sh" "$M6" "$M5MAN"
"$ROOT/scripts/m6/preflight_m6.sh" "$HOME/.config/portable-ai-governance/m6/m6.env"
echo 'PASS: Node2 M6 one-shot deployment complete'
