#!/usr/bin/env bash
set -euo pipefail
umask 077
ROLE="${1:?role required}";SRC="${2:?m12 material directory required}";DEST="${3:-$HOME/.config/portable-ai-governance/m12}";ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.."&&pwd)"
[[ "$ROLE" == node1 || "$ROLE" == node2 ]]||{ echo "FAIL: role must be node1 or node2" >&2;exit 2;}
case "$DEST" in ""|/|"$HOME"|"$HOME/.config"|"$HOME/.config/portable-ai-governance") echo "FAIL: unsafe M12 destination: $DEST" >&2;exit 2;;esac
FILES=(intelligence-source-policy.json m12-control-mapping.json product-inventory.json normalized-vulnerabilities.json exploitation-evidence.json aev-assessments.json m12-intel-manifest.json m12-intel-manifest.json.sig signing-public.pem)
for f in "${FILES[@]}";do test -f "$SRC/$f"||{ echo "FAIL missing $f";exit 2;};done
if [[ "$ROLE" == node2 && -f "$SRC/signing-private.pem" ]];then echo 'FAIL: Node2 must not receive M12 private signing key' >&2;exit 2;fi
install -d -m700 "$DEST";rm -f "$DEST/signing-private.pem"
for f in "${FILES[@]}";do install -m600 "$SRC/$f" "$DEST/$f";done
if [[ "$ROLE" == node1 && -f "$SRC/signing-private.pem" ]];then install -m600 "$SRC/signing-private.pem" "$DEST/signing-private.pem";fi
python3 "$ROOT/scripts/m12/validate_m12_node.py" --material "$DEST" --repo-root "$ROOT"
echo "PASS: M12 $ROLE material deployed to $DEST"
