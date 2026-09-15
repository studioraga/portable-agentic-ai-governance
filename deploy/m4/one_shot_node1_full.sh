#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"; M2="${1:?m2 material root}"; M3="${2:?m3 material}"; M4="${3:-$ROOT/var/m4-material}"
"$ROOT/deploy/m3/one_shot_node1_full.sh" "$M2" "$M3"
"$ROOT/deploy/m4/one_shot_node1.sh" "$M3" "$M4"
echo 'PASS: Node1 full M0-M4 one-shot deployment complete'
