#!/usr/bin/env bash
set -euo pipefail
umask 077
SRC="${1:?usage: package_verifier_material.sh <material-dir> [output.tar.gz]}"; OUT="${2:-m3-verifier-material.tar.gz}"
[ -d "$SRC" ] || { echo "FAIL missing material dir"; exit 2; }
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
mkdir "$TMP/m3-material"; cp -a "$SRC/." "$TMP/m3-material/"; rm -f "$TMP/m3-material/signing-private.pem"
tar -C "$TMP" -czf "$OUT" m3-material
( cd "$(dirname "$OUT")"; sha256sum "$(basename "$OUT")" > "$(basename "$OUT").sha256" )
echo "PASS: verifier-only M3 material packaged: $OUT"
