#!/usr/bin/env bash
set -euo pipefail
SRC="$1";OUT="$2";ROOT="$(dirname "$OUT")";TMP="$(mktemp -d)";trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/m23-material"
for f in enterprise-identity-policy.json m23-control-mapping.json m23-gap-closure.json m23-validation-summary.json m23-source-manifest.json m23-identity-manifest.json m23-identity-manifest.json.sig federation-public.pem pam-public.pem signing-public.pem positive-federated-assertion.jwt positive-jit-grant.jwt positive-break-glass-grant.jwt;do cp "$SRC/$f" "$TMP/m23-material/$f";done
if find "$TMP" -type f -iname '*private*.pem' | grep -q .;then echo 'FAIL: private key in M23 verifier material';exit 2;fi
tar -C "$TMP" -czf "$OUT" m23-material
( cd "$ROOT" && sha256sum "$(basename "$OUT")" > "$(basename "$OUT").sha256" && sha256sum -c "$(basename "$OUT").sha256" )
echo "PASS: M23 verifier-only material packaged at $OUT"
