#!/usr/bin/env bash
set -euo pipefail
M=${1:?material dir};OUT=${2:?output tar};TMP=$(mktemp -d);trap 'rm -rf "$TMP"' EXIT;mkdir -p "$TMP/m28-material";for f in "$M"/*;do b=$(basename "$f");[[ "$b" == *private*.pem ]] && continue;cp "$f" "$TMP/m28-material/$b";done;if find "$TMP" -iname '*private*.pem'|grep -q .;then echo 'FAIL private key';exit 2;fi;tar -C "$TMP" -czf "$OUT" m28-material;sha256sum "$OUT" > "$OUT.sha256"
