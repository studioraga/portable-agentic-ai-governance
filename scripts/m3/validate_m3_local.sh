#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"; TMP="$ROOT/var/m3-validation"; rm -rf "$TMP"; mkdir -p "$TMP"
export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
"$ROOT/scripts/m2/validate_m2_local.sh" >/dev/null
python3 "$ROOT/scripts/m3/build_m3_material.py" --root "$ROOT" --out "$TMP/material"
# verifier-only copy intentionally excludes private signing key
mkdir "$TMP/verifier"; cp -a "$TMP/material/." "$TMP/verifier/"; rm -f "$TMP/verifier/signing-private.pem"
PAG_M3_ALLOW_FIXTURE_SCAN=1 "$ROOT/deploy/m3/deploy_node.sh" "$TMP/verifier" "$TMP/node-config"
"$ROOT/scripts/m3/preflight_m3.sh" "$TMP/node-config/m3.env"
python3 "$ROOT/scripts/m3/validate_m3_node.py" "$TMP/node-config/m3.env"
# Negative: prompt tamper
cp "$TMP/node-config/assets/system-prompt.txt" "$TMP/prompt.bak"; printf 'tampered\n' > "$TMP/node-config/assets/system-prompt.txt"
if python3 "$ROOT/scripts/m3/validate_m3_node.py" "$TMP/node-config/m3.env" >/dev/null 2>&1; then echo 'FAIL prompt-tamper accepted'; exit 2; else echo 'PASS prompt-tamper-rejected'; fi
mv "$TMP/prompt.bak" "$TMP/node-config/assets/system-prompt.txt"
# Negative: SBOM signature tamper
printf '\n' >> "$TMP/node-config/software.cdx.json"
if python3 "$ROOT/scripts/m3/validate_m3_node.py" "$TMP/node-config/m3.env" >/dev/null 2>&1; then echo 'FAIL signed-sbom-tamper accepted'; exit 2; else echo 'PASS signed-sbom-tamper-rejected'; fi
cp "$TMP/material/software.cdx.json" "$TMP/node-config/software.cdx.json"
# Negative: high vulnerability
python3 - "$TMP/node-config/vulnerability-report.json" <<'PY'
import json,sys
p=sys.argv[1]; d=json.load(open(p)); d['vulnerabilities']=[{'id':'CVE-TEST-HIGH','severity':'high'}]; open(p,'w').write(json.dumps(d))
PY
if python3 "$ROOT/scripts/m3/validate_m3_node.py" "$TMP/node-config/m3.env" >/dev/null 2>&1; then echo 'FAIL high-vulnerability accepted'; exit 2; else echo 'PASS high-vulnerability-rejected'; fi
cp "$TMP/material/vulnerability-report.json" "$TMP/node-config/vulnerability-report.json"
"$ROOT/scripts/m3/validate_combined_node.sh" "$ROOT/var/m2-validation/node1-config/production.env" "$TMP/node-config/m3.env" >/dev/null
echo 'PASS combined-m2-m3-production-profile'
echo 'PASS: Milestone 3 local supply-chain validation complete'
