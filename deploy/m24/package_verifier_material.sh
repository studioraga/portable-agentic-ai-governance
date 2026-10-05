#!/usr/bin/env bash
set -euo pipefail
M=${1:?material dir};OUT=${2:?output tar.gz};TMP=$(mktemp -d);trap 'rm -rf "$TMP"' EXIT;mkdir -p "$TMP/m24-material"
for f in asset-security-policy.json asset-register.json data-lifecycle-policy.json dlp-policy.json cryptographic-lifecycle-policy.json m24-control-mapping.json m24-gap-closure.json m24-validation-summary.json m24-source-manifest.json m24-asset-data-manifest.json m24-asset-data-manifest.json.sig signing-public.pem positive-sanitization-record.json positive-export-decision.json;do cp "$M/$f" "$TMP/m24-material/$f";done
if find "$TMP" -type f -iname '*private*.pem' | grep -q .;then echo 'FAIL: private key in verifier package';exit 2;fi
tar -C "$TMP" -czf "$OUT" m24-material;sha256sum "$OUT" > "$OUT.sha256";echo "PASS: created $OUT"
