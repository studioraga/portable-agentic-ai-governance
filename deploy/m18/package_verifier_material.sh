#!/usr/bin/env bash
set -euo pipefail
SRC="${1:?material directory required}";OUT="${2:?output tar.gz required}";mkdir -p "$(dirname "$OUT")"
T="$(mktemp -d)";trap 'rm -rf "$T"' EXIT;mkdir -m700 "$T/m18-material"
for f in technical-file-policy.json m18-control-mapping.json annex-vii-map.json product-technical-profile.json annex-vii-technical-file-index.json annex-vii-readiness-summary.json annex-vii-gap-register.json technical-file-cover.json m18-technical-file-manifest.json m18-technical-file-manifest.json.sig signing-public.pem;do install -m600 "$SRC/$f" "$T/m18-material/$f";done
tar -czf "$OUT" -C "$T" m18-material
(cd "$(dirname "$OUT")";sha256sum "$(basename "$OUT")" > "$(basename "$OUT").sha256";sha256sum -c "$(basename "$OUT").sha256")
echo "PASS: M18 verifier-only material packaged and checksum verified at $OUT"
