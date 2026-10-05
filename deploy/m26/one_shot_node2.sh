#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd); ARCHIVE=${1:?usage: one_shot_node2.sh m26-verifier.tar.gz}; DEST=${2:-/tmp/m26-node1}
rm -rf "$DEST";mkdir -p "$DEST";tar -C "$DEST" -xzf "$ARCHIVE";"$ROOT/scripts/m26/verify_node2.sh" "$DEST/m26-material"
