#!/usr/bin/env bash
set -euo pipefail
SRC="$1";OUT="$2";ROOT="$(dirname "$OUT")";TMP="$(mktemp -d)";trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/m21-material"
for f in platform-security-policy.json m21-control-mapping.json threat-model.json key-management-policy.json measured-boot-policy.json pag-platform-demo.service apparmor-profile selinux-policy.te node1-platform-profile.json node2-platform-profile.json platform-validation-summary.json firmware.bin firmware-descriptor.json firmware-descriptor.json.sig rollback-positive.json rollback-negative.json dice-demo.json m21-platform-manifest.json m21-platform-manifest.json.sig signing-public.pem; do cp "$SRC/$f" "$TMP/m21-material/$f"; done
if find "$TMP" -type f -iname '*private*.pem' | grep -q .; then echo 'FAIL: private key in verifier material'; exit 2; fi
tar -C "$TMP" -czf "$OUT" m21-material
( cd "$ROOT" && sha256sum "$(basename "$OUT")" > "$(basename "$OUT").sha256" )
( cd "$ROOT" && sha256sum -c "$(basename "$OUT").sha256" )
echo "PASS: M21 verifier-only material packaged at $OUT"
