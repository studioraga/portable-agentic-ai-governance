#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"; TMP="$ROOT/var/m6-validation"; rm -rf "$TMP"; mkdir -p "$TMP"; export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
"$ROOT/scripts/m5/validate_m5_local.sh" >/dev/null
M3="$ROOT/var/m3-validation/material"; M4="$ROOT/var/m4-validation/material"; M5="$ROOT/var/m5-validation/material"
python3 "$ROOT/scripts/m6/build_m6_material.py" --m3-material "$M3" --m4-material "$M4" --m5-material "$M5" --out "$TMP/material"
mkdir -m 700 "$TMP/verifier"; cp -a "$TMP/material/." "$TMP/verifier/"; rm -f "$TMP/verifier/signing-private.pem"
"$ROOT/deploy/m6/deploy_node.sh" "$TMP/verifier" "$M5/compliance-risk-manifest.json" "$TMP/node-config" >/dev/null
"$ROOT/scripts/m6/preflight_m6.sh" "$TMP/node-config/m6.env"
python3 "$ROOT/scripts/m6/validate_m6_node.py" "$TMP/node-config/m6.env"
python3 "$ROOT/scripts/m6/run_evidence_analyst.py" --env "$TMP/node-config/m6.env" --operation evidence.list >/dev/null
python3 "$ROOT/scripts/m6/run_evidence_analyst.py" --env "$TMP/node-config/m6.env" --operation evidence.verify --evidence-id 'm5:compliance-risk-manifest.json' >/dev/null
echo 'PASS bounded-read-only-positive-path'
# Negative: side-effecting tool request must be impossible at CLI/parser boundary or agent policy
if python3 - "$ROOT" "$TMP/node-config/m6.env" <<'PY' >/dev/null 2>&1
import sys
from pathlib import Path
sys.path.insert(0,str(Path(sys.argv[1])/'src'))
from portable_ai_governance.evidence_analyst.agent import EvidenceAnalyst,AgentRequest
from portable_ai_governance.evidence_analyst.runtime import require_evidence_analyst
E={}
for line in open(sys.argv[2]):
    if '=' in line and not line.startswith('#'):
        k,v=line.rstrip().split('=',1); E[k]=v
require_evidence_analyst(E)
a=EvidenceAnalyst(E['PAG_M6_AGENT_POLICY'],E['PAG_M6_EVIDENCE_CATALOG'],E['PAG_M6_EVIDENCE_ROOT'])
a.run(AgentRequest('write','m5:compliance-risk-manifest.json'))
PY
then echo 'FAIL side-effecting-tool accepted'; exit 2; else echo 'PASS side-effecting-tool-rejected'; fi
# Negative: catalog path escape
cp "$TMP/node-config/evidence-catalog.json" "$TMP/catalog.bak"
python3 - "$TMP/node-config/evidence-catalog.json" <<'PY'
import json,sys
p=sys.argv[1]; d=json.load(open(p)); d['entries'][0]['path']='../escape'; open(p,'w').write(json.dumps(d))
PY
if python3 "$ROOT/scripts/m6/validate_m6_node.py" "$TMP/node-config/m6.env" >/dev/null 2>&1; then echo 'FAIL catalog-path-escape accepted'; exit 2; else echo 'PASS catalog-path-escape-rejected'; fi
mv "$TMP/catalog.bak" "$TMP/node-config/evidence-catalog.json"
# Negative: evidence digest tamper
first="$(find "$TMP/node-config/evidence" -type f | head -1)"; cp "$first" "$TMP/evidence.bak"; printf '\nTAMPER\n' >> "$first"
if python3 "$ROOT/scripts/m6/validate_m6_node.py" "$TMP/node-config/m6.env" >/dev/null 2>&1; then echo 'FAIL evidence-tamper accepted'; exit 2; else echo 'PASS evidence-tamper-rejected'; fi
mv "$TMP/evidence.bak" "$first"
# Negative: M5 binding drift
cp "$TMP/node-config/m5-compliance-risk-manifest.json" "$TMP/m5.bak"; printf '\n' >> "$TMP/node-config/m5-compliance-risk-manifest.json"
if python3 "$ROOT/scripts/m6/validate_m6_node.py" "$TMP/node-config/m6.env" >/dev/null 2>&1; then echo 'FAIL m5-binding-drift accepted'; exit 2; else echo 'PASS m5-binding-drift-rejected'; fi
mv "$TMP/m5.bak" "$TMP/node-config/m5-compliance-risk-manifest.json"
"$ROOT/scripts/m6/validate_combined_node.sh" "$ROOT/var/m2-validation/node1-config/production.env" "$ROOT/var/m3-validation/node-config/m3.env" "$ROOT/var/m4-validation/node-config/m4.env" "$ROOT/var/m5-validation/node-config/m5.env" "$TMP/node-config/m6.env" >/dev/null
echo 'PASS combined-m2-m3-m4-m5-m6-production-profile'
echo 'PASS: Milestone 6 bounded Evidence Analyst validation complete'
