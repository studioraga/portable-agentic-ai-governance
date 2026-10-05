#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
case "${1:-}" in node1) exec "$ROOT/deploy/m25/one_shot_node1.sh" "${2:-$ROOT/var/m25-material}";; node2) exec "$ROOT/deploy/m25/one_shot_node2.sh" "${2:?verifier archive required}";; *) echo 'usage: deploy_node.sh node1 [material-dir] | node2 <verifier.tar.gz>';exit 2;; esac
