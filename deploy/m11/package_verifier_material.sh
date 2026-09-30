#!/usr/bin/env bash
set -euo pipefail

SRC="${1:?usage: $0 <m11-material-dir> <output.tar.gz>}"
OUT="${2:?usage: $0 <m11-material-dir> <output.tar.gz>}"

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

mkdir -p "$(dirname "$OUT")"
mkdir -m 700 "$TMP/m11-material"

FILES=(
    cra-requirements.json
    node-role-profile.json
    cra-coverage-report.json
    m11-cra-manifest.json
    m11-cra-manifest.json.sig
    signing-public.pem
)

echo "=== M11 verifier-package build ==="
echo "source : $SRC"
echo "output : $OUT"

for f in "${FILES[@]}"; do
    if [[ ! -f "$SRC/$f" ]]; then
        echo "FAIL: missing required verifier material: $SRC/$f" >&2
        exit 2
    fi

    install -m 600 \
        "$SRC/$f" \
        "$TMP/m11-material/$f"
done

# Defense in depth: the verifier package must never contain private key material.
if find "$TMP" -type f \
    \( -name '*private*.pem' -o -name 'signing-private.pem' \) \
    -print | grep -q .; then

    echo "FAIL: private key detected in verifier package" >&2
    exit 2
fi

tar \
    -C "$TMP" \
    -czf "$OUT" \
    m11-material

OUT_DIR="$(cd "$(dirname "$OUT")" && pwd)"
OUT_NAME="$(basename "$OUT")"
SHA_NAME="${OUT_NAME}.sha256"

(
    cd "$OUT_DIR"

    sha256sum "$OUT_NAME" > "$SHA_NAME"

    # Verify from the same directory because the checksum intentionally
    # contains only the portable basename.
    sha256sum -c "$SHA_NAME"
)

echo
echo "PASS: M11 verifier-only material packaged and checksum verified"
echo "archive : $OUT"
echo "sha256  : ${OUT}.sha256"
