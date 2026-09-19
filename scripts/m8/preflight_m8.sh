#!/usr/bin/env bash
set -euo pipefail
ENVF="${1:?usage preflight_m8.sh m8.env}";set -a;source "$ENVF";set +a
for n in PAG_M8_MANIFEST PAG_M8_MANIFEST_SIG PAG_M8_PUBLIC_KEY PAG_M8_AGENT_POLICY PAG_M8_TOOL_REGISTRY PAG_M8_AUTHORIZATION_RULES PAG_M8_APPROVAL_AUTHORITIES PAG_M8_APPROVAL_PUBLIC_KEY PAG_M7_MANIFEST; do v="${!n:-}"; [ -f "$v" ] || { echo "FAIL $n $v"; exit 2; }; echo "PASS $n $v"; done
[ -n "${PAG_M8_ACTION_ROOT:-}" ] || { echo 'FAIL PAG_M8_ACTION_ROOT'; exit 2; };echo 'M8 PREFLIGHT: PASS'
