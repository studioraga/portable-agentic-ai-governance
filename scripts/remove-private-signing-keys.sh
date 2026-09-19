#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"

echo "=== Private supply-chain key cleanup ==="
echo "Root: $(realpath "$ROOT")"
echo

echo "Private signing keys found:"
find "$ROOT" -type f \
  \( -name 'signing-private.pem' \
     -o -name 'approval-signing-private.pem' \
     -o -name '*signing-private*.pem' \) \
  -print

echo
read -r -p "Delete all private signing keys listed above? [y/N] " answer

case "$answer" in
  y|Y|yes|YES)
    find "$ROOT" -type f \
      \( -name 'signing-private.pem' \
         -o -name 'approval-signing-private.pem' \
         -o -name '*signing-private*.pem' \) \
      -print -delete
    ;;
  *)
    echo "Aborted. Nothing deleted."
    exit 0
    ;;
esac

echo
echo "=== Verification: remaining PEM files ==="
find "$ROOT" -type f -name '*.pem' -print

echo
echo "=== Verification: private signing keys must be absent ==="

if find "$ROOT" -type f \
     \( -name 'signing-private.pem' \
        -o -name 'approval-signing-private.pem' \
        -o -name '*signing-private*.pem' \) \
     -print -quit | grep -q .; then
    echo "FAIL: private supply-chain signing key still exists"
    exit 1
else
    echo "PASS: no private supply-chain signing keys remain"
fi
