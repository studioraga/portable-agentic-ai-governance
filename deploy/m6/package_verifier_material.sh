#!/usr/bin/env bash
set -euo pipefail
SRC="${1:?usage package_verifier_material.sh <m6-material-dir> <out.tar.gz>}"; OUT="${2:?output required}"; TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
mkdir -m 700 "$TMP/m6-material"; cp -a "$SRC/." "$TMP/m6-material/"; rm -f "$TMP/m6-material/signing-private.pem"; tar -C "$TMP" -czf "$OUT" m6-material; chmod 600 "$OUT"; (cd "$(dirname "$OUT")" && sha256sum "$(basename "$OUT")" > "$(basename "$OUT").sha256"); echo "PASS: M6 verifier material packaged at $OUT"
