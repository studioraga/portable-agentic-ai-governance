#!/usr/bin/env bash
set -euo pipefail
umask 077
SRC="${1:?m9 material}";M8MAN="${2:?m8 manifest}";DEST="${3:-$HOME/.config/portable-ai-governance/m9}";ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.."&&pwd)"
case "$DEST" in ""|/|"$HOME"|"$HOME/.config"|"$HOME/.config/portable-ai-governance") echo "FAIL: unsafe M9 destination: $DEST" >&2;exit 2;;esac
for f in security-ops-manifest.json security-ops-manifest.json.sig signing-public.pem security-ops-policy.json recovery-signing-public.pem;do test -f "$SRC/$f"||{ echo "FAIL missing $f";exit 2;};done
test -f "$M8MAN"||{ echo 'FAIL missing M8 manifest';exit 2;}
install -d -m700 "$DEST" "$DEST/runtime" "$DEST/runtime/secops"
rm -f "$DEST/signing-private.pem" "$DEST/recovery-signing-private.pem"
for f in security-ops-manifest.json security-ops-manifest.json.sig signing-public.pem security-ops-policy.json recovery-signing-public.pem;do install -m600 "$SRC/$f" "$DEST/$f";done
install -m600 "$M8MAN" "$DEST/m8-action-agent-manifest.json"
cat > "$DEST/m9.env" <<EOF
PAG_SECURITY_OPS_REQUIRED=1
PAG_M9_ROOT=$DEST
PAG_M9_MANIFEST=$DEST/security-ops-manifest.json
PAG_M9_MANIFEST_SIG=$DEST/security-ops-manifest.json.sig
PAG_M9_PUBLIC_KEY=$DEST/signing-public.pem
PAG_M9_POLICY=$DEST/security-ops-policy.json
PAG_M9_RECOVERY_PUBLIC_KEY=$DEST/recovery-signing-public.pem
PAG_M8_MANIFEST=$DEST/m8-action-agent-manifest.json
PAG_M9_RUNTIME_ROOT=$DEST/runtime/secops
EOF
chmod 600 "$DEST/m9.env";find "$DEST" -type d -exec chmod 700 {} +;find "$DEST" -type f -exec chmod 600 {} +
python3 "$ROOT/scripts/m9/validate_m9_node.py" "$DEST/m9.env";echo "PASS: M9 security-operations material deployed to $DEST (runtime SecOps state preserved)"
