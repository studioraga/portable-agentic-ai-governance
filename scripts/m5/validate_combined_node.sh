#!/usr/bin/env bash
set -euo pipefail
M2="${1:?m2 env}"; M3="${2:?m3 env}"; M4="${3:?m4 env}"; M5="${4:?m5 env}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"; export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
set -a; source "$M2"; source "$M3"; source "$M4"; source "$M5"; set +a
python3 - <<'PY'
import json,os
from portable_ai_governance.kernel.security_profile import evaluate_security_profile
r=evaluate_security_profile(dict(os.environ)); print(json.dumps({'profile':r.profile,'ok':r.ok,'checks':[{'name':c.name,'ok':c.ok,'detail':c.detail} for c in r.checks]},indent=2)); raise SystemExit(0 if r.ok else 2)
PY
python3 "$ROOT/scripts/m5/validate_m5_node.py" "$M5"
echo 'PASS: combined M2+M3+M4+M5 production node validation complete'
