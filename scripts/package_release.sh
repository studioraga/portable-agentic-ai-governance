#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
VERSION="${1:-0.4.0}"
OUT="${2:-$ROOT/../portable-agentic-ai-governance-m0-m4-v${VERSION}.tar.gz}"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/portable-agentic-ai-governance"
tar --exclude='./.git' --exclude='./.git/*' --exclude='./.venv' --exclude='./.venv/*' --exclude='./.pytest_cache' --exclude='./.pytest_cache/*' --exclude='*/__pycache__' --exclude='*/__pycache__/*' --exclude='*.pyc' --exclude='./var/*' -cf - . | tar -C "$TMP/portable-agentic-ai-governance" -xf -
mkdir -p "$TMP/portable-agentic-ai-governance/var/evidence" "$TMP/portable-agentic-ai-governance/var/runs" "$TMP/portable-agentic-ai-governance/var/state"
(
 cd "$TMP/portable-agentic-ai-governance"
 find . -type f ! -path './release/source-manifest.sha256' -print0 | sort -z | xargs -0 sha256sum > release/source-manifest.sha256
)
tar -C "$TMP" -czf "$OUT" portable-agentic-ai-governance
( cd "$(dirname "$OUT")"; sha256sum "$(basename "$OUT")" > "$(basename "$OUT").sha256" )
printf 'Created %s\nCreated %s.sha256\n' "$OUT" "$OUT"
