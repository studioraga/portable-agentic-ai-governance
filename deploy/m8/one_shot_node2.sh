#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)";M8="${1:?}";M7MAN="${2:?}";"$ROOT/scripts/m8/preflight_dependencies.sh";[ ! -e "$M8/signing-private.pem" ] || { echo 'FAIL: verifier contains release signing private key';exit 2; }; [ ! -e "$M8/approval-signing-private.pem" ] || { echo 'FAIL: verifier contains approval signing private key';exit 2; };"$ROOT/deploy/m8/deploy_node.sh" "$M8" "$M7MAN";"$ROOT/scripts/m8/preflight_m8.sh" "$HOME/.config/portable-ai-governance/m8/m8.env";echo 'PASS: Node2 M8 one-shot deployment complete'
