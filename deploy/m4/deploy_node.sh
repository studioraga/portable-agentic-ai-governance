#!/usr/bin/env bash
set -euo pipefail
umask 077
SRC="${1:?usage deploy_node.sh <m4-material-dir> <m3-lock-file> [dest]}"; M3LOCK="${2:?m3 lock required}"; DEST="${3:-$HOME/.config/portable-ai-governance/m4}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
[ -d "$SRC" ] || { echo "FAIL material dir missing: $SRC"; exit 2; }; [ -f "$M3LOCK" ] || { echo "FAIL M3 lock missing: $M3LOCK"; exit 2; }
install -d -m 700 "$DEST"
for f in ai-security-manifest.json ai-security-manifest.json.sig signing-public.pem model-governance.json data-provenance.json retrieval-policy.json embedding-policy.json evaluation-suite.json evaluation-results.json threat-model.json; do install -m 600 "$SRC/$f" "$DEST/$f"; done
install -m 600 "$M3LOCK" "$DEST/m3-artifact-locks.json"
cat > "$DEST/m4.env" <<EOF
PAG_AI_SECURITY_REQUIRED=1
PAG_M4_ROOT=$DEST
PAG_M4_MANIFEST=$DEST/ai-security-manifest.json
PAG_M4_MANIFEST_SIG=$DEST/ai-security-manifest.json.sig
PAG_M4_PUBLIC_KEY=$DEST/signing-public.pem
PAG_M4_MODEL_GOVERNANCE=$DEST/model-governance.json
PAG_M4_DATA_PROVENANCE=$DEST/data-provenance.json
PAG_M4_RETRIEVAL_POLICY=$DEST/retrieval-policy.json
PAG_M4_EMBEDDING_POLICY=$DEST/embedding-policy.json
PAG_M4_EVAL_SUITE=$DEST/evaluation-suite.json
PAG_M4_EVAL_RESULTS=$DEST/evaluation-results.json
PAG_M4_THREAT_MODEL=$DEST/threat-model.json
PAG_M3_LOCK_FILE=$DEST/m3-artifact-locks.json
EOF
chmod 600 "$DEST/m4.env"
python3 "$ROOT/scripts/m4/validate_m4_node.py" "$DEST/m4.env"
echo "PASS: M4 verifier material deployed to $DEST"
