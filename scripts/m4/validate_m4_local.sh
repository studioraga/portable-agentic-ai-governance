#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"; TMP="$ROOT/var/m4-validation"; rm -rf "$TMP"; mkdir -p "$TMP"
export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
"$ROOT/scripts/m3/validate_m3_local.sh" >/dev/null
M3MAT="$ROOT/var/m3-validation/material"
python3 "$ROOT/scripts/m4/build_m4_material.py" --m3-material "$M3MAT" --out "$TMP/material"
mkdir -m 700 "$TMP/verifier"; cp -a "$TMP/material/." "$TMP/verifier/"; rm -f "$TMP/verifier/signing-private.pem"
"$ROOT/deploy/m4/deploy_node.sh" "$TMP/verifier" "$M3MAT/artifact-locks.json" "$TMP/node-config" >/dev/null
"$ROOT/scripts/m4/preflight_m4.sh" "$TMP/node-config/m4.env"
python3 "$ROOT/scripts/m4/validate_m4_node.py" "$TMP/node-config/m4.env"
# Negative: cross-tenant retrieval must be denied
python3 - <<'PY'
from portable_ai_governance.ai_security.retrieval import RetrievalPrincipal,authorize_record
p=RetrievalPrincipal('u','tenant-a','internal',('ai_user',)); r={'tenant':'tenant-b','classification':'public'}; policy={'deny_cross_tenant':True,'allowed_roles':['ai_user']}
assert authorize_record(p,r,policy)[0] is False
print('PASS cross-tenant-retrieval-rejected')
PY
# Negative: evaluation failure blocks
cp "$TMP/node-config/evaluation-results.json" "$TMP/eval.bak"
python3 - "$TMP/node-config/evaluation-results.json" <<'PY'
import json,sys
p=sys.argv[1]; d=json.load(open(p)); d['results'][0]['passed']=False; d['score']=0.5; open(p,'w').write(json.dumps(d))
PY
if python3 "$ROOT/scripts/m4/validate_m4_node.py" "$TMP/node-config/m4.env" >/dev/null 2>&1; then echo 'FAIL evaluation-failure accepted'; exit 2; else echo 'PASS evaluation-failure-rejected'; fi
mv "$TMP/eval.bak" "$TMP/node-config/evaluation-results.json"
# Negative: autonomy enabled blocks
cp "$TMP/node-config/threat-model.json" "$TMP/threat.bak"
python3 - "$TMP/node-config/threat-model.json" <<'PY'
import json,sys
p=sys.argv[1]; d=json.load(open(p)); d['llm_agent_autonomy']=True; open(p,'w').write(json.dumps(d))
PY
if python3 "$ROOT/scripts/m4/validate_m4_node.py" "$TMP/node-config/m4.env" >/dev/null 2>&1; then echo 'FAIL autonomy accepted'; exit 2; else echo 'PASS autonomy-rejected'; fi
mv "$TMP/threat.bak" "$TMP/node-config/threat-model.json"
# Negative: model digest drift blocks
cp "$TMP/node-config/model-governance.json" "$TMP/model.bak"
python3 - "$TMP/node-config/model-governance.json" <<'PY'
import json,sys
p=sys.argv[1]; d=json.load(open(p)); d['models'][0]['sha256']='0'*64; open(p,'w').write(json.dumps(d))
PY
if python3 "$ROOT/scripts/m4/validate_m4_node.py" "$TMP/node-config/m4.env" >/dev/null 2>&1; then echo 'FAIL model-digest-drift accepted'; exit 2; else echo 'PASS model-digest-drift-rejected'; fi
mv "$TMP/model.bak" "$TMP/node-config/model-governance.json"
"$ROOT/scripts/m4/validate_combined_node.sh" "$ROOT/var/m2-validation/node1-config/production.env" "$ROOT/var/m3-validation/node-config/m3.env" "$TMP/node-config/m4.env" >/dev/null
echo 'PASS combined-m2-m3-m4-production-profile'
echo 'PASS: Milestone 4 local AI-security validation complete'
