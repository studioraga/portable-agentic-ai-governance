#!/usr/bin/env bash
set -euo pipefail
SRC=${1:?material};OUT=${2:?tar};TMP=$(mktemp -d);trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/m29-material";cp -a "$SRC"/. "$TMP/m29-material"/;rm -f "$TMP/m29-material/signing-private.pem"
if find "$TMP" -type f -iname '*private*.pem' | grep -q .; then echo 'FAIL: private key in M29 verifier package';exit 2;fi
tar -C "$TMP" -czf "$OUT" m29-material;sha256sum "$OUT" > "$OUT.sha256";echo "PASS: verifier package $OUT"
