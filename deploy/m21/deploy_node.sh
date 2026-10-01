#!/usr/bin/env bash
set -euo pipefail
ROLE="$1";SRC="$2";DEST="$3";ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
case "$DEST" in "$HOME/.config/portable-ai-governance/m21"|/tmp/m21-*) ;; *) echo 'FAIL: unsafe M21 destination'; exit 2;; esac
if [[ "$ROLE" == node2 ]] && find "$SRC" -maxdepth 1 -type f -iname '*private*.pem' | grep -q .; then echo 'FAIL: Node2 must not receive M21 private signing key'; exit 2; fi
rm -rf "$DEST";install -d -m700 "$DEST"
cp -a "$SRC"/. "$DEST"/
if [[ "$ROLE" == node2 ]]; then rm -f "$DEST/signing-private.pem"; fi
export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
python3 "$ROOT/scripts/m21/validate_m21_node.py" --material "$DEST" --repo-root "$ROOT"
echo "PASS: M21 $ROLE material deployed to $DEST"
