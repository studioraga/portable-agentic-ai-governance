#!/usr/bin/env bash
set -euo pipefail
SRC="${1:?material}";OUT="${2:?archive}";D="$(dirname "$OUT")";B="$(basename "$OUT")";mkdir -p "$D";T="$(mktemp -d)";trap 'rm -rf "$T"' EXIT
mkdir -m700 "$T/m19-material"
for f in "$SRC"/*;do [[ -f "$f" ]] || continue;[[ "$(basename "$f")" == 'signing-private.pem' ]] && continue;install -m600 "$f" "$T/m19-material/$(basename "$f")";done
tar -C "$T" -czf "$OUT" m19-material
( cd "$D";sha256sum "$B" > "$B.sha256";sha256sum -c "$B.sha256" )
if tar -tzf "$OUT" | grep -Eq '(^|/)(signing-private\.pem|[^/]*private[^/]*\.pem)$';then echo 'FAIL: private M19 key in verifier archive';exit 2;fi
echo "PASS: M19 verifier-only material packaged and checksum verified at $OUT"
