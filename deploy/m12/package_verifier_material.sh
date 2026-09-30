#!/usr/bin/env bash
set -euo pipefail
SRC="${1:?usage: $0 <m12-material-dir> <output.tar.gz>}";OUT="${2:?usage: $0 <m12-material-dir> <output.tar.gz>}";TMP="$(mktemp -d)";trap 'rm -rf "$TMP"' EXIT
FILES=(intelligence-source-policy.json m12-control-mapping.json product-inventory.json normalized-vulnerabilities.json exploitation-evidence.json aev-assessments.json m12-intel-manifest.json m12-intel-manifest.json.sig signing-public.pem)
mkdir -p "$(dirname "$OUT")";mkdir -m700 "$TMP/m12-material"
for f in "${FILES[@]}";do test -f "$SRC/$f"||{ echo "FAIL missing $f";exit 2;};install -m600 "$SRC/$f" "$TMP/m12-material/$f";done
if find "$TMP" -type f \( -name '*private*.pem' -o -name 'signing-private.pem' \) -print|grep -q .;then echo 'FAIL: private key detected in M12 verifier package' >&2;exit 2;fi
tar -C "$TMP" -czf "$OUT" m12-material
( cd "$(dirname "$OUT")";sha256sum "$(basename "$OUT")" > "$(basename "$OUT").sha256";sha256sum -c "$(basename "$OUT").sha256" )
echo "PASS: M12 verifier-only material packaged and checksum verified at $OUT"
