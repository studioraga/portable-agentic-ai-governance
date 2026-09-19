#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.."&&pwd)";M2="$1";M3="$2";M4="$3";M5="$4";M6="$5";M7="$6";M8="$7";M9="$8";M10="$9";set -a;source "$M2";source "$M3";source "$M4";source "$M5";source "$M6";source "$M7";source "$M8";source "$M9";source "$M10";set +a;export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}";python3 - <<'PY'
import json
from portable_ai_governance.kernel.security_profile import evaluate_security_profile
r=evaluate_security_profile();print(json.dumps({'profile':r.profile,'ok':r.ok,'checks':[{'name':x.name,'ok':x.ok,'detail':x.detail} for x in r.checks]},indent=2));raise SystemExit(0 if r.ok else 2)
PY
python3 "$ROOT/scripts/m10/validate_m10_node.py" "$M10" >/dev/null
echo 'PASS: combined M2+M3+M4+M5+M6+M7+M8+M9+M10 production node validation complete'
