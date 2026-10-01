#!/usr/bin/env bash
set -euo pipefail
SRC="${1:?source}";DST="${2:?destination}";mkdir -p "$DST";chmod 700 "$DST";cp -f "$SRC"/* "$DST"/;chmod 600 "$DST"/*;echo "PASS: M20 material deployed to $DST"
