#!/usr/bin/env bash
set -euo pipefail
ROLE="${1:?role}";SRC="${2:?material directory required}";DST="${3:?destination required}"
if [[ "$ROLE" == node2 ]] && find "$SRC" -maxdepth 1 -type f -iname '*private*' -print | grep -q .; then echo 'FAIL: Node2 must not receive M17 private signing key'; exit 2; fi
mkdir -p "$DST";chmod 700 "$DST";rm -f "$DST"/*
for f in annex-i-evidence-policy.json m17-control-mapping.json annex-i-evidence-map.json annex-i-evidence-index.json annex-i-coverage-summary.json annex-i-evidence-gaps.json m17-annex-i-manifest.json m17-annex-i-manifest.json.sig signing-public.pem;do install -m600 "$SRC/$f" "$DST/$f";done
rm -f "$DST/signing-private.pem"
echo "PASS: M17 $ROLE material deployed to $DST"
