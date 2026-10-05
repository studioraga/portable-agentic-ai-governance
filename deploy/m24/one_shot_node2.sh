#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd);ARCHIVE=${1:?usage: one_shot_node2.sh verifier.tar.gz};WORK=${2:-$ROOT/var/m24-validation/node2};rm -rf "$WORK";mkdir -p "$WORK";tar -C "$WORK" -xzf "$ARCHIVE";"$ROOT/scripts/m24/verify_node2.sh" "$WORK/m24-material"
