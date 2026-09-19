#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.."&&pwd)"
for c in python3 openssl sha256sum install tar gzip;do command -v "$c" >/dev/null||{ echo "FAIL command:$c";exit 2;};echo "PASS command:$c $(command -v "$c")";done
python3 - <<'PY'
import sys,fcntl
assert sys.version_info>=(3,10),sys.version
print('PASS python-version',sys.version.split()[0]);print('PASS python-stdlib fcntl available')
PY
PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}" python3 "$ROOT/scripts/m3/check_dependency_inventory.py" "$ROOT" --require-empty-runtime
echo 'M9 DEPENDENCY PREFLIGHT: PASS'
