#!/usr/bin/env bash
set -euo pipefail
umask 077
SRC="${1:?material dir}"; OUT="${2:?output tar.gz}"; TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
mkdir -m 700 "$TMP/m4-material"; cp -a "$SRC/." "$TMP/m4-material/"; rm -f "$TMP/m4-material/signing-private.pem"
find "$TMP/m4-material" -type d -exec chmod 700 {} +; find "$TMP/m4-material" -type f -exec chmod 600 {} +
tar -C "$TMP" -czf "$OUT" m4-material
( cd "$(dirname "$OUT")"; sha256sum "$(basename "$OUT")" > "$(basename "$OUT").sha256" )
echo "PASS: M4 verifier bundle created at $OUT"
