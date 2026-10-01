#!/usr/bin/env bash
set -euo pipefail
ROLE="${1:?role}";SRC="${2:?source}";DST="${3:?destination}"
if [[ "$ROLE" == node2 && -e "$SRC/signing-private.pem" ]];then echo 'FAIL: Node2 must not receive M19 private signing key';exit 2;fi
mkdir -p "$DST";chmod 700 "$DST";find "$DST" -mindepth 1 -maxdepth 1 -type f -delete
for f in "$SRC"/*;do [[ -f "$f" ]] || continue;[[ "$(basename "$f")" == 'signing-private.pem' ]] && continue;install -m600 "$f" "$DST/$(basename "$f")";done
echo "PASS: M19 $ROLE verifier material deployed to $DST"
