#!/usr/bin/env bash
set -euo pipefail
umask 077
SRC="${1:?m8 material}";M7MAN="${2:?m7 manifest}";DEST="${3:-$HOME/.config/portable-ai-governance/m8}";ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
case "$DEST" in ""|/|"$HOME"|"$HOME/.config"|"$HOME/.config/portable-ai-governance") echo "FAIL: unsafe M8 destination: $DEST" >&2; exit 2;; esac
for f in action-agent-manifest.json action-agent-manifest.json.sig signing-public.pem action-agent-policy.json action-tool-registry.json action-authorization-rules.json approval-authorities.json approval-signing-public.pem;do
  test -f "$SRC/$f" || { echo "FAIL: missing M8 source artifact: $SRC/$f" >&2; exit 2; }
done
test -f "$M7MAN" || { echo "FAIL: missing M7 manifest: $M7MAN" >&2; exit 2; }
# Preserve runtime/actions across redeploy so one-use approvals and effect journals remain durable.
install -d -m700 "$DEST" "$DEST/runtime" "$DEST/runtime/actions"
rm -f "$DEST/signing-private.pem" "$DEST/approval-signing-private.pem"
for f in action-agent-manifest.json action-agent-manifest.json.sig signing-public.pem action-agent-policy.json action-tool-registry.json action-authorization-rules.json approval-authorities.json approval-signing-public.pem;do install -m600 "$SRC/$f" "$DEST/$f";done
install -m600 "$M7MAN" "$DEST/m7-tool-agent-manifest.json"
cat >"$DEST/m8.env" <<EOF
PAG_ACTION_AGENT_REQUIRED=1
PAG_M8_ROOT=$DEST
PAG_M8_MANIFEST=$DEST/action-agent-manifest.json
PAG_M8_MANIFEST_SIG=$DEST/action-agent-manifest.json.sig
PAG_M8_PUBLIC_KEY=$DEST/signing-public.pem
PAG_M8_AGENT_POLICY=$DEST/action-agent-policy.json
PAG_M8_TOOL_REGISTRY=$DEST/action-tool-registry.json
PAG_M8_AUTHORIZATION_RULES=$DEST/action-authorization-rules.json
PAG_M8_APPROVAL_AUTHORITIES=$DEST/approval-authorities.json
PAG_M8_APPROVAL_PUBLIC_KEY=$DEST/approval-signing-public.pem
PAG_M7_MANIFEST=$DEST/m7-tool-agent-manifest.json
PAG_M8_ACTION_ROOT=$DEST/runtime/actions
EOF
chmod 600 "$DEST/m8.env";find "$DEST" -type d -exec chmod 700 {} +;find "$DEST" -type f -exec chmod 600 {} +;python3 "$ROOT/scripts/m8/validate_m8_node.py" "$DEST/m8.env";echo "PASS: M8 approval-controlled action material deployed to $DEST (runtime action state preserved)"
