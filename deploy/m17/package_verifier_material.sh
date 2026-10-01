#!/usr/bin/env bash
set -euo pipefail
SRC="${1:?material directory required}";OUT="${2:?output tar.gz required}";mkdir -p "$(dirname "$OUT")"
if find "$SRC" -maxdepth 1 -type f -iname '*private*' -print | grep -q .; then :; fi
T="$(mktemp -d)";trap 'rm -rf "$T"' EXIT;mkdir -m700 "$T/m17-material"
for f in annex-i-evidence-policy.json m17-control-mapping.json annex-i-evidence-map.json annex-i-evidence-index.json annex-i-coverage-summary.json annex-i-evidence-gaps.json m17-annex-i-manifest.json m17-annex-i-manifest.json.sig signing-public.pem;do install -m600 "$SRC/$f" "$T/m17-material/$f";done
tar -czf "$OUT" -C "$T" m17-material;(cd "$(dirname "$OUT")";sha256sum "$(basename "$OUT")" > "$(basename "$OUT").sha256";sha256sum -c "$(basename "$OUT").sha256")
echo "PASS: M17 verifier-only material packaged and checksum verified at $OUT"
