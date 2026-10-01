#!/usr/bin/env bash
set -euo pipefail
SRC="${1:?material}";OUT="${2:?archive}";D="$(dirname "$OUT")";B="$(basename "$OUT")";mkdir -p "$D";T="$(mktemp -d)";trap 'rm -rf "$T"' EXIT;mkdir -m700 "$T/m20-material"
for f in "$SRC"/*;do [[ -f "$f" ]]||continue;[[ "$(basename "$f")" == signing-private.pem ]]&&continue;install -m600 "$f" "$T/m20-material/$(basename "$f")";done
tar -C "$T" -czf "$OUT" m20-material;(cd "$D";sha256sum "$B">"$B.sha256";sha256sum -c "$B.sha256");tar -tzf "$OUT"|grep -q signing-private.pem&&{ echo 'FAIL: private M20 key leaked';exit 2;}||true;echo "PASS: M20 verifier-only material packaged at $OUT"
