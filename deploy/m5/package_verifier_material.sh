#!/usr/bin/env bash
set -euo pipefail
umask 077
SRC="${1:?usage: package_verifier_material.sh <m5-material-dir> <out.tar.gz>}"; OUT="${2:?output required}"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
mkdir -m 700 "$TMP/m5-material"
cp -a "$SRC/." "$TMP/m5-material/"
rm -f "$TMP/m5-material/signing-private.pem"
find "$TMP/m5-material" -type d -exec chmod 700 {} +
find "$TMP/m5-material" -type f -exec chmod 600 {} +
tar -C "$TMP" -czf "$OUT" m5-material
( cd "$(dirname "$OUT")"; sha256sum "$(basename "$OUT")" > "$(basename "$OUT").sha256" )
echo "PASS: M5 verifier material packaged at $OUT"
