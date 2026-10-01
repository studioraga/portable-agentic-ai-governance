#!/usr/bin/env bash
set -euo pipefail
SRC="${1:?usage: $0 <m16-material-dir> <output.tar.gz>}";OUT="${2:?usage: $0 <m16-material-dir> <output.tar.gz>}";TMP="$(mktemp -d)";trap 'rm -rf "$TMP"' EXIT
FILES=(secure-update-policy.json m16-control-mapping.json lifecycle-registry.json update-catalog.json update-install-decisions.json eol-notifications.json security-update.bin security-update.json security-update.json.sig m16-lifecycle-manifest.json m16-lifecycle-manifest.json.sig signing-public.pem)
mkdir -p "$(dirname "$OUT")";mkdir -m700 "$TMP/m16-material"
for f in "${FILES[@]}";do test -f "$SRC/$f"||{ echo "FAIL missing $f";exit 2;};install -m600 "$SRC/$f" "$TMP/m16-material/$f";done
if find "$TMP" -type f \( -name '*private*.pem' -o -name 'signing-private.pem' \) -print|grep -q .;then echo 'FAIL: private key detected in M16 verifier package' >&2;exit 2;fi
tar -C "$TMP" -czf "$OUT" m16-material
( cd "$(dirname "$OUT")";sha256sum "$(basename "$OUT")" > "$(basename "$OUT").sha256";sha256sum -c "$(basename "$OUT").sha256" )
echo "PASS: M16 verifier-only material packaged and checksum verified at $OUT"
