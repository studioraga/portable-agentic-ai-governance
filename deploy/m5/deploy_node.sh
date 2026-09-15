#!/usr/bin/env bash
set -euo pipefail
umask 077
SRC="${1:?usage deploy_node.sh <m5-material-dir> <m4-manifest> [dest]}"; M4MAN="${2:?M4 manifest required}"; DEST="${3:-$HOME/.config/portable-ai-governance/m5}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
[ -d "$SRC" ] || { echo "FAIL material dir missing: $SRC"; exit 2; }; [ -f "$M4MAN" ] || { echo "FAIL M4 manifest missing: $M4MAN"; exit 2; }
install -d -m 700 "$DEST"
for f in compliance-risk-manifest.json compliance-risk-manifest.json.sig signing-public.pem impact-assessment.json privacy-assessment.json exception-register.json third-parties.json continuous-controls.json compliance-report.json; do install -m 600 "$SRC/$f" "$DEST/$f"; done
install -m 600 "$M4MAN" "$DEST/m4-ai-security-manifest.json"
cat > "$DEST/m5.env" <<EOF2
PAG_COMPLIANCE_RISK_REQUIRED=1
PAG_M5_ROOT=$DEST
PAG_M5_MANIFEST=$DEST/compliance-risk-manifest.json
PAG_M5_MANIFEST_SIG=$DEST/compliance-risk-manifest.json.sig
PAG_M5_PUBLIC_KEY=$DEST/signing-public.pem
PAG_M5_IMPACT_ASSESSMENT=$DEST/impact-assessment.json
PAG_M5_PRIVACY_ASSESSMENT=$DEST/privacy-assessment.json
PAG_M5_EXCEPTION_REGISTER=$DEST/exception-register.json
PAG_M5_THIRD_PARTIES=$DEST/third-parties.json
PAG_M5_CONTINUOUS_CONTROLS=$DEST/continuous-controls.json
PAG_M5_COMPLIANCE_REPORT=$DEST/compliance-report.json
PAG_M4_MANIFEST=$DEST/m4-ai-security-manifest.json
EOF2
chmod 600 "$DEST/m5.env"
python3 "$ROOT/scripts/m5/validate_m5_node.py" "$DEST/m5.env"
echo "PASS: M5 verifier material deployed to $DEST"
