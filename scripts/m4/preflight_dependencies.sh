#!/usr/bin/env bash
set -euo pipefail
fail=0
pass(){ printf 'PASS %-30s %s\n' "$1" "$2"; }
err(){ printf 'FAIL %-30s %s\n' "$1" "$2"; fail=1; }
for c in python3 openssl sha256sum install tar gzip; do command -v "$c" >/dev/null && pass "command:$c" "$(command -v "$c")" || err "command:$c" missing; done
python3 - <<'PY' >/tmp/pag-m4-python-version
import sys
assert sys.version_info >= (3,10), sys.version
print(sys.version.split()[0])
PY
pass python-version "$(cat /tmp/pag-m4-python-version)"
openssl genpkey -algorithm ED25519 -out /tmp/pag-m4-ed25519.key >/dev/null 2>&1 && pass openssl-ed25519 supported || err openssl-ed25519 unsupported
rm -f /tmp/pag-m4-ed25519.key /tmp/pag-m4-python-version
python3 - <<'PY' >/tmp/pag-m4-deps
import tomllib
from pathlib import Path
p=tomllib.loads(Path('pyproject.toml').read_text())
d=p.get('project',{}).get('dependencies',[])
print(len(d))
PY
count="$(cat /tmp/pag-m4-deps)"; rm -f /tmp/pag-m4-deps
[ "$count" = 0 ] && pass python-runtime-dependencies '0 third-party dependencies' || err python-runtime-dependencies "$count declared; review/pin before M4 validation"
[ $fail -eq 0 ] || { echo 'M4 DEPENDENCY PREFLIGHT: FAIL'; exit 2; }
echo 'M4 DEPENDENCY PREFLIGHT: PASS'
