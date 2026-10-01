#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)";cd "$ROOT";export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
git -c safe.directory="$ROOT" diff --check
python3 -m compileall -q src/portable_ai_governance/platform_security scripts/m21
python3 -m pytest -q tests/platform_security
python3 -m json.tool governance/platform/m21/platform-security-policy.json >/dev/null
python3 -m json.tool governance/platform/m21/threat-model.json >/dev/null
if command -v systemd-analyze >/dev/null; then systemd-analyze verify examples/m21/systemd/pag-platform-demo.service >/dev/null; fi
if command -v apparmor_parser >/dev/null; then
    AA_ERR="$(mktemp)"
    if ! apparmor_parser \
        -Q \
        -K \
        -q \
        examples/m21/apparmor/usr.bin.pag-platform-demo \
        >/dev/null 2>"$AA_ERR"
    then
        echo "FAIL: AppArmor profile syntax validation failed" >&2
        cat "$AA_ERR" >&2
        rm -f "$AA_ERR"
        exit 1
    fi

    if [[ -s "$AA_ERR" ]]; then
        echo "INFO: AppArmor profile syntax valid; non-fatal parser/runtime diagnostics suppressed"
    fi

    rm -f "$AA_ERR"
fi
echo 'PASS: M21 local CI/CD platform-security gate complete'
