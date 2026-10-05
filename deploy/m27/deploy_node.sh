#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd);ROLE=${1:?usage: deploy_node.sh node1|node2};case "$ROLE" in node1) exec "$ROOT/deploy/m27/one_shot_node1.sh";; node2) shift; exec "$ROOT/deploy/m27/one_shot_node2.sh" "$@";; *) echo 'role must be node1 or node2' >&2; exit 2;; esac
