#!/usr/bin/env bash
set -euo pipefail
umask 077
SRC="${1:?m10 material}";M9MAN="${2:?m9 manifest}";DEST="${3:-$HOME/.config/portable-ai-governance/m10}";ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.."&&pwd)"
case "$DEST" in ""|/|"$HOME"|"$HOME/.config"|"$HOME/.config/portable-ai-governance") echo "FAIL: unsafe M10 destination: $DEST" >&2;exit 2;;esac
for f in multi-agent-manifest.json multi-agent-manifest.json.sig signing-public.pem multi-agent-policy.json multi-agent-topology.json workflow-decision-public.pem;do test -f "$SRC/$f"||{ echo "FAIL missing $f";exit 2;};done
test -f "$M9MAN"||{ echo 'FAIL missing M9 manifest';exit 2;}
install -d -m700 "$DEST" "$DEST/runtime" "$DEST/runtime/multi-agent"
rm -f "$DEST/signing-private.pem" "$DEST/workflow-decision-private.pem"
for f in multi-agent-manifest.json multi-agent-manifest.json.sig signing-public.pem multi-agent-policy.json multi-agent-topology.json workflow-decision-public.pem;do install -m600 "$SRC/$f" "$DEST/$f";done
install -m600 "$M9MAN" "$DEST/m9-security-ops-manifest.json"
cat > "$DEST/m10.env" <<EOF
PAG_MULTI_AGENT_REQUIRED=1
PAG_M10_ROOT=$DEST
PAG_M10_MANIFEST=$DEST/multi-agent-manifest.json
PAG_M10_MANIFEST_SIG=$DEST/multi-agent-manifest.json.sig
PAG_M10_PUBLIC_KEY=$DEST/signing-public.pem
PAG_M10_POLICY=$DEST/multi-agent-policy.json
PAG_M10_TOPOLOGY=$DEST/multi-agent-topology.json
PAG_M10_DECISION_PUBLIC_KEY=$DEST/workflow-decision-public.pem
PAG_M9_MANIFEST=$DEST/m9-security-ops-manifest.json
PAG_M10_RUNTIME_ROOT=$DEST/runtime/multi-agent
EOF
chmod 600 "$DEST/m10.env";find "$DEST" -type d -exec chmod 700 {} +;find "$DEST" -type f -exec chmod 600 {} +
python3 "$ROOT/scripts/m10/validate_m10_node.py" "$DEST/m10.env"
echo "PASS: M10 multi-agent material deployed to $DEST (runtime workflow state preserved)"
