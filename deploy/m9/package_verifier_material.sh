#!/usr/bin/env bash
set -euo pipefail
SRC="${1:?m9 material}";OUT="${2:?output tar.gz}";TMP="$(mktemp -d)";trap 'rm -rf "$TMP"' EXIT
mkdir -m700 "$TMP/m9-material";for f in security-ops-manifest.json security-ops-manifest.json.sig signing-public.pem security-ops-policy.json recovery-signing-public.pem;do install -m600 "$SRC/$f" "$TMP/m9-material/$f";done
tar -C "$TMP" -czf "$OUT" m9-material;(cd "$(dirname "$OUT")"&&sha256sum "$(basename "$OUT")">"$(basename "$OUT").sha256");echo "PASS: M9 verifier material packaged at $OUT"
