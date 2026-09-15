#!/usr/bin/env bash
set -euo pipefail
umask 077
SRC="${1:?usage deploy_node.sh <m6-material-dir> <m5-manifest> [dest]}"; M5MAN="${2:?M5 manifest required}"; DEST="${3:-$HOME/.config/portable-ai-governance/m6}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
[ -d "$SRC" ] || { echo "FAIL material dir missing: $SRC"; exit 2; }; [ -f "$M5MAN" ] || { echo "FAIL M5 manifest missing: $M5MAN"; exit 2; }
rm -rf "$DEST"; install -d -m 700 "$DEST" "$DEST/evidence"
for f in evidence-analyst-manifest.json evidence-analyst-manifest.json.sig signing-public.pem agent-policy.json evidence-catalog.json; do install -m 600 "$SRC/$f" "$DEST/$f"; done
cp -a "$SRC/evidence/." "$DEST/evidence/"; find "$DEST/evidence" -type d -exec chmod 700 {} +; find "$DEST/evidence" -type f -exec chmod 600 {} +
install -m 600 "$M5MAN" "$DEST/m5-compliance-risk-manifest.json"
cat > "$DEST/m6.env" <<EOF2
PAG_EVIDENCE_ANALYST_REQUIRED=1
PAG_M6_ROOT=$DEST
PAG_M6_MANIFEST=$DEST/evidence-analyst-manifest.json
PAG_M6_MANIFEST_SIG=$DEST/evidence-analyst-manifest.json.sig
PAG_M6_PUBLIC_KEY=$DEST/signing-public.pem
PAG_M6_AGENT_POLICY=$DEST/agent-policy.json
PAG_M6_EVIDENCE_CATALOG=$DEST/evidence-catalog.json
PAG_M6_EVIDENCE_ROOT=$DEST/evidence
PAG_M5_MANIFEST=$DEST/m5-compliance-risk-manifest.json
EOF2
chmod 600 "$DEST/m6.env"
python3 "$ROOT/scripts/m6/validate_m6_node.py" "$DEST/m6.env"
echo "PASS: M6 Evidence Analyst verifier material deployed to $DEST"
