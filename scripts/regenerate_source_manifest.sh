#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
TMP="$(mktemp)"; trap 'rm -f "$TMP"' EXIT
find . -type f \
  ! -path './.git/*' \
  ! -path './.venv/*' \
  ! -path './.pytest_cache/*' \
  ! -path '*/__pycache__/*' \
  ! -name '*.pyc' \
  ! -path './var/*' \
  ! -path './release/source-manifest.sha256' \
  -print0 | sort -z | xargs -0 sha256sum > "$TMP"
install -m 644 "$TMP" release/source-manifest.sha256
echo 'PASS: regenerated release/source-manifest.sha256'
