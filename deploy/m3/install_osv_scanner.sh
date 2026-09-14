#!/usr/bin/env bash
set -euo pipefail
umask 077

# Pin a known-good OSV-Scanner release. v2.5.0/v2.5.1 currently have a
# documented regression affecting some SPDX/Go scans, so M3 defaults to v2.4.0.
VERSION="${PAG_OSV_SCANNER_VERSION:-v2.4.0}"
DEST_DIR="${PAG_OSV_INSTALL_DIR:-$HOME/.local/bin}"
BASE_URL="https://github.com/google/osv-scanner/releases/download/${VERSION}"

case "$(uname -s):$(uname -m)" in
  Linux:x86_64) ASSET="osv-scanner_linux_amd64" ;;
  Linux:aarch64|Linux:arm64) ASSET="osv-scanner_linux_arm64" ;;
  *) echo "FAIL: unsupported platform for OSV-Scanner: $(uname -s) $(uname -m)"; exit 2 ;;
esac

mkdir -p "$DEST_DIR"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

fetch() {
  local url="$1" out="$2"
  if command -v curl >/dev/null 2>&1; then
    curl --fail --location --proto '=https' --tlsv1.2 --silent --show-error "$url" -o "$out"
  elif command -v wget >/dev/null 2>&1; then
    wget --https-only --quiet "$url" -O "$out"
  else
    echo 'FAIL: curl or wget is required to install OSV-Scanner'
    exit 2
  fi
}

fetch "$BASE_URL/$ASSET" "$TMP/$ASSET"
fetch "$BASE_URL/osv-scanner_SHA256SUMS" "$TMP/osv-scanner_SHA256SUMS"

expected="$(awk -v f="$ASSET" '$2==f || $2=="*"f {print $1; exit}' "$TMP/osv-scanner_SHA256SUMS")"
[ -n "$expected" ] || { echo "FAIL: checksum for $ASSET not found in official release checksum file"; exit 2; }
actual="$(sha256sum "$TMP/$ASSET" | awk '{print $1}')"
[ "$actual" = "$expected" ] || { echo "FAIL: OSV-Scanner checksum mismatch"; exit 2; }

install -m 0755 "$TMP/$ASSET" "$DEST_DIR/osv-scanner"

PATH="$DEST_DIR:$PATH" osv-scanner --version
printf 'PASS: installed OSV-Scanner %s at %s\n' "$VERSION" "$DEST_DIR/osv-scanner"
printf 'NOTE: add %s to PATH if it is not already present.\n' "$DEST_DIR"
