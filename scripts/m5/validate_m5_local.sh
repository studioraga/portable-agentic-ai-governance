#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"; TMP="$ROOT/var/m5-validation"; rm -rf "$TMP"; mkdir -p "$TMP"
export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
"$ROOT/scripts/m4/validate_m4_local.sh" >/dev/null
M4MAT="$ROOT/var/m4-validation/material"
python3 "$ROOT/scripts/m5/build_m5_material.py" --m4-material "$M4MAT" --out "$TMP/material"
mkdir -m 700 "$TMP/verifier"; cp -a "$TMP/material/." "$TMP/verifier/"; rm -f "$TMP/verifier/signing-private.pem"
"$ROOT/deploy/m5/deploy_node.sh" "$TMP/verifier" "$M4MAT/ai-security-manifest.json" "$TMP/node-config" >/dev/null
"$ROOT/scripts/m5/preflight_m5.sh" "$TMP/node-config/m5.env"
python3 "$ROOT/scripts/m5/validate_m5_node.py" "$TMP/node-config/m5.env"
# Negative: expired approved exception
cp "$TMP/node-config/exception-register.json" "$TMP/exceptions.bak"
python3 - "$TMP/node-config/exception-register.json" <<'PY'
import json,sys
p=sys.argv[1]; d=json.load(open(p)); d['exceptions']=[{'exception_id':'ex-1','control_id':'AIS-RAG-001','owner':'owner','approver':'approver','reason':'test','compensating_controls':['manual review'],'created_at':'2026-01-01T00:00:00Z','expires_at':'2026-01-02T00:00:00Z','status':'approved'}]; open(p,'w').write(json.dumps(d))
PY
if python3 "$ROOT/scripts/m5/validate_m5_node.py" "$TMP/node-config/m5.env" >/dev/null 2>&1; then echo 'FAIL expired-exception accepted'; exit 2; else echo 'PASS expired-exception-rejected'; fi
mv "$TMP/exceptions.bak" "$TMP/node-config/exception-register.json"
# Negative: privacy DPIA required but not approved
cp "$TMP/node-config/privacy-assessment.json" "$TMP/privacy.bak"
python3 - "$TMP/node-config/privacy-assessment.json" <<'PY'
import json,sys
p=sys.argv[1]; d=json.load(open(p)); d['dpia_required']=True; d['dpia_status']='pending'; open(p,'w').write(json.dumps(d))
PY
if python3 "$ROOT/scripts/m5/validate_m5_node.py" "$TMP/node-config/m5.env" >/dev/null 2>&1; then echo 'FAIL pending-dpia accepted'; exit 2; else echo 'PASS pending-dpia-rejected'; fi
mv "$TMP/privacy.bak" "$TMP/node-config/privacy-assessment.json"
# Negative: stale continuous control
cp "$TMP/node-config/continuous-controls.json" "$TMP/continuous.bak"
python3 - "$TMP/node-config/continuous-controls.json" <<'PY'
import json,sys
p=sys.argv[1]; d=json.load(open(p)); d['controls'][0]['last_checked']='2020-01-01T00:00:00Z'; open(p,'w').write(json.dumps(d))
PY
if python3 "$ROOT/scripts/m5/validate_m5_node.py" "$TMP/node-config/m5.env" >/dev/null 2>&1; then echo 'FAIL stale-control accepted'; exit 2; else echo 'PASS stale-control-rejected'; fi
mv "$TMP/continuous.bak" "$TMP/node-config/continuous-controls.json"
# Negative: automated certification claim prohibited
cp "$TMP/node-config/compliance-report.json" "$TMP/report.bak"
python3 - "$TMP/node-config/compliance-report.json" <<'PY'
import json,sys
p=sys.argv[1]; d=json.load(open(p)); d['certification_claim']=True; open(p,'w').write(json.dumps(d))
PY
if python3 "$ROOT/scripts/m5/validate_m5_node.py" "$TMP/node-config/m5.env" >/dev/null 2>&1; then echo 'FAIL certification-claim accepted'; exit 2; else echo 'PASS certification-claim-rejected'; fi
mv "$TMP/report.bak" "$TMP/node-config/compliance-report.json"
"$ROOT/scripts/m5/validate_combined_node.sh" "$ROOT/var/m2-validation/node1-config/production.env" "$ROOT/var/m3-validation/node-config/m3.env" "$ROOT/var/m4-validation/node-config/m4.env" "$TMP/node-config/m5.env" >/dev/null
echo 'PASS combined-m2-m3-m4-m5-production-profile'
echo 'PASS: Milestone 5 local compliance/risk validation complete'
