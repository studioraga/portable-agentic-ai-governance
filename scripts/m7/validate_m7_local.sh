#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"; TMP="$ROOT/var/m7-validation"; rm -rf "$TMP"; mkdir -p "$TMP"; export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
"$ROOT/scripts/m6/validate_m6_local.sh" >/dev/null
M2="$ROOT/var/m2-validation/node1-config/production.env"; M6MAT="$ROOT/var/m6-validation/material"; M6ENV="$ROOT/var/m6-validation/node-config/m6.env"
python3 "$ROOT/scripts/m7/build_m7_material.py" --m6-material "$M6MAT" --out "$TMP/material"
mkdir -m 700 "$TMP/verifier"; cp -a "$TMP/material/." "$TMP/verifier/"; rm -f "$TMP/verifier/signing-private.pem"
"$ROOT/deploy/m7/deploy_node.sh" "$TMP/verifier" "$M6MAT/evidence-analyst-manifest.json" "$TMP/node-config" >/dev/null
"$ROOT/scripts/m7/preflight_m7.sh" "$TMP/node-config/m7.env"
python3 "$ROOT/scripts/m7/validate_m7_node.py" "$TMP/node-config/m7.env"
python3 "$ROOT/scripts/m7/run_tool_agent.py" --m2-env "$M2" --m6-env "$M6ENV" --m7-env "$TMP/node-config/m7.env" --tool evidence.verify --evidence-id 'm5:compliance-risk-manifest.json' --run-id m7-local --call-id c1 >/dev/null
echo 'PASS typed-tool-positive-path'
python3 -m pytest -q "$ROOT/tests/tool_agent/test_m7_tool_agent.py" >/dev/null
echo 'PASS schema-authorization-policy-budget-audit-negative-suite'
# Negative: M6 binding drift must fail static validation.
cp "$TMP/node-config/m6-evidence-analyst-manifest.json" "$TMP/m6.bak"; printf '\n' >> "$TMP/node-config/m6-evidence-analyst-manifest.json"
if python3 "$ROOT/scripts/m7/validate_m7_node.py" "$TMP/node-config/m7.env" >/dev/null 2>&1; then echo 'FAIL m6-binding-drift accepted'; exit 2; else echo 'PASS m6-binding-drift-rejected'; fi
mv "$TMP/m6.bak" "$TMP/node-config/m6-evidence-analyst-manifest.json"
# Negative: side-effecting registry entry must fail static validation.
cp "$TMP/node-config/typed-tool-registry.json" "$TMP/registry.bak"
python3 - "$TMP/node-config/typed-tool-registry.json" <<'PY2'
import json,sys
p=sys.argv[1]; d=json.load(open(p)); d['tools'][0]['side_effecting']=True; open(p,'w').write(json.dumps(d))
PY2
if python3 "$ROOT/scripts/m7/validate_m7_node.py" "$TMP/node-config/m7.env" >/dev/null 2>&1; then echo 'FAIL side-effecting-registry accepted'; exit 2; else echo 'PASS side-effecting-registry-rejected'; fi
mv "$TMP/registry.bak" "$TMP/node-config/typed-tool-registry.json"
"$ROOT/scripts/m7/validate_combined_node.sh" "$ROOT/var/m2-validation/node1-config/production.env" "$ROOT/var/m3-validation/node-config/m3.env" "$ROOT/var/m4-validation/node-config/m4.env" "$ROOT/var/m5-validation/node-config/m5.env" "$ROOT/var/m6-validation/node-config/m6.env" "$TMP/node-config/m7.env" >/dev/null
echo 'PASS combined-m2-m3-m4-m5-m6-m7-production-profile'
echo 'PASS: Milestone 7 mediated typed-tool agent validation complete'
