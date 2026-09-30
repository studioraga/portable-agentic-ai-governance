#!/usr/bin/env bash
set -euo pipefail
SRC="${1:?usage: $0 <m13-material-dir> <output.tar.gz>}";OUT="${2:?usage: $0 <m13-material-dir> <output.tar.gz>}";TMP="$(mktemp -d)";trap 'rm -rf "$TMP"' EXIT
FILES=(incident-classification-policy.json m13-control-mapping.json incident-assessments.json cra-cases.json deadline-states.json awareness-journal.json m13-clock-manifest.json m13-clock-manifest.json.sig signing-public.pem)
mkdir -p "$(dirname "$OUT")";mkdir -m700 "$TMP/m13-material"
for f in "${FILES[@]}";do test -f "$SRC/$f"||{ echo "FAIL missing $f";exit 2;};install -m600 "$SRC/$f" "$TMP/m13-material/$f";done
if find "$TMP" -type f \( -name '*private*.pem' -o -name 'signing-private.pem' \) -print|grep -q .;then echo 'FAIL: private key detected in M13 verifier package' >&2;exit 2;fi
tar -C "$TMP" -czf "$OUT" m13-material
( cd "$(dirname "$OUT")";sha256sum "$(basename "$OUT")" > "$(basename "$OUT").sha256";sha256sum -c "$(basename "$OUT").sha256" )
echo "PASS: M13 verifier-only material packaged and checksum verified at $OUT"
