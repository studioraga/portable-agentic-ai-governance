#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
MATERIAL="${1:?usage: one_shot_node2.sh MATERIAL_ROOT [CONFIG_ROOT]}"
CONFIG="${2:-$HOME/.config/portable-ai-governance/m2}"
cd "$ROOT"
PAG_SECURITY_PROFILE=lab ./deploy/deploy_node1.sh
./deploy/m2/deploy_node2.sh "$MATERIAL" "$CONFIG"
./scripts/m2/validate_m2_node.sh "$CONFIG/production.env"
echo 'PASS: Node2 M2 one-shot deployment complete'
