#!/usr/bin/env bash
set -euo pipefail
SRC="${1:?usage: $0 <m15-material-dir> <output.tar.gz>}";OUT="${2:?usage: $0 <m15-material-dir> <output.tar.gz>}";TMP="$(mktemp -d)";trap 'rm -rf "$TMP"' EXIT
FILES=(psirt-cvd-policy.json m15-control-mapping.json psirt-cases.json maintainer-coordination.json vulnerability-advisories.json user-notifications.json public-contact-cvd-contract.json m15-psirt-manifest.json m15-psirt-manifest.json.sig signing-public.pem)
mkdir -p "$(dirname "$OUT")";mkdir -m700 "$TMP/m15-material"
for f in "${FILES[@]}";do test -f "$SRC/$f"||{ echo "FAIL missing $f";exit 2;};install -m600 "$SRC/$f" "$TMP/m15-material/$f";done
if find "$TMP" -type f \( -name '*private*.pem' -o -name 'signing-private.pem' \) -print|grep -q .;then echo 'FAIL: private key detected in M15 verifier package' >&2;exit 2;fi
tar -C "$TMP" -czf "$OUT" m15-material
( cd "$(dirname "$OUT")";sha256sum "$(basename "$OUT")" > "$(basename "$OUT").sha256";sha256sum -c "$(basename "$OUT").sha256" )
echo "PASS: M15 verifier-only material packaged and checksum verified at $OUT"
