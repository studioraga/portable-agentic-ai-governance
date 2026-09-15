#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
fail=0
pass(){ printf 'PASS %-30s %s\n' "$1" "$2"; }
err(){ printf 'FAIL %-30s %s\n' "$1" "$2"; fail=1; }
for c in python3 openssl sha256sum install tar gzip; do
  command -v "$c" >/dev/null && pass "command:$c" "$(command -v "$c")" || err "command:$c" missing
done
python3 - <<'PY' >/tmp/pag-m4-python-version
import sys
assert sys.version_info >= (3,10), sys.version
print(sys.version.split()[0])
PY
pass python-version "$(cat /tmp/pag-m4-python-version)"
openssl genpkey -algorithm ED25519 -out /tmp/pag-m4-ed25519.key >/dev/null 2>&1 && pass openssl-ed25519 supported || err openssl-ed25519 unsupported
rm -f /tmp/pag-m4-ed25519.key /tmp/pag-m4-python-version

# Python 3.10 has no stdlib tomllib. Use the already fail-closed dependency
# inventory implementation, which includes a conservative Python-3.10
# pyproject fallback and supported lock/manifest detection.
if python3 "$ROOT/scripts/m3/check_dependency_inventory.py" "$ROOT" --require-empty-runtime >/tmp/pag-m4-dependency-inventory.out; then
  cat /tmp/pag-m4-dependency-inventory.out
  pass python-runtime-dependencies '0 third-party dependencies'
else
  cat /tmp/pag-m4-dependency-inventory.out 2>/dev/null || true
  err python-runtime-dependencies 'dependency inventory/review failed'
fi
rm -f /tmp/pag-m4-dependency-inventory.out
[ $fail -eq 0 ] || { echo 'M4 DEPENDENCY PREFLIGHT: FAIL'; exit 2; }
echo 'M4 DEPENDENCY PREFLIGHT: PASS'
