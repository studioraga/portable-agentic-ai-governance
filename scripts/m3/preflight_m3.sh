#!/usr/bin/env bash
set -euo pipefail
umask 077
ENV_FILE="${1:?usage: preflight_m3.sh <m3.env>}"
[ -r "$ENV_FILE" ] || { echo "FAIL env-file $ENV_FILE"; exit 2; }
set -a; source "$ENV_FILE"; set +a
bad=0
pass(){ printf 'PASS %-30s %s\n' "$1" "$2"; }
fail(){ printf 'FAIL %-30s %s\n' "$1" "$2"; bad=1; }
[ "${PAG_SUPPLY_CHAIN_REQUIRED:-}" = 1 ] && pass supply-chain-required 1 || fail supply-chain-required required
for n in PAG_M3_LOCK_FILE PAG_M3_SBOM PAG_M3_AI_BOM PAG_M3_PROVENANCE PAG_M3_PUBLIC_KEY PAG_M3_VULN_REPORT PAG_M3_VULN_POLICY; do
 p="${!n:-}"; [ -r "$p" ] && pass "$n" "$p" || fail "$n" "missing/unreadable"
done
for n in PAG_M3_SBOM_SIG PAG_M3_AI_BOM_SIG PAG_M3_PROVENANCE_SIG; do p="${!n:-}"; [ -r "$p" ] && pass "$n" "$p" || fail "$n" missing; done
if [ "$bad" -ne 0 ]; then echo 'M3 PREFLIGHT: FAIL'; exit 2; fi
echo 'M3 PREFLIGHT: PASS'
