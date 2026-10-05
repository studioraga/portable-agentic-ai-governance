#!/usr/bin/env bash
set -euo pipefail
SRC="$1";OUT="$2";ROOT="$(dirname "$OUT")";TMP="$(mktemp -d)";trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/m22-material"
for f in cissp-domain-catalog.json enterprise-security-requirements.json enterprise-control-mapping.json gap-register.json evidence-policy.json m22-evaluation-summary.json m22-source-manifest.json m22-enterprise-manifest.json m22-enterprise-manifest.json.sig signing-public.pem; do cp "$SRC/$f" "$TMP/m22-material/$f";done
if find "$TMP" -type f -iname '*private*.pem' | grep -q .; then echo 'FAIL: private key in verifier material';exit 2;fi
tar -C "$TMP" -czf "$OUT" m22-material
( cd "$ROOT" && sha256sum "$(basename "$OUT")" > "$(basename "$OUT").sha256" && sha256sum -c "$(basename "$OUT").sha256" )
echo "PASS: M22 verifier-only material packaged at $OUT"
