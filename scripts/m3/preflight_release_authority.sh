#!/usr/bin/env bash
set -euo pipefail
bad=0
pass(){ printf 'PASS %-28s %s\n' "$1" "$2"; }
fail(){ printf 'FAIL %-28s %s\n' "$1" "$2"; bad=1; }
for c in python3 openssl sha256sum; do command -v "$c" >/dev/null 2>&1 && pass "command:$c" "$(command -v "$c")" || fail "command:$c" missing; done
if command -v osv-scanner >/dev/null 2>&1; then
  pass command:osv-scanner "$(command -v osv-scanner)"
  pass osv-scanner-version "$(osv-scanner --version 2>&1 | head -1)"
else
  fail command:osv-scanner 'missing; run ./deploy/m3/install_osv_scanner.sh'
fi
if [ "$bad" -ne 0 ]; then echo 'M3 RELEASE-AUTHORITY PREFLIGHT: FAIL'; exit 2; fi
echo 'M3 RELEASE-AUTHORITY PREFLIGHT: PASS'
