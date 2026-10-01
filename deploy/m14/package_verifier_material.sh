#!/usr/bin/env bash
set -euo pipefail
SRC="${1:?usage: $0 <m14-material-dir> <output.tar.gz>}";OUT="${2:?usage: $0 <m14-material-dir> <output.tar.gz>}";TMP="$(mktemp -d)";trap 'rm -rf "$TMP"' EXIT
FILES=(reporting-policy.json m14-control-mapping.json reporting-packs.json submission-readiness.json srp-field-checklist.json m14-reporting-manifest.json m14-reporting-manifest.json.sig signing-public.pem)
mkdir -p "$(dirname "$OUT")";mkdir -m700 "$TMP/m14-material"
for f in "${FILES[@]}";do test -f "$SRC/$f"||{ echo "FAIL missing $f";exit 2;};install -m600 "$SRC/$f" "$TMP/m14-material/$f";done
if find "$TMP" -type f \( -name '*private*.pem' -o -name 'signing-private.pem' \) -print|grep -q .;then echo 'FAIL: private key detected in M14 verifier package' >&2;exit 2;fi
tar -C "$TMP" -czf "$OUT" m14-material
( cd "$(dirname "$OUT")";sha256sum "$(basename "$OUT")" > "$(basename "$OUT").sha256";sha256sum -c "$(basename "$OUT").sha256" )
echo "PASS: M14 verifier-only material packaged and checksum verified at $OUT"
