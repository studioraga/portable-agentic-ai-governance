#!/usr/bin/env bash
set -euo pipefail
ROLE="${1:?role}";SRC="${2:?material directory required}";DST="${3:?destination required}"
mkdir -p "$DST";chmod 700 "$DST";rm -f "$DST"/*
for f in psirt-cvd-policy.json m15-control-mapping.json psirt-cases.json maintainer-coordination.json vulnerability-advisories.json user-notifications.json public-contact-cvd-contract.json m15-psirt-manifest.json m15-psirt-manifest.json.sig signing-public.pem;do install -m600 "$SRC/$f" "$DST/$f";done
rm -f "$DST/signing-private.pem"
echo "PASS: M15 $ROLE material deployed to $DST"
