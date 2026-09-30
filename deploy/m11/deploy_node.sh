#!/usr/bin/env bash
set -euo pipefail
umask 077
SRC="${1:?m11 material}";DEST="${2:-$HOME/.config/portable-ai-governance/m11}";ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.."&&pwd)"
case "$DEST" in ""|/|"$HOME"|"$HOME/.config"|"$HOME/.config/portable-ai-governance") echo "FAIL: unsafe M11 destination: $DEST" >&2;exit 2;;esac
for f in cra-requirements.json node-role-profile.json cra-coverage-report.json m11-cra-manifest.json m11-cra-manifest.json.sig signing-public.pem;do test -f "$SRC/$f"||{ echo "FAIL missing $f";exit 2;};done
install -d -m700 "$DEST";rm -f "$DEST/signing-private.pem"
for f in cra-requirements.json node-role-profile.json cra-coverage-report.json m11-cra-manifest.json m11-cra-manifest.json.sig signing-public.pem;do install -m600 "$SRC/$f" "$DEST/$f";done
python3 "$ROOT/scripts/m11/validate_m11_node.py" --material "$DEST" --repo-root "$ROOT"
echo "PASS: M11 verifier-only CRA foundation deployed to $DEST"
