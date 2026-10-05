#!/usr/bin/env bash
set -euo pipefail
ROLE=${1:-};case "$ROLE" in node1) exec "$(dirname "$0")/one_shot_node1.sh";;node2) shift;exec "$(dirname "$0")/one_shot_node2.sh" "$@";;*) echo 'usage: deploy_node.sh node1|node2 [archive]';exit 2;;esac
