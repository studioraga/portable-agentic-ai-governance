#!/usr/bin/env bash
set -euo pipefail
ROLE="${1:?role}";SRC="${2:?material directory required}";DST="${3:?destination required}"
mkdir -p "$DST";chmod 700 "$DST";rm -f "$DST"/*
for f in secure-update-policy.json m16-control-mapping.json lifecycle-registry.json update-catalog.json update-install-decisions.json eol-notifications.json security-update.bin security-update.json security-update.json.sig m16-lifecycle-manifest.json m16-lifecycle-manifest.json.sig signing-public.pem;do install -m600 "$SRC/$f" "$DST/$f";done
rm -f "$DST/signing-private.pem"
echo "PASS: M16 $ROLE material deployed to $DST"
