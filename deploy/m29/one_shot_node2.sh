#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd);ARCHIVE=${1:?m29-verifier.tar.gz};TMP=${2:-/tmp/m29-node1};rm -rf "$TMP";mkdir -p "$TMP";tar -C "$TMP" -xzf "$ARCHIVE";"$ROOT/scripts/m29/verify_node2.sh" "$TMP/m29-material"
