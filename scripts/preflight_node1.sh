#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

fail=0
pass() { printf 'PASS %-28s %s\n' "$1" "${2:-}"; }
warn() { printf 'WARN %-28s %s\n' "$1" "${2:-}"; }
err()  { printf 'FAIL %-28s %s\n' "$1" "${2:-}"; fail=1; }

printf '%s\n' '=== Portable Agentic AI Governance: Node1 preflight ==='

if [ -r /etc/os-release ]; then
  . /etc/os-release
  case "${ID:-}:${VERSION_ID:-}" in
    ubuntu:24.04) pass OS "Ubuntu ${VERSION_ID}" ;;
    *) warn OS "validated target is Ubuntu 24.04 LTS; detected ${PRETTY_NAME:-unknown}" ;;
  esac
else
  warn OS '/etc/os-release unavailable'
fi

for cmd in bash python3 tar gzip sha256sum openssl install df awk find sort xargs; do
  if command -v "$cmd" >/dev/null 2>&1; then
    pass "command:$cmd" "$(command -v "$cmd")"
  else
    err "command:$cmd" 'missing'
  fi
done

if command -v git >/dev/null 2>&1; then
  pass command:git "$(git --version)"
else
  warn command:git 'not required at runtime; recommended for source control'
fi

if python3 - <<'PY' >/dev/null 2>&1
import sys
raise SystemExit(0 if sys.version_info >= (3, 10) else 1)
PY
then
  pass python-version "$(python3 -V 2>&1)"
else
  err python-version "Python 3.10+ required; found $(python3 -V 2>&1 || true)"
fi

if python3 -m venv --help >/dev/null 2>&1; then
  pass python-venv 'available'
else
  err python-venv 'install python3-venv (Ubuntu 24.04: sudo apt install python3-venv)'
fi

if python3 -m pip --version >/dev/null 2>&1; then
  pass pip "$(python3 -m pip --version)"
else
  warn pip 'optional for runtime; required only to install pytest/dev tools with pip'
fi

if python3 -m pytest --version >/dev/null 2>&1; then
  pass pytest "$(python3 -m pytest --version 2>&1 | head -1)"
else
  warn pytest 'full extended suite unavailable until pytest is installed; built-in self-tests remain available'
fi

for p in src schemas governance agents docs tests scripts deploy examples release; do
  [ -e "$p" ] && pass "repo:$p" present || err "repo:$p" missing
done

for f in README.md instruction.md pyproject.toml docs/Architecture.md docs/Validation.md docs/Deployment.md docs/Milestones.md; do
  [ -r "$f" ] && pass "file:$f" readable || err "file:$f" missing
 done

if [ -w . ]; then pass repo-write 'repository root writable'; else err repo-write 'repository root not writable'; fi

avail_kb=$(df -Pk . | awk 'NR==2 {print $4}')
if [ "${avail_kb:-0}" -ge 102400 ]; then
  pass disk-space "${avail_kb} KiB available"
else
  err disk-space 'at least 100 MiB free required'
fi

# Production secrets are intentionally not required for lab preflight.
if [ "${PAG_SECURITY_PROFILE:-lab}" = production ]; then
  [ "${PAG_FAIL_CLOSED:-}" = 1 ] && pass PAG_FAIL_CLOSED 1 || err PAG_FAIL_CLOSED 'must be 1 in production'
  for v in PAG_EVIDENCE_SIGNING_KEY PAG_REQUEST_SIGNING_KEY PAG_APPROVAL_SIGNING_KEY; do
    value="${!v:-}"
    if [ "${#value}" -ge 32 ]; then pass "$v" 'present, length >=32'; else err "$v" 'missing or shorter than 32 characters'; fi
  done
  if [ "${PAG_EVIDENCE_SIGNING_KEY:-}" = "${PAG_REQUEST_SIGNING_KEY:-}" ] || \
     [ "${PAG_EVIDENCE_SIGNING_KEY:-}" = "${PAG_APPROVAL_SIGNING_KEY:-}" ] || \
     [ "${PAG_REQUEST_SIGNING_KEY:-}" = "${PAG_APPROVAL_SIGNING_KEY:-}" ]; then
    err signing-key-separation \
      'evidence, request and approval signing keys must be independent'
  else
    pass signing-key-separation independent
  fi
else
  pass security-profile "${PAG_SECURITY_PROFILE:-lab}"
fi

if [ "$fail" -ne 0 ]; then
  echo 'PREFLIGHT: FAIL'
  exit 2
fi
echo 'PREFLIGHT: PASS'
