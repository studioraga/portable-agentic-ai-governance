#!/usr/bin/env bash
set -euo pipefail
ENV="${1:?usage: preflight_m5.sh <m5.env>}"
[ -f "$ENV" ] || { echo "FAIL env missing: $ENV"; exit 2; }
set -a; source "$ENV"; set +a
[ "${PAG_COMPLIANCE_RISK_REQUIRED:-0}" = 1 ] || { echo 'FAIL compliance-risk-required'; exit 2; }
for n in PAG_M5_MANIFEST PAG_M5_MANIFEST_SIG PAG_M5_PUBLIC_KEY PAG_M5_IMPACT_ASSESSMENT PAG_M5_PRIVACY_ASSESSMENT PAG_M5_EXCEPTION_REGISTER PAG_M5_THIRD_PARTIES PAG_M5_CONTINUOUS_CONTROLS PAG_M5_COMPLIANCE_REPORT PAG_M4_MANIFEST; do v="${!n:-}"; [ -f "$v" ] || { echo "FAIL $n $v"; exit 2; }; echo "PASS $n $v"; done
echo 'M5 PREFLIGHT: PASS'
