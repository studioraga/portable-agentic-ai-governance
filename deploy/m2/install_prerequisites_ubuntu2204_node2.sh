#!/usr/bin/env bash
set -euo pipefail
if [ ! -r /etc/os-release ]; then echo 'ERROR: /etc/os-release unavailable' >&2; exit 2; fi
. /etc/os-release
if [ "${ID:-}" != ubuntu ] || [ "${VERSION_ID:-}" != 22.04 ]; then
  echo "ERROR: this installer is for Ubuntu 22.04; detected ${PRETTY_NAME:-unknown}" >&2
  exit 2
fi
sudo apt update
sudo apt install -y --no-install-recommends \
  python3 python3-venv python3-pip python3-pytest \
  openssl ca-certificates tar gzip coreutils findutils mawk
python3 - <<'PY'
import ssl, sys
assert sys.version_info >= (3,10), sys.version
assert ssl.HAS_TLSv1_3, ssl.OPENSSL_VERSION
print('PASS: Python', sys.version.split()[0])
print('PASS: TLS1.3', ssl.OPENSSL_VERSION)
PY
echo 'PASS: Node2 Ubuntu 22.04 M2 prerequisites installed'
