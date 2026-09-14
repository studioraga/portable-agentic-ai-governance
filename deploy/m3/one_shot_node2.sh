#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"; MAT="${1:?usage one_shot_node2.sh <transferred-m3-material>}"
if [ -e "$MAT/signing-private.pem" ]; then echo 'FAIL: private supply-chain signing key must not be transferred to Node2'; exit 2; fi
"$ROOT/deploy/m3/deploy_node.sh" "$MAT" "${PAG_M3_CONFIG_DIR:-$HOME/.config/portable-ai-governance/m3}"
"$ROOT/scripts/m3/preflight_m3.sh" "${PAG_M3_CONFIG_DIR:-$HOME/.config/portable-ai-governance/m3}/m3.env"
echo 'PASS: Node2 M3 one-shot deployment complete'
