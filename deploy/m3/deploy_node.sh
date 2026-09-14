#!/usr/bin/env bash
set -euo pipefail
umask 077
SRC="${1:?usage deploy_node.sh <material-dir> [dest]}"; DEST="${2:-$HOME/.config/portable-ai-governance/m3}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
[ -d "$SRC" ] || { echo "FAIL: material dir missing: $SRC"; exit 2; }
install -d -m 700 "$DEST" "$DEST/assets"
for f in artifact-locks.json software.cdx.json software.cdx.json.sig ai-ml.cdx.json ai-ml.cdx.json.sig provenance.intoto.json provenance.intoto.json.sig signing-public.pem vulnerability-policy.json vulnerability-report.json; do
  install -m 600 "$SRC/$f" "$DEST/$f"
done
cp -a "$SRC/assets/." "$DEST/assets/"; chmod -R go-rwx "$DEST/assets"
cat > "$DEST/m3.env" <<EOF
PAG_SUPPLY_CHAIN_REQUIRED=1
PAG_M3_ALLOW_FIXTURE_SCAN=${PAG_M3_ALLOW_FIXTURE_SCAN:-0}
PAG_M3_ROOT=$DEST
PAG_M3_LOCK_FILE=$DEST/artifact-locks.json
PAG_M3_SBOM=$DEST/software.cdx.json
PAG_M3_SBOM_SIG=$DEST/software.cdx.json.sig
PAG_M3_AI_BOM=$DEST/ai-ml.cdx.json
PAG_M3_AI_BOM_SIG=$DEST/ai-ml.cdx.json.sig
PAG_M3_PROVENANCE=$DEST/provenance.intoto.json
PAG_M3_PROVENANCE_SIG=$DEST/provenance.intoto.json.sig
PAG_M3_PUBLIC_KEY=$DEST/signing-public.pem
PAG_M3_VULN_REPORT=$DEST/vulnerability-report.json
PAG_M3_VULN_POLICY=$DEST/vulnerability-policy.json
EOF
chmod 600 "$DEST/m3.env"
PYTHONPATH="$ROOT/src" python3 "$ROOT/scripts/m3/validate_m3_node.py" "$DEST/m3.env"
echo "PASS: M3 verifier material deployed to $DEST"
