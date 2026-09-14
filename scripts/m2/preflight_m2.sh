#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
ENV_FILE="${1:?usage: preflight_m2.sh production.env}"
[ -r "$ENV_FILE" ] || { echo "FAIL env-file $ENV_FILE"; exit 2; }
set -a; source "$ENV_FILE"; set +a
export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
fail=0
pass(){ printf 'PASS %-30s %s\n' "$1" "${2:-}"; }
err(){ printf 'FAIL %-30s %s\n' "$1" "${2:-}"; fail=1; }
for c in python3 openssl sha256sum; do command -v "$c" >/dev/null && pass "command:$c" "$(command -v "$c")" || err "command:$c" missing; done
[ "${PAG_SECURITY_PROFILE:-}" = production ] && pass profile production || err profile 'must be production'
[ "${PAG_FAIL_CLOSED:-}" = 1 ] && pass fail-closed 1 || err fail-closed 'must be 1'
[ "${PAG_MTLS_REQUIRED:-}" = 1 ] && pass mtls-required 1 || err mtls-required 'must be 1'
for v in PAG_NODE_ID PAG_IDENTITY_FILE PAG_SECRETS_DIR PAG_POLICY_CATALOG PAG_TLS_CA_FILE PAG_TLS_CERT_FILE PAG_TLS_KEY_FILE PAG_WORKLOAD_REGISTRY; do
  value="${!v:-}"; [ -n "$value" ] && pass "$v" "$value" || err "$v" missing
done
python -m portable_ai_governance.cli validate-security >/tmp/pag-m2-security-profile.json || { cat /tmp/pag-m2-security-profile.json; err security-profile rejected; }
[ "$fail" -eq 0 ] || { echo 'M2 PREFLIGHT: FAIL'; exit 2; }
echo 'M2 PREFLIGHT: PASS'
