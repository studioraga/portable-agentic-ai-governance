#!/usr/bin/env bash
set -euo pipefail
umask 077
M5="${1:?usage: one_shot_node2.sh <m5-verifier-dir> <m4-manifest>}"; M4MAN="${2:?M4 manifest required}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
[ ! -f "$M5/signing-private.pem" ] || { echo 'FAIL: verifier material contains signing-private.pem'; exit 2; }
"$ROOT/scripts/m5/preflight_dependencies.sh"
"$ROOT/deploy/m5/deploy_node.sh" "$M5" "$M4MAN"
"$ROOT/scripts/m5/preflight_m5.sh" "$HOME/.config/portable-ai-governance/m5/m5.env"
echo 'PASS: Node2 M5 one-shot deployment complete'
