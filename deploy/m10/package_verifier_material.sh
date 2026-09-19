#!/usr/bin/env bash
set -euo pipefail
SRC="${1:?m10 material}";OUT="${2:?output tar.gz}";TMP="$(mktemp -d)";trap 'rm -rf "$TMP"' EXIT
mkdir -m700 "$TMP/m10-material"
for f in multi-agent-manifest.json multi-agent-manifest.json.sig signing-public.pem multi-agent-policy.json multi-agent-topology.json workflow-decision-public.pem;do test -f "$SRC/$f"||{ echo "FAIL missing $f";exit 2;};install -m600 "$SRC/$f" "$TMP/m10-material/$f";done
tar -C "$TMP" -czf "$OUT" m10-material
( cd "$(dirname "$OUT")";sha256sum "$(basename "$OUT")" > "$(basename "$OUT").sha256" )
echo "PASS: M10 verifier-only material packaged at $OUT"
