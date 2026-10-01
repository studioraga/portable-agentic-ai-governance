#!/usr/bin/env bash
set -euo pipefail
ROLE="${1:?role}";SRC="${2:?material directory required}";DST="${3:?destination required}"
mkdir -p "$DST";chmod 700 "$DST"
rm -f "$DST"/*
for f in reporting-policy.json m14-control-mapping.json reporting-packs.json submission-readiness.json srp-field-checklist.json m14-reporting-manifest.json m14-reporting-manifest.json.sig signing-public.pem;do install -m600 "$SRC/$f" "$DST/$f";done
rm -f "$DST/signing-private.pem"
echo "PASS: M14 $ROLE material deployed to $DST"
