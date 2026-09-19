#!/usr/bin/env bash
set -euo pipefail
SRC="${1:?usage package_verifier_material.sh <m7-material-dir> <out.tar.gz>}"; OUT="${2:?output required}"; TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
mkdir -m 700 "$TMP/m7-material"; cp -a "$SRC/." "$TMP/m7-material/"; rm -f "$TMP/m7-material/signing-private.pem"; find "$TMP/m7-material" -type d -exec chmod 700 {} +; find "$TMP/m7-material" -type f -exec chmod 600 {} +
tar -C "$TMP" -czf "$OUT" m7-material; chmod 600 "$OUT"; (cd "$(dirname "$OUT")" && sha256sum "$(basename "$OUT")" > "$(basename "$OUT").sha256"); echo "PASS: M7 verifier material packaged at $OUT"
