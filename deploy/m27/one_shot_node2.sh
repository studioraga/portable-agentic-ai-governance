#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd);ARCHIVE=${1:?usage: one_shot_node2.sh m27-verifier.tar.gz};DEST=${2:-/tmp/m27-node1};rm -rf "$DEST";mkdir -p "$DEST";tar -C "$DEST" -xzf "$ARCHIVE";exec "$ROOT/scripts/m27/verify_node2.sh" "$DEST/m27-material"
