#!/usr/bin/env bash
set -euo pipefail
SRC=${1:?source material};OUT=${2:?output tar.gz};TMP=$(mktemp -d);trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/m27-material"
cp -a "$SRC"/. "$TMP/m27-material/"
rm -f "$TMP/m27-material/signing-private.pem"
if find "$TMP" -iname '*private*.pem' | grep -q .; then echo 'FAIL: private key remains in verifier package' >&2; exit 2; fi
mkdir -p "$(dirname "$OUT")";tar -C "$TMP" -czf "$OUT" m27-material
sha256sum "$OUT" > "$OUT.sha256"
echo "PASS: verifier-only package $OUT"
