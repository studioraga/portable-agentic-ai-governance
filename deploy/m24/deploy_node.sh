#!/usr/bin/env bash
set -euo pipefail
ROLE=${1:?usage: deploy_node.sh node1|node2 [archive]};ROOT=$(cd "$(dirname "$0")/../.." && pwd)
case "$ROLE" in node1)exec "$ROOT/deploy/m24/one_shot_node1.sh";;node2)exec "$ROOT/deploy/m24/one_shot_node2.sh" "${2:?Node2 requires verifier archive}";;*)echo 'role must be node1 or node2';exit 2;;esac
