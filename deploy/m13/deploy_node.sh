#!/usr/bin/env bash
set -euo pipefail
umask 077
ROLE="${1:?role required}";SRC="${2:?m13 material directory required}";DEST="${3:-$HOME/.config/portable-ai-governance/m13}";ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.."&&pwd)"
[[ "$ROLE" == node1 || "$ROLE" == node2 ]]||{ echo 'FAIL: role must be node1 or node2' >&2;exit 2;}
case "$DEST" in ""|/|"$HOME"|"$HOME/.config"|"$HOME/.config/portable-ai-governance") echo "FAIL: unsafe M13 destination: $DEST" >&2;exit 2;;esac
FILES=(incident-classification-policy.json m13-control-mapping.json incident-assessments.json cra-cases.json deadline-states.json awareness-journal.json m13-clock-manifest.json m13-clock-manifest.json.sig signing-public.pem)
for f in "${FILES[@]}";do test -f "$SRC/$f"||{ echo "FAIL missing $f";exit 2;};done
if [[ "$ROLE" == node2 && -f "$SRC/signing-private.pem" ]];then echo 'FAIL: Node2 must not receive M13 private signing key' >&2;exit 2;fi
install -d -m700 "$DEST";rm -f "$DEST/signing-private.pem"
for f in "${FILES[@]}";do install -m600 "$SRC/$f" "$DEST/$f";done
if [[ "$ROLE" == node1 && -f "$SRC/signing-private.pem" ]];then install -m600 "$SRC/signing-private.pem" "$DEST/signing-private.pem";fi
python3 "$ROOT/scripts/m13/validate_m13_node.py" --material "$DEST" --repo-root "$ROOT"
echo "PASS: M13 $ROLE material deployed to $DEST"
