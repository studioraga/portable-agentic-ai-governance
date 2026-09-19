#!/usr/bin/env bash
set -euo pipefail
umask 077
SRC="${1:?usage deploy_node.sh <m7-material-dir> <m6-manifest> [dest]}"; M6MAN="${2:?M6 manifest required}"; DEST="${3:-$HOME/.config/portable-ai-governance/m7}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
[ -d "$SRC" ] || { echo "FAIL M7 material missing: $SRC"; exit 2; }; [ -f "$M6MAN" ] || { echo "FAIL M6 manifest missing: $M6MAN"; exit 2; }
rm -rf "$DEST"; install -d -m 700 "$DEST"
for f in tool-agent-manifest.json tool-agent-manifest.json.sig signing-public.pem tool-agent-policy.json typed-tool-registry.json tool-authorization-rules.json; do install -m 600 "$SRC/$f" "$DEST/$f"; done
install -m 600 "$M6MAN" "$DEST/m6-evidence-analyst-manifest.json"
cat > "$DEST/m7.env" <<EOF2
PAG_TOOL_AGENT_REQUIRED=1
PAG_M7_ROOT=$DEST
PAG_M7_MANIFEST=$DEST/tool-agent-manifest.json
PAG_M7_MANIFEST_SIG=$DEST/tool-agent-manifest.json.sig
PAG_M7_PUBLIC_KEY=$DEST/signing-public.pem
PAG_M7_AGENT_POLICY=$DEST/tool-agent-policy.json
PAG_M7_TOOL_REGISTRY=$DEST/typed-tool-registry.json
PAG_M7_AUTHORIZATION_RULES=$DEST/tool-authorization-rules.json
PAG_M6_MANIFEST=$DEST/m6-evidence-analyst-manifest.json
EOF2
chmod 600 "$DEST/m7.env"; find "$DEST" -type d -exec chmod 700 {} +; find "$DEST" -type f -exec chmod 600 {} +
python3 "$ROOT/scripts/m7/validate_m7_node.py" "$DEST/m7.env"
echo "PASS: M7 typed-tool verifier material deployed to $DEST"
