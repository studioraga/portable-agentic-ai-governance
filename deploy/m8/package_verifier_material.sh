#!/usr/bin/env bash
set -euo pipefail
SRC="${1:?}";OUT="${2:?}";TMP="$(mktemp -d)";trap 'rm -rf "$TMP"' EXIT;mkdir -m700 "$TMP/m8-material";cp -a "$SRC/." "$TMP/m8-material/";rm -f "$TMP/m8-material/signing-private.pem" "$TMP/m8-material/approval-signing-private.pem";tar -C "$TMP" -czf "$OUT" m8-material;chmod 600 "$OUT";(cd "$(dirname "$OUT")"&&sha256sum "$(basename "$OUT")">"$(basename "$OUT").sha256");echo "PASS: M8 verifier material packaged at $OUT"
