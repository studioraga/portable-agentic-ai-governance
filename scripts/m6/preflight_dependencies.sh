#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
for c in python3 openssl sha256sum install tar gzip; do command -v "$c" >/dev/null || { echo "FAIL command:$c"; exit 2; }; echo "PASS command:$c $(command -v "$c")"; done
python3 - <<'PY'
import sys
assert sys.version_info >= (3,10), sys.version
print('PASS python-version', '.'.join(map(str,sys.version_info[:3])))
PY
openssl genpkey -algorithm ED25519 -out /tmp/pag-m6-ed25519.$$ >/dev/null 2>&1 && rm -f /tmp/pag-m6-ed25519.$$ && echo 'PASS openssl-ed25519 supported'
python3 "$ROOT/scripts/m3/check_dependency_inventory.py" "$ROOT" --require-empty-runtime >/tmp/pag-m6-deps.$$
cat /tmp/pag-m6-deps.$$; rm -f /tmp/pag-m6-deps.$$
echo 'PASS python-runtime-dependencies 0 third-party dependencies'
echo 'M6 DEPENDENCY PREFLIGHT: PASS'
