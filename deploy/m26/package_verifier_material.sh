#!/usr/bin/env bash
set -euo pipefail
MAT=${1:?material dir}; OUT=${2:?output tar.gz}; TMP=$(mktemp -d);trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/m26-material";cp -a "$MAT/." "$TMP/m26-material/";rm -f "$TMP/m26-material/signing-private.pem"
if find "$TMP" -type f -iname '*private*.pem' | grep -q .; then echo 'FAIL: private key in verifier package';exit 1;fi
tar -C "$TMP" -czf "$OUT" m26-material;sha256sum "$OUT" > "$OUT.sha256";echo "Wrote $OUT and $OUT.sha256"
