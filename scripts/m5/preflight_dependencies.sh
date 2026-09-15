#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
for c in python3 openssl sha256sum install tar gzip; do
  command -v "$c" >/dev/null || { echo "FAIL command:$c"; exit 2; }
  echo "PASS command:$c $(command -v "$c")"
done
python3 - <<'PY'
import sys
assert sys.version_info >= (3,10), sys.version
print('PASS python-version', sys.version.split()[0])
PY
_tmpkey="$(mktemp)"
trap 'rm -f "${_tmpkey:-}"' EXIT
openssl genpkey -algorithm Ed25519 -out "$_tmpkey" 2>/dev/null || { echo 'FAIL openssl-ed25519'; exit 2; }
echo 'PASS openssl-ed25519 supported'

# Python 3.10 does not provide stdlib tomllib. Reuse the repository's
# Python-3.10-safe deterministic dependency inventory rather than adding a
# runtime TOML dependency merely for preflight validation.
python3 "$ROOT/scripts/m3/check_dependency_inventory.py" "$ROOT" --require-empty-runtime >/tmp/pag-m5-dependency-inventory.out || {
  cat /tmp/pag-m5-dependency-inventory.out 2>/dev/null || true
  rm -f /tmp/pag-m5-dependency-inventory.out
  echo 'FAIL python-runtime-dependencies dependency inventory/review failed'
  exit 2
}
cat /tmp/pag-m5-dependency-inventory.out
rm -f /tmp/pag-m5-dependency-inventory.out
echo 'PASS python-runtime-dependencies 0 third-party dependencies'
echo 'M5 DEPENDENCY PREFLIGHT: PASS'
