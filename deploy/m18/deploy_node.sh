#!/usr/bin/env bash
set -euo pipefail
ROLE="${1:?role}";SRC="${2:?material directory required}";DST="${3:?destination required}"
if [[ "$ROLE" == node2 ]] && find "$SRC" -maxdepth 1 -type f -iname '*private*' -print | grep -q .; then echo 'FAIL: Node2 must not receive M18 private signing key';exit 2;fi
mkdir -p "$DST";chmod 700 "$DST";rm -f "$DST"/*
for f in technical-file-policy.json m18-control-mapping.json annex-vii-map.json product-technical-profile.json annex-vii-technical-file-index.json annex-vii-readiness-summary.json annex-vii-gap-register.json technical-file-cover.json m18-technical-file-manifest.json m18-technical-file-manifest.json.sig signing-public.pem;do install -m600 "$SRC/$f" "$DST/$f";done
rm -f "$DST/signing-private.pem"
echo "PASS: M18 $ROLE material deployed to $DST"
