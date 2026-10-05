#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd);ARCHIVE=${1:?m25-verifier.tar.gz};TMP=${2:-/tmp/m25-node1};rm -rf "$TMP";mkdir -p "$TMP";tar -C "$TMP" -xzf "$ARCHIVE";"$ROOT/scripts/m25/verify_node2.sh" "$TMP/m25-material"
