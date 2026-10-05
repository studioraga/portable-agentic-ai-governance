#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd);ARCHIVE=${1:?verifier tar required};DEST=${2:-/tmp/m28-node1};rm -rf "$DEST";mkdir -p "$DEST";tar -C "$DEST" -xzf "$ARCHIVE";"$ROOT/scripts/m28/verify_node2.sh" "$DEST/m28-material"
