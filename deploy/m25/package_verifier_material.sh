#!/usr/bin/env bash
set -euo pipefail
M=${1:?material dir};OUT=${2:?output tar.gz};TMP=$(mktemp -d);trap 'rm -rf "$TMP"' EXIT;mkdir -p "$TMP/m25-material"
for f in network-zone-policy.json egress-policy.json network-detection-policy.json m25-control-mapping.json m25-gap-closure.json m25-validation-summary.json m25-source-manifest.json generated-nftables.conf positive-flow-decision.json negative-flow-decision.json negative-egress-decision.json m25-network-manifest.json m25-network-manifest.json.sig signing-public.pem;do cp "$M/$f" "$TMP/m25-material/$f";done
if find "$TMP" -type f -iname '*private*.pem' | grep -q .;then echo 'FAIL: private key in verifier package';exit 2;fi
tar -C "$TMP" -czf "$OUT" m25-material;sha256sum "$OUT" > "$OUT.sha256";echo "PASS: created $OUT"
