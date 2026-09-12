#!/usr/bin/env bash
set -euo pipefail
if [ "${EUID}" -eq 0 ]; then SUDO=''; else SUDO='sudo'; fi
. /etc/os-release 2>/dev/null || true
if [ "${ID:-}" != ubuntu ] || [ "${VERSION_ID:-}" != 24.04 ]; then
  echo "ERROR: this helper is intentionally limited to Ubuntu 24.04 LTS; detected ${PRETTY_NAME:-unknown}" >&2
  exit 2
fi
$SUDO apt-get update
$SUDO apt-get install -y --no-install-recommends \
  python3 python3-venv python3-pip python3-pytest \
  git openssl ca-certificates tar gzip coreutils findutils mawk

echo 'PASS: baseline Node1 prerequisites installed'
echo 'NOTE: Ubuntu repository pytest may be older than the optional pyproject dev range; the current M0-M1 tests use no pytest-8-only feature.'
