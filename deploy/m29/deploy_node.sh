#!/usr/bin/env bash
set -euo pipefail
ROLE=${1:?node1|node2};SRC=${2:?material};DST=${3:-$HOME/.config/portable-ai-governance/m29};mkdir -p "$DST";cp -a "$SRC"/. "$DST"/;if [ "$ROLE" = node2 ];then rm -f "$DST/signing-private.pem";fi;echo "PASS: deployed M29 material for $ROLE to $DST"
